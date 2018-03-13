# Usage:
# bash filter.sh path
# 
# Example:
# bash filter.sh ClearnlpOutput/Part1

bash word_filter.sh $1 | python file_filter.py 