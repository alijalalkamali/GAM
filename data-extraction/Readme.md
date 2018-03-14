# Data-extraction

### Installation
This project is based on python3.
Using pip:
```
pip install corenlp_xml
```

## Usage
Download ClearNLPwithCoreNLPTokenizer.jar and move data sets into the data folder as following directory structure.

```
Default data directory:
data-extraction/
├── data
│   ├── 20140519
│   │   ├── ClearNLPOutput
│   │   ├── CoreNLPOutput   
│   │   └── NewsTextFiles   
│   └── params
│       ├── country_nationality.txt
│       └── stativewords.txt
├── file_filter.py
├── filter.sh
├── ClearNLPwithCoreNLPTokenizer.jar
└── word_filter.sh
```

Extract data from a directory.
```
python3 data-extraction.py              \
    -i 20140519/ClearnlpOutput/Part1    \
    -o outputs/20140519/Part1
```

Parameters:

- -i:
- -o:

