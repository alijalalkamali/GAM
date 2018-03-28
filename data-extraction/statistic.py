import argparse
import logging
import os.path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoocurrenceCounter:
    def __init__(self):
        pass
    
    def count(self):
        pass

def main():
    parser = argparse.ArgumentParser(description='Analyze extracted data.')
    parser.add_argument(
        '--inputdir', '-i', required=True, help='input extracted data')
    parser.add_argument(
        '--outputdir', '-o', default='', help='directory for output')

    args = parser.parse_args()
    input_dir = args.inputdir.rstrip('/')

    if not os.path.isdir(input_dir):
        logger.warning(
            'input directory \'%s\' doesn\'t exist', input_dir)
    for filename in os.listdir(input_dir):
        # Count coocurrence from file.
        pass


if __name__ == '__main__':
    main()