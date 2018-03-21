import argparse
import os.path
import srl_processing
import subprocess


def is_valid_imput(args):
    '''(TODO:Input validity check)'''
    return True


def main():
    parser = argparse.ArgumentParser(description='Extract data from newsTexts.')
    parser.add_argument('--inputdir', '-i', required=True, help='input train file')
    parser.add_argument('--outputdir', '-o', default='outputs/', help='directory for outputs')
    
    args = parser.parse_args()
    
    if not is_valid_imput(args):
        return
    
    # Filtering files by state
    bash_cmd = 'bash filter.sh %s'%args.inputdir
    subprocess.call(bash_cmd, stdout=subprocess.STDOUT, stderr=subprocess.STDOUT, shell=True)
    
    # Process files. Save in a list.
    sp = srl_processing.SrlProcessor()
    lines = []
    for ans in sp.process_list('list.txt'):
        lines.append(ans)
        
    # Write outputs to files
    if not os.path.isdir(args.outputdir):
        os.makedirs(args.outputdir)
    
    
    outpath = os.path.join(args.outputdir, 'out.txt')
    with open(outpath, 'a') as fp:
        fp.writelines(lines)
        
if __name__ == '__main__':
    main()