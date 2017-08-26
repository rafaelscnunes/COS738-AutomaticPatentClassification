# Automatic Patent Classification
Machine Learning System to classify a Patent Request based on it's title and 
resume, using INPI-Brazil RPI Patent text data for training the model.

## Modules
1. download - downloads the last available RPI on http://revistas.inpi.gov.br
2. import  - parses all .txt or .TXT on ./input and generates ./output/
\<RPI>.csv, \<RPI>_parsed.txt and ./import.log;
3. pre_processing - based on full.csv generates dataset.csv containing 
title|resume|ipc|ipc1|ipc2|ipc3|ipc4, with stemmed text using nltk.stem
.RSLPStemmer() and separating each patent request IPC code in one line, 
therefore the same patent request will have as many replicas as the number 
of classifications it have.


## Inputs
1. ./input/\*.txt or ./input/\*.TXT - RPI (Revista da Propriedade 
Industrial) one per file;

## Outputs
1. ./import.log - record execution informations.
2. ./output/\<RPI>_parsed.txt - processed RPI file (debug)
3. ./output/\<RPI>.csv - records extracted from <RPI>.txt file
4. ./output/full.csv - all records extracted from all <RPI>.txt
5. ./imported/\<RPI>.txt - archives all imported .txt files
6. ./output/dataset.csv - pre-processed records.

## References
1. http://revistas.inpi.gov.br - download Patent section of RPI (.txt's) 
2. http://dados.gov.br/dataset/revista-da-propriedade-industrial-rpi
/resource/4288c07c-f9bd-45d7-8fc0-56b4fc1f5c82 - informations on how to get 
RPI files