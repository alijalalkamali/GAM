import argparse
import collections
import file_util
import logging
import os.path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoocurrenceCounter:
    def __init__(self):
        self.actions = set()
        self.positive_count = collections.defaultdict(collections.Counter)
        self.negative_count = collections.defaultdict(collections.Counter)
        neg_stative_path = 'data/params/neg_stative.txt'
        self.negative_list = file_util.file_loader(neg_stative_path)
        state_path = 'data/params/state.txt'
        self.state_list = file_util.file_loader(state_path)
    
    def count(self, state, action, stative_verb):
        self.actions.add(action)
        if self.is_positive(stative_verb):
            self.positive_count[action][state] += 1
        else:
            self.negative_count[action][state] += 1
        
    def is_positive(self, stative_verb):
        return stative_verb in self.negative_list
        
    def generate_report(self):
        for action in self.actions:
            tokens = [action]
            total_with_action = 0
            for state in self.state_list:
                total = (
                    self.positive_count[action][state]
                    + self.negative_count[action][state])
                if total == 0:
                    tokens.append('')
                    continue
                total_with_action += total
                ratio = self.positive_count[action][state]/total
                tokens.append('%d-%d'%(ratio*100, 100-ratio*100))
            tokens.append(str(total_with_action))
            yield ','.join(tokens)
        

def main():
    parser = argparse.ArgumentParser(description='Analyze extracted data.')
    parser.add_argument(
        '--inputdir', '-i', required=True, help='input extracted data')
    parser.add_argument(
        '--outputdir', '-o', default='outputs', help='directory for output')

    args = parser.parse_args()
    input_dir = args.inputdir.rstrip('/')
    output_dir = args.outputdir
    outputname = 'summary.txt'

    if not os.path.isdir(input_dir):
        logger.warning(
            'input directory \'%s\' doesn\'t exist', input_dir)
        return
    
    counter = CoocurrenceCounter()
    for filename in os.listdir(input_dir):
        if len(filename) > 0 and filename[0] == '.':
            continue
        # Count coocurrence from file.
        with open(os.path.join(input_dir, filename)) as fp:
            for line in fp.readlines():
                tokens = line.split(',')
                counter.count(tokens[4], tokens[3], tokens[5])
    
    outpath = os.path.join(output_dir, outputname)         
    with open(outpath, 'w+') as fp:
        # Print Title
        state_list = file_util.file_loader('data/params/state.txt')
        title_line = 'X,{},Total Count\n'.format(','.join(state_list) )
        fp.write(title_line)

        for line in counter.generate_report():
            fp.write(line)
            fp.write('\n')


if __name__ == '__main__':
    main()