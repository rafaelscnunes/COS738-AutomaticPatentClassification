#!/Library/Frameworks/Python.framework/Versions/3.6/bin/Python3.6
# -*- coding: utf-8 -*-
"""
Created on 23/Aug/2017 with PyCharm Community Edition
@title:  Work3 - Automatic Patent Classification - download
@author: rafaenune - Rafael Nunes - rnunes@cos.ufrj.br


    Downloads only the last RPI available at http://revistas.inpi.gov.br/
"""

import datetime
import urllib.request
import json
import zipfile
import os

BASE_URL = "http://revistas.inpi.gov.br/"
BUSCA = "rpi/busca/data?"
TXT = "txt/"
DATA_INICIAL = "01/01/1900"
DATA_FINAL = datetime.datetime.now().strftime("%d/%m/%Y")
TIPO_REVISTA = {'Comunicados': '1',
               'Contratos': '2',
               'Desenhos': '3',
               'Indicações': '4',
               'Marcas': '5',
               'Patentes': '6',
               'Programas': '7',
               'Circuitos': '8'
              }
OUTPUT_FOLDER = "./input/"

# downloading JSON with all RPIs since 01/Jan/1900
search_url = BASE_URL + BUSCA + "revista.dataInicial=" + DATA_INICIAL + \
      "&revista.dataFinal=" + DATA_FINAL + "&revista.tipoRevista.id=" + \
      TIPO_REVISTA['Patentes']
patents_rpis = json.loads(urllib.request.urlopen(search_url).read())

# downloading Pxxxx.zip file
download_url = BASE_URL + TXT + patents_rpis[0]['nomeArquivoEscritorio']
zip_file = OUTPUT_FOLDER + patents_rpis[0]['nomeArquivoEscritorio']
urllib.request.urlretrieve(download_url, zip_file)

# extracting Pxxxx.zip file into ./input folder
zfobj = zipfile.ZipFile(zip_file)
for name in zfobj.namelist():
    uncompressed = zfobj.read(name)
    outputFilename = OUTPUT_FOLDER + name
    output = open(outputFilename, 'wb')
    output.write(uncompressed)
    output.close()
os.remove(zip_file)
