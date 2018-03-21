import pathlib
import argparse
import subprocess
import srl_processing


def is_valid_input(args):
    '''(TODO:Input validity check)'''
    return True


def main():
    parser = argparse.ArgumentParser(description='Extract data from newsTexts.')
    parser.add_argument('--inputdir', '-i', help='input train file')
    parser.add_argument('--outputdir', '-o', help='directory for outputs')
    
    args = parser.parse_args()
    
    if not is_valid_input(args):
        return
    
    # Filtering files by state
    p = subprocess.Popen(['bash', 'filter.sh', args.inputdir])
    if p.wait() != 0: return None
    
    # Process files
    sp = srl_processing.SrlProcessor()
    lines = []
    for ans in sp.process_list('list.txt'):
        if ans:
            lines.append(ans)
        
    # Write outputs to files
    outpath = '%s/out.txt'%args.outputdir
    pathlib.Path(args.outputdir).mkdir(parents=True, exist_ok=True)
    with open(outpath, 'w+') as fp:
        fp.writelines(lines)
        
if __name__ == '__main__':
    main()