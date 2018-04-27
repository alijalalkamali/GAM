import argparse
import logging
import savReaderWriter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Extract data from newsTexts.')
parser.add_argument('--inputdir', '-i', required=True, help='input train file')
parser.add_argument('--outputdir', '-o', default='outputs/', help='directory for outputs')
args = parser.parse_args()

with savReaderWriter.SavReader(args.inputdir) as reader:
    header = reader.header
    for line in reader:
        print len(line)
        print line
        import pdb; pdb.set_trace()