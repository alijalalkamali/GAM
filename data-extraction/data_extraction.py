import argparse
import logging
import os.path
import pathlib
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
    
    # Process files. Save in a list.
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
    parser.add_argument('--part', '-p', action='store_true', help='process part directory')

    args = parser.parse_args()
    args.inputdir = args.inputdir.rstrip('/')
    
    if not is_valid_input(args):
        return
    
    def gen_output_filename(_dir):
        _dir_split = _dir.split('/')
        return '_'.join([_dir_split[-3], _dir_split[-1]])
    
    if args.part:
        outputname = '%s.txt'%(gen_output_filename(args.inputdir))
        # import pdb; pdb.set_trace()
        extract_part(args.inputdir, args.outputdir, outputname)
    else:
        clearnlp_dir = os.path.join(args.inputdir, 'ClearNLPOutput')
        if not os.path.isdir(clearnlp_dir):
            logging.warning(
                'ClearNLPOutput path \'%s\' doesn\'t exist', clearnlp_dir)
        for part_id in os.listdir(clearnlp_dir):
            logging.info('Processing %s', part_id)
            inputdir = os.path.join(clearnlp_dir, part_id)
            outputname = '%s.txt'%(gen_output_filename(inputdir))
            extract_part(inputdir, args.outputdir, outputname)
    
        
if __name__ == '__main__':
    main()