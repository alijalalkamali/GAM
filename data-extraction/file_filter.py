#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

state_words=[
    "force",
    "cooperation",
    "welfare",
    "military",
    "tie",
    "economy",
    "GDP",
    "tension",
    "trade"
]

def get_full_path(path_format, path):
    return path_format.format(path)

def check_corenlp_file(filename, sen_id, content):
    f = open(get_full_path(corenlp_path, filename), 'rb')
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

def reproduce_clearnlp(file_path):
    print('Reproduce %s...' % (file_path))

    part_id, filename = tuple(file_path.split('/'))
    subprocess.Popen(['bash', './convert_clearnlp.sh', part_id, filename])

    print("{} has been reproduced.".format(get_full_path(text_path, file_path)))

def parse_id():
    reproduce_files = []
    file_candidates = []

    for file_path in sys.stdin:
        sen_id = 0
        file_path = file_path.strip()
        _file_candidates = []
        with open(file_path, 'r') as f:
            _, part_id, filename = tuple(file_path.split('/'))
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
                    _filename = '{}/{}'.format(part_id, filename.split('.')[0])

                    if not os.path.isfile(get_full_path(corenlp_path, _filename)) or \
                        not os.path.isfile(get_full_path(text_path, _filename)):
                        continue

                    if not check_corenlp_file(_filename, sen_id, content):
                        reproduce_files.append(_filename)
                        _file_candidates = []
                        break

                    cand = ','.join((_filename, str(sen_id), str(content['id']), content['lemma']))
                    _file_candidates.append(cand)

        if _file_candidates:
            file_candidates.extend(_file_candidates)

    if reproduce_files:
        print('Reproduce unmatched files...')

        if os.path.isdir(reproduce_dir):
            shutil.rmtree(reproduce_dir)
        os.makedirs(reproduce_dir)

        part_file_subpath_list = set()

        for file in reproduce_files:
            part_id, filename = tuple(file.split('/'))
            part_file_subpath = reproduce_dir + '/' + part_id
            part_file_subpath_list.add(part_file_subpath)
            if not os.path.isdir(part_file_subpath):
                os.makedirs(part_file_subpath)

            src_path = get_full_path(text_path, file)
            des_path = get_full_path(reproduce_path, file)
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

        print('Reproducing completed!')

        for part_id in os.listdir(reproduce_output_dir):
            for filename in os.listdir(reproduce_output_dir + '/' + part_id):
                file_path = '{}/{}/{}'.format(reproduce_output_dir, part_id, filename)
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
                            _filename = '{}/{}'.format(part_id, filename.split('.')[0])

                            cand = ','.join((_filename, str(sen_id), str(content['id']), content['lemma']))
                            file_candidates.append(cand)
                
                des_path = get_full_path(clearnlp_path, '{}/{}'.format(part_id, filename.split('.')[0]))
                shutil.move(file_path, des_path)

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
