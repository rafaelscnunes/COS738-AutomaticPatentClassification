# Automatic Patent Classification
Machine Learning System to classify a Patent Request based on it's title and 
resume, using INPI-Brazil RPI Patent text data for training the model.

## Modules
1. import  - parses all .txt or .TXT on ./input and generates ./output/
\<RPI>.csv, \<RPI>_parsed.txt and ./import.log;

## Inputs
1. ./input/\*.txt or ./input/\*.TXT - RPI (Revista da Propriedade 
Industrial) one per file;

## Outputs
1. ./import.log - record execution informations.
2. ./output/\<RPI>_parsed.txt - processed RPI file (debug)
3. ./output/\<RPI>.csv - records extracted from <RPI>.txt file
4. ./output/full.csv - all records extracted from all <RPI>.txt

## References
1. http://revistas.inpi.gov.br - download Patent section of RPI (.txt's) 
 
