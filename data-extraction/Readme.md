# Data-extraction

### Installation
This project is based on python3.
Using pip:
```
pip install corenlp_xml
```

### Quick Start
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

Filter data sets
```
bash filter.sh 20140519/ClearnlpOutput/Part1
```
The result file 'list.txt' will be used in the next step.

## Usage

````bash

````

## Input format


## Output format

