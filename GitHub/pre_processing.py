#!/Library/Frameworks/Python.framework/Versions/3.6/bin/Python3.6
# -*- coding: utf-8 -*-
"""
Created on 23/Aug/2017 with PyCharm Community Edition
@title:  Work3 - Automatic Patent Classification - pre_processing
@author: rafaenune - Rafael Nunes - rnunes@cos.ufrj.br
"""
import re
import nltk
import time

t = time.process_time()
count = 0
MIN_WORD_LENGHT = 2
input_csv = "./github/output/full.csv"
output_csv = "./github/output/dataset_ipc_first.csv"
# stemmer = nltk.stem.PorterStemmer()
stemmer = nltk.stem.RSLPStemmer()
stop_words = []
patent_base = {}

try:
    in_csv = open(input_csv, 'r', encoding = 'latin-1')
    line = in_csv.readline()
except:
    line = ''

if line.lower() == 'número do pedido|classificação ' \
                   'internacional|título|resumo|complemento|comentários|rpi\n':
    for line in in_csv:
        count += 1
        if line.split('|')[0] not in patent_base:
            patent_base[line.split('|')[0]] = {}
            patent_base[line.split('|')[0]]['ipc'] = line.split('|')[1].split(',')
            words = line.split('|')[2].split()
            words = [re.sub('[^a-zA-Z]', '', word) for word in words]
            words = [stemmer.stem(word) for word in words
                     if not word in stop_words
                     and len(word) >= MIN_WORD_LENGHT]
            patent_base[line.split('|')[0]]['title'] = ' '.join(words)
            words = line.split('|')[3].split()
            words = [re.sub('[^a-zA-Z]', '', word) for word in words]
            words = [stemmer.stem(word) for word in words
                     if not word in stop_words
                     and len(word) >= MIN_WORD_LENGHT]
            patent_base[line.split('|')[0]]['resume'] = ' '.join(words)
            patent_base[line.split('|')[0]]['rpi'] = int(line.split('|')[6][
                                                         :-1])
            # print(line.split('|')[0] + ': '
            #       + patent_base[line.split('|')[0]]['title'] + '|'
            #       + patent_base[line.split('|')[0]]['resume'] + '|'
            #       + str(patent_base[line.split('|')[0]]['ipc']))
        else:
            # print('O pedido %s já foi processado na RPI %d!!' % (line.split(
            #         '|')[0], patent_base[line.split('|')[0]]['rpi']))
            if int(line.split('|')[6]) > patent_base[line.split('|')[0]][
                'rpi']:
                # print(patent_base[line.split('|')[0]])
                patent_base[line.split('|')[0]]['ipc'] = line.split('|')[
                    1].split(',')
                words = line.split('|')[2].split()
                words = [re.sub('[^a-zA-Z]', '', word) for word in words]
                words = [stemmer.stem(word) for word in words
                         if not word in stop_words
                         and len(word) >= MIN_WORD_LENGHT]
                patent_base[line.split('|')[0]]['title'] = ' '.join(words)
                words = line.split('|')[3].split()
                words = [re.sub('[^a-zA-Z]', '', word) for word in words]
                words = [stemmer.stem(word) for word in words
                         if not word in stop_words
                         and len(word) >= MIN_WORD_LENGHT]
                patent_base[line.split('|')[0]]['resume'] = ' '.join(words)
                patent_base[line.split('|')[0]]['rpi'] = int(
                        line.split('|')[6])
                # print(patent_base[line.split('|')[0]])
                # print('Pedido %s reprocessando agora na RPI %d.' % (
                #     line.split('|')[0], patent_base[line.split('|')[0]]['rpi']))
        # if count == 5000: break
    in_csv.close()
else:
    print('Arquivo full.csv inexistente ou corrompido. Nada foi feito!')

out_csv = open(output_csv, 'w', encoding = 'latin-1')
out_csv.write('title|resume|ipc\n')
for patent in patent_base:
    out_csv.write(patent_base[patent]['title'] + '|'
                  + patent_base[patent]['resume'] + '|'
                  + patent_base[patent]['ipc'][0] + '\n')
    # print(patent_base[patent]['title'] + '|'
    #               + patent_base[patent]['resume'] + '|'
    #               + patent_base[patent]['ipc'][0] + '\n')
    # for ipc_class in range(0, len(patent_base[patent]['ipc'])):
    #     out_csv.write(patent_base[patent]['title'] + '|'
    #                   + patent_base[patent]['resume'] + '|'
    #                   + patent_base[patent]['ipc'][ipc_class] + '|'
    #                   + patent_base[patent]['ipc'][ipc_class][:1] + '|'
    #                   + patent_base[patent]['ipc'][ipc_class][1:3] + '|'
    #                   + patent_base[patent]['ipc'][ipc_class][3:4] + '|'
    #                   + patent_base[patent]['ipc'][ipc_class][5:] + '\n')
# out_csv.close()
tt = time.process_time() - t
# print('Tempo total de processamento: %f segundos' % tt)

# performance log to estimate time of processing full.csv completely
f_log = open('./github/pre_processing2.log', 'a', encoding = 'utf-8')
print('count = %d' %count)
f_log.write('count = %d\n' %count)
print('Tempo total de processamento: %f segundos' % tt)
f_log.write('Tempo total de processamento: %f segundos\n' % tt)
print('Média por linha no full.csv: %f segundos' % (tt/count))
f_log.write('Média por linha no full.csv: %f segundos\n' % (tt/count))
print('Estimativa para 355k linhas: %f horas' % (tt/count*355000/3600))
f_log.write('Estimativa para 355k linhas: %f horas\n' % (tt/count*355000/3600))