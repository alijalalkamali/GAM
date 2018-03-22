#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os, sys
import subprocess
import shutil
from corenlp_xml.document import Document


list_filename = 'list.txt'
reproduce_dir = 'reproduce_input'
reproduce_output_dir = 'reproduce_output'
corenlp_path = 'CoreNLPOutput/{}.xml'
clearnlp_path = 'ClearnlpOutput/{}.txt.srl'
text_path = 'NewsTextFiles/{}.txt'
reproduce_path = reproduce_dir + '/{}.txt'
prefix_path = ''

state_words=[
    "force",
    "cooperation",
    "welfare",
    "military",
    "tie",
    "economy",
    "gdp",
    "tension",
    "trade"
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_full_path(prefix_path, path_format, path):
    return os.path.join(prefix_path, path_format.format(path))

def check_corenlp_file(prefix_path, filename, sen_id, content):
    f = open(get_full_path(prefix_path, corenlp_path, filename), 'rb')
    xml_string = f.read()
    f.close()

    doc = Document(xml_string)
    # check whether sentence id matches
    if len(doc.sentences) < sen_id:
        return False
    s = list(doc.sentences)[sen_id-1]

    # check whether word id matches
    node = s.basic_dependencies.get_node_by_idx(content['id'])
    if not node or node.text != content['lemma']:
        return False

    return True

def parse_id():
    reproduce_files = []
    file_candidates = []

    for file_path in sys.stdin:
        sen_id = 0
        file_path = file_path.strip()
        _file_candidates = []
        with open(file_path, 'r') as f:
            prefix_path = os.path.join(*(file_path.split('/')[:-3]))
            part_id, filename = tuple(file_path.split('/'))[-2:]
            for line in f:
                line = line.strip().split()
                if len(line) < 2:
                    continue
                content = {
                    'id': int(line[0]),
                    'lemma': line[2],
                }
                if content['id'] == 1:
                    sen_id += 1
                if content['lemma'] in state_words:
                    _filename = os.path.join(part_id, filename.split('.')[0])
                    # print(os.path.isfile(get_full_path(prefix_path, corenlp_path, _filename)))
                    # print(os.path.isfile(get_full_path(prefix_path, text_path, _filename)))
                    if not os.path.isfile(get_full_path(prefix_path, corenlp_path, _filename)):
                        logging.info('file missing: %s'%get_full_path(prefix_path, corenlp_path, _filename))
                        continue
                    if not os.path.isfile(get_full_path(prefix_path, text_path, _filename)):
                        logging.info('file missing: %s'%get_full_path(prefix_path, text_path, _filename))
                        continue
                    if not check_corenlp_file(prefix_path, _filename, sen_id, content):
                        reproduce_files.append(_filename)
                        _file_candidates = []
                        break

                    cand = ','.join((os.path.join(prefix_path, _filename), str(sen_id), str(content['id']), content['lemma']))
                    _file_candidates.append(cand)

        if _file_candidates:
            file_candidates.extend(_file_candidates)
    print(file_candidates)
    print(reproduce_files)
    if reproduce_files:
        logging.info('Reproduce unmatched files...')

        if os.path.isdir(reproduce_dir):
            shutil.rmtree(reproduce_dir)
        os.makedirs(reproduce_dir)

        part_file_subpath_list = set()

        for file in reproduce_files:
            logging.info(file)
            part_id, filename = tuple(file.split('/'))
            part_file_subpath = reproduce_dir + '/' + part_id
            part_file_subpath_list.add(part_file_subpath)
            if not os.path.isdir(part_file_subpath):
                os.makedirs(part_file_subpath)

            src_path = get_full_path(prefix_path ,text_path, file)
            des_path = get_full_path('', reproduce_path, file)
            shutil.copy(src_path, des_path)

        if os.path.isdir(reproduce_output_dir):
            shutil.rmtree(reproduce_output_dir)

        for path in part_file_subpath_list:
            part_id = path.split('/')[1]
            output_dir = reproduce_output_dir + '/' + part_id
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)

            p = subprocess.Popen(['java', '-jar', 'ClearNLPwithCoreNLPTokenizer.jar', path, output_dir])

            if p.wait() != 0: return None

        # clear temp input directory
        shutil.rmtree(reproduce_dir)
        logging.info('Reproducing completed!')

        for part_id in os.listdir(reproduce_output_dir):
            for filename in os.listdir(os.path.join(reproduce_output_dir, part_id)):
                sen_id = 0
                file_path = os.path.join(reproduce_output_dir, part_id, filename)
                with open(file_path, 'r') as f:
                    for line in f:
                        line = line.strip().split()
                        if len(line) < 3:
                            continue

                        if not line[0].isdigit():
                            print(file_path)
                            print(line)
                            break

                        content = {
                            'id': int(line[0]),
                            'lemma': line[2],
                        }
                        if content['id'] == 1:
                            sen_id += 1

                        if content['lemma'] in state_words:
                            _filename = os.path.join(part_id, filename.split('.')[0])

                            cand = ','.join((_filename, str(sen_id), str(content['id']), content['lemma']))
                            file_candidates.append(cand)
                
                des_path = get_full_path(prefix_path, clearnlp_path, '{}/{}'.format(part_id, filename.split('.')[0]))
                shutil.move(file_path, des_path)

        # clear temp output directory
        shutil.rmtree(reproduce_output_dir)

    return file_candidates

def main():
    '''
    Default data directory:
    data-extraction/
    ├── data
    │   ├── 20140519
    │   │   ├── ClearNLPOutput
    │   │   ├── CoreNLPOutput   
    │   │   └── NewsTextFiles   
    │   └── params
    │       ├── countr_map.txt
    │       └── stativewords.txt
    └── file_filter.py
    '''
    with open(list_filename, 'w') as f:
        for file in parse_id():
            f.write(file + '\n')


if __name__ == '__main__':
    main()
