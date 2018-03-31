import argparse
import logging
import os.path
import pathlib
import re
import srl_processing
import subprocess


sp = srl_processing.SrlProcessor() # singleton
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_valid_input(args):
    '''(TODO:Input validity check)'''
    return True

def extract_part(inputdir, outputdir, outputname):
    # Filtering files by state

    p = subprocess.Popen(['bash', 'filter.sh', inputdir])
    if p.wait() != 0: return None
    
    # Process files. Save in a list. Can use generator instead of buffering.
    lines = []
    for ans in sp.process_list('list.txt'):
        if ans:
            lines.append('%s\n'%','.join(ans))
    
    # Write outputs to files
    outpath = os.path.join(outputdir, outputname)
    pathlib.Path(outputdir).mkdir(parents=True, exist_ok=True)
    with open(outpath, 'w+') as fp:
        fp.writelines(lines)
        

def main():
    parser = argparse.ArgumentParser(description='Extract data from newsTexts.')
    parser.add_argument('--inputdir', '-i', required=True, help='input train file')
    parser.add_argument('--outputdir', '-o', default='outputs/', help='directory for outputs')

    args = parser.parse_args()
    full_inputdir = args.inputdir.rstrip('/')
    
    if not is_valid_input(args):
        return
    
    def gen_output_filename(_dir):
        _dir_split = _dir.split('/')
        return '_'.join([_dir_split[-3], _dir_split[-1]])
    
    def process_part(input_dir):
        outputname = '%s.txt'%(gen_output_filename(input_dir))
        extract_part(input_dir, args.outputdir, outputname)
        
    def process_date(input_dir):
        clearnlp_dir = os.path.join(input_dir, 'ClearNLPOutput')
        if not os.path.isdir(clearnlp_dir):
            logger.warning(
                'ClearNLPOutput path \'%s\' doesn\'t exist', clearnlp_dir)
        for part_id in os.listdir(clearnlp_dir):
            logger.info('Processing %s', part_id)
            inputdir = os.path.join(clearnlp_dir, part_id)
            outputname = '%s.txt'%(gen_output_filename(inputdir))
            extract_part(inputdir, args.outputdir, outputname)
            
    # Matching different level of input
    logger.info('Input directory: %s', full_inputdir)
    if re.match(r'.*Part[0-9]*$', full_inputdir):
        part_dir = full_inputdir
        process_part(part_dir)
    elif re.match(r'.*[0-9]{8}$', full_inputdir):
        date_dir = full_inputdir
        process_date(date_dir)
    else:
        logger.info('Batch date input')
        for date in os.listdir(full_inputdir):
            if not re.match('^[0-9]{8}$', date):
                # Not a date
                continue
            date_dir = os.path.join(full_inputdir, date)
            process_date(date_dir)
            
    # Report
    print('***********************************')
    print('End of data extraction.')
    print('# of sentence with state: %d', sp.state_count)
    print('# of sentence with stative verb: %d', sp.stative_verb_count)
    print('# of sentence with actor: %d', sp.actor_count)
    print('***********************************')
    
            
        
if __name__ == '__main__':
    main()