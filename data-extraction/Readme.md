# Data-extraction

### Features
- Extracts actors and their action that change the states.
- Check consistency between ClearNLP and CoreNLP tokenization and reproduce \
CoreNLP output if there are inconsistency.
- Resolve possesive pronouns by coreference resolution from CoreNLP output.
- Process all files in a directory.

### Installation
This project is based on python3.5+ and jdk8.

Install dependency using pip:
```
python3 -m pip install corenlp_xml
```

### Usage
Download ClearNLPwithCoreNLPTokenizer.jar and move data sets into the data folder as following directory structure.

```
Default data directory:
data_extraction/
├── data
│   ├── 20140519
│   │   ├── ClearNLPOutput
│   │   ├── CoreNLPOutput   
│   │   └── NewsTextFiles   
│   └── params
│       ├── country_nationality.txt
│       ├── neg_stative.txt
│       ├── state.txt
│       └── stativewords.txt
├── file_filter.py
├── filter.sh
├── ClearNLPwithCoreNLPTokenizer.jar
└── word_filter.sh
```

#### Extract data from a directory.
```
python3 data_extraction.py -i data
```

Parameters:

- -i: The directory which contains the output files.
- -o:(optional) The directory for output file. The output files will be saved in name \
{date}_{part}.txt. By default it will be saved in 'outputs' folder.

Examples:
```
python3 data_extraction.py -i data
```
```
python3 data_extraction.py -i data/20140519
```
```
python3 data_extraction.py -i data/20140519/ClearNLPOutput/Part1
```

#### Generate statistic summary.
```
python3 statistic.py -i outputs
```

Parameters:

- -i: The directory which contains the data extraction output.
- -o:(optional) The directory for output file. The output files will be saved in name \
summary.txt

### Output format
The output is saved in csv format. 
```
data/20140519/Part1/newsText22,Azerbaijani;Brazilian,0;0,play,trade,expand
```
Each line contains these columns:
- Source. The incomplete path of the source file.
- Actors. If there are more than one actors, they are separated by semicolons.
- Relation between actors and stative verb. 0 if actor is not in the subtree \
of stative verb. If actor is in the subtree of stative verb. If there are more \
than one actors, they are separated by semicolons.
- Action verb.
- State.
- Stative verb.

### Known Issues
