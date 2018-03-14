import argparse
import subprocess
import srl_processing


def is_valid_imput(args):
    '''(TODO:Input validity check)'''
    return True


def main():
    parser = argparse.ArgumentParser(description='Extract data from newsTexts.')
    parser.add_argument('--inputdir', '-i', help='input train file')
    parser.add_argument('--outputdir', '-o', help='directory for outputs')
    
    args = parser.parse_args()
    
    if not is_valid_imput(args):
        return
    
    # Filtering files by state
    bash_cmd = 'bash filter.sh %s'%args.inputdir
    subprocess.check_output(bash_cmd, stderr=subprocess.STDOUT)
    
    # Process files
    sp = srl_processing.SrlProcessor()
    lines = []
    for ans in sp.process_list('list.txt'):
        lines.append(ans)
        
    # Write outputs to files
    outpath = '%s/out.txt'%args.outputdir
    with open('outpath', 'a') as fp:
        fp.writelines(lines)
        
if __name__ == '__main__':
    main()