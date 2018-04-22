# ClearNLP and CoreNLP Token Comparer

https://drive.google.com/drive/u/1/folders/0B5KQB5IU1zaPb09rbTNXSC01UWM

### USAGE
java -jar ClearNLPCoreNLPTokenComparer.jar ./states.txt ./stative_verbs.txt [inputDir] [outputFile] [isSkipSame] 

[inputDir] is the input directory of newsText

[outputFile] is the output file including paths of all files need to be regenerated

[isSkipSame] is the indicator whether you want to skip those files with the same tokens 
(if you already have corenlpOutput and clearnlpOutput, you may set this as 1). Default value should be 0.

e.g.
java -jar ClearNLPCoreNLPTokenComparer.jar ./states.txt ./stative_verbs.txt ./data/Part1/ ./output.txt 0 

