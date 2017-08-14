#!/Library/Frameworks/Python.framework/Versions/3.6/bin/Python3.6
# -*- coding: utf-8 -*-
"""
Created on 14/Aug/2017 with PyCharm Community Edition
@title:  Automatic-Patent-Classification - import.py
@author: rafaenune - Rafael Nunes - rnunes@cos.ufrj.br
"""


import os
import re
import sys
import time
# import mysql.connector


#Dicionário com o significado de cada código de despacho
Cd  = {'PR - Recursos - Decisões':'PR - Recursos - Decisões',
      'PR - Recursos - Despachos':'PR - Recursos - Despachos',
      'PR - Cancelamentos':'PR - Cancelamentos',
      '1.1':'Publicação Internacional – PCT. Apresentação de petição de requerimento de entrada na fase nacional.',
      '1.1.1': 'Retificação',
      '1.1.2': 'Publicação anulada',
      '1.1.3': 'Republicação',
      '1.2': 'Notificação - Pedido retirado - PCT',
      '1.2.1': 'Publicação anulada',
      '1.2.2': 'Republicação',
      '1.2.3': 'Decisão anulada',
      '1.3': 'Notificação - Fase Nacional - PCT',
      '1.3.1': 'Retificação',
      '1.3.2': 'Publicação anulada',
      '1.3.3': 'Republicação',
      '1.3.4': 'Decisão anulada',
      '2.1': 'Pedido de Patente ou Certificado de Adição de Invenção depositado',
      '2.2':'???',
      '3.1':'Publicação do Pedido de Patente ou de Certificado de Adição de Invenção',
      '3.2':'Publicação Antecipada',
      '3.4':'???',
      '4.1':'???',
      '4.2':'???',
      '6.1':'Exigência Técnica',
      '6.5':'???',
      '7.1':'Conhecimento de Parecer Técnico',
      '9.1':'Deferimento',
      '9.1.3':'Republicação',
      '9.2':'Indeferimento',
      '10.1':'Desistência Homologada',
      '11.1':'Arquivamento - Art. 33 da LPI',
      '11.2':'Arquivamento - Art. 36 §1° da LPI',
      '11.8':'???',
      '12.1':'Recurso Contra o Deferimento',
      '12.2':'Recurso Contra o Indeferimento',
      '12.3':'Recurso Contra o Arquivamento',
      '13.1':'Notificação para Pagamento da Retribuição Relativa à Expedição da Carta-Patente dos Pedidos Deferidos na Vigência da Lei 5772/71',
      '13.3':'???',
      '14.1':'???',
      '14.2':'???',
      '14.4':'???',
      '14.7':'???',
      '14.11':'???',
      '15.1':'Arquivamento do Pedido de Patente por Comprovação e Recolhimento Intempestivo de Anuidade - AN 082/86 item 4.1',
      '15.3':'Arquivamento do Pedido de Patente por Falta de Comprovação e Recolhimento de Anuidade - AN 082/86 item 4.1',
      '15.5':'???',
      '15.10':'Mudança de Natureza',
      '15.11':'Alteração de Classificação',
      '15.15':'???',
      '15.17':'???',
      '16.1':'Concessão de Patente ou Certificado de Adição de Invenção',
      '17.1':'Notificação de Interposição de Nulidade Administrativa',
      '18.2':'Caducidade - Art 50 da Lei 5772/71',
      '22.2':'Petição Não Conhecida'}

class despachos:
    'Estrutura dos registros de despachos publicados nas RPIs, cada código INID tem seu próprio atributo'
    def __init__(self, codigo):
        self.rpi = ''
        self.codigo = codigo
        self.Co = '' #parece ser o mesmo que o campo complemento, mas foi criada uma variável específica mesmo assim
        self.co = '' #parece ser o mesmo que o campo complemento, mas foi criada uma variável específica mesmo assim
        self.decisao = ''
        self.divisao = ''
        self.im = ''
        self.requisitante = []
        self.protocolo = ''
        self.numero_pedido = ''
        self.data_prorrogacao = ''
        self.data_deposito = ''
        self.data_complementacao = ''
        self.dados_prioridade_unionista = ''
        self.data43_publicacao = ''
        self.data44_exame = ''
        self.data45_concessao = ''
        self.classificacao_int = ''
        self.classificacao_nac = ''
        self.titulo = ''
        self.resumo = ''
        self.pedido_original_adicao = ''
        self.pedido_original_divisao = ''
        self.dados_prioridade_interna = ''
        self.depositante = ''
        self.inventor = []
        self.titular = []
        self.procurador = []
        self.paises_designados = []
        self.data_inicio_fase_nacional = ''
        self.pct = ''
        self.wo = ''
        self.complemento = ''
        self.comentarios = ''
        self.lixo = [] #informações descartadas durante o processamento do .txt/.TXT
        self.processo = ''
        self.peticao = ''
        self.ultima_informacao = ''
        self.certificado_averbacao = ''
        self.cessionaria = ''
        self.cedente =''
        self.pais_cedente = ''
        self.pais_cessionaria = ''
        self.setor = ''
        self.cnpj_cpf = ''
        self.endereco_cessionaria = ''
        self.natureza_documento = ''
        self.objeto = ''
        self.moeda_pagamento = ''
        self.valor = ''
        self.forma_pagamento = ''
        self.prazo = ''
        self.resp_IR = ''
        self.servicos_despesas_isentas_averbacao = ''
        self.requerente = ''
        self.data_entrada = ''
        self.criador = ''
        self.linguagem = ''
        self.campo_aplicacao = ''
        self.tipo_programa = ''
        self.data_criacao = ''
        self.regime_guarda = ''
        self.data_peticao = ''
        self.li = ''
        self.la = ''
        self.fo = ''
        self.rc = ''
        self.nome_programa = ''

#Título das colunas do .csv
SEPARADOR = '|'
# FIRSTLINE = str('Número do pedido'+SEPARADOR+'Código de despacho'+SEPARADOR+'Base legal'+SEPARADOR+'Decisão'+SEPARADOR+'Divisão'+SEPARADOR+
#                 'Parte interessada'+SEPARADOR+'Requisitante'+SEPARADOR+'Número do protocolo (SINPI)'+SEPARADOR+'Data do depósito'+SEPARADOR+
#                 'Data de complementação'+SEPARADOR+'Dados da prioridade unionista'+SEPARADOR+'Data de publicação'+SEPARADOR+'Data de exame'+SEPARADOR+
#                 'Data de concessão'+SEPARADOR+'Classificação Internacional'+SEPARADOR+'Classificação Nacional'+SEPARADOR+'Título'+SEPARADOR+
#                 'Resumo'+SEPARADOR+'Pedido original (adição)'+SEPARADOR+'Pedido original (divisão)'+SEPARADOR+'Nome do depositante'+SEPARADOR+
#                 'Inventores'+SEPARADOR+'Titulares'+SEPARADOR+'Procuradores'+SEPARADOR+'Países designados'+SEPARADOR+
#                 'Data de início da fase nacional do PCT'+SEPARADOR+'PCT - número de depósito internacional'+SEPARADOR+
#                 'WO - número de publicação internacional'+SEPARADOR+'Complemento'+SEPARADOR+'Comentários'+SEPARADOR+'Requerente/Comentário'+SEPARADOR+
#                 'Data do Registro/Data da Prorrogação'+SEPARADOR+'Dados da prioridade interna (número e data de depósito)'+SEPARADOR+
#                 'Processo'+SEPARADOR+'Petição'+SEPARADOR+'Com última informação de'+SEPARADOR+'Certificado de averbação'+SEPARADOR+
#                 'Cessionária'+SEPARADOR+'Cedente'+SEPARADOR+'País da cedente'+SEPARADOR+'País da cessionária'+SEPARADOR+'Setor'+SEPARADOR+
#                 'CNPJ/CPF'+SEPARADOR+'Endereço cessionária'+SEPARADOR+'Natureza do documento'+SEPARADOR+'Objeto'+SEPARADOR+
#                 'Moeda de pagamento'+SEPARADOR+'Valor'+SEPARADOR+'Forma de pagamento'+SEPARADOR+'Prazo'+SEPARADOR+
#                 'Responsável pelo pagamento do IR'+SEPARADOR+'Serviços/Despesas isentas de averbação'+SEPARADOR+'Requerente'+SEPARADOR+
#                 'Data de entrada'+SEPARADOR+'Criador'+SEPARADOR+'Nome do programa'+SEPARADOR+'Linguagem'+SEPARADOR+'Campo de aplicação'+SEPARADOR+
#                 'Tipo de programa'+SEPARADOR+'Data de criação'+SEPARADOR+'Regime de guarda'+SEPARADOR+'Data da petição'+SEPARADOR+'(Li)'+SEPARADOR+
#                 '(La)'+SEPARADOR+'(Fo)'+SEPARADOR+'(Rc)'+SEPARADOR+'Lixo de processamento'+SEPARADOR+'RPI\n')
FIRSTLINE = str('Número do pedido'+SEPARADOR+'Classificação Internacional'+
                SEPARADOR+'Título'+SEPARADOR+'Resumo'+SEPARADOR+'Complemento'+
                SEPARADOR+'Comentários'+SEPARADOR+'RPI\n')

# os.chdir("D:\\rnunes\Documents\PycharmProjects\consultorias\RPI\\")
if len([f for f in os.listdir('./input') if (f.endswith('.txt') or f.endswith(
        '.TXT'))]) > 0:
    log = open(sys.argv[0].split('.')[0] + '.log', 'a', encoding='utf-8')
    log.write(time.strftime('%d/%m/%Y-%H:%M:%S - Starting execution of program: ' + sys.argv[0] + '\n'))

    csv_full = open('./output/full.csv', 'a+', encoding='utf-8')
    if csv_full.tell() == 0:
        csv_full.write(FIRSTLINE)

    # db = mysql.connector.connect(host='localhost',user='python',password='', database='revista')
    # cursor = db.cursor()
    # db_record = ('''INSERT INTO despachos (numero_pedido, codigo, Co, decisao, divisao, im, requisitantes, protocolo, data_deposito, data_complementacao,\
    #                     dados_prioridade_unionista, data43_publicacao, data44_exame, data45_concessao, classificacao_int, classificacao_nac, titulo, resumo, pedido_original_adicao,\
    #                     pedido_original_divisao, depositante, inventores, titulares, procuradores, paises, data_inicio_fase_nacional, pct, wo, complemento,\
    #                     comentarios, co_req, data_prorrogacao, dados_prioridade_interna, processo, peticao, ultima_informacao, certificado_averbacao, cessionaria, cedente, pais_cedente,\
    #                     pais_cessionaria, setor, cnpj_cpf, endereco_cessionaria, natureza_documento, objeto, moeda_pagamento, valor, forma_pagamento, prazo, resp_IR,\
    #                     servicos_despesas_isentas_averbacao, requerente, data_entrada, criador, nome_programa, linguagem, campo_aplicacao, tipo_programa, data_criacao,\
    #                     regime_guarda, data_peticao, li, la, fo, rc, lixo, rpi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
    #                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
    #                     %s, %s, %s)''')
    #
    # db_record2 = ('''INSERT INTO despachos_duplicados (numero_pedido, codigo, Co, decisao, divisao, im, requisitantes, protocolo, data_deposito, data_complementacao,\
    #                     dados_prioridade_unionista, data43_publicacao, data44_exame, data45_concessao, classificacao_int, classificacao_nac, titulo, resumo, pedido_original_adicao,\
    #                     pedido_original_divisao, depositante, inventores, titulares, procuradores, paises, data_inicio_fase_nacional, pct, wo, complemento,\
    #                     comentarios, co_req, data_prorrogacao, dados_prioridade_interna, processo, peticao, ultima_informacao, certificado_averbacao, cessionaria, cedente, pais_cedente,\
    #                     pais_cessionaria, setor, cnpj_cpf, endereco_cessionaria, natureza_documento, objeto, moeda_pagamento, valor, forma_pagamento, prazo, resp_IR,\
    #                     servicos_despesas_isentas_averbacao, requerente, data_entrada, criador, nome_programa, linguagem, campo_aplicacao, tipo_programa, data_criacao,\
    #                     regime_guarda, data_peticao, li, la, fo, rc, lixo, rpi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
    #                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
    #                     %s, %s, %s)''')

    for file in os.listdir('./input'):
        if file.endswith('.txt') or file.endswith('.TXT'):
            rpi = []
            last = ''
            erro_processamento = False
            log.write(time.strftime('%d/%m/%Y-%H:%M:%S  -  Parsing original file ' + file + '...\n'))
            f_out = open('./output/' + file[1:-4] + '_parsed.txt', 'w',
                         encoding='utf-8')
            for line in open('./input/' + file, 'r', encoding='latin-1'):
                line = line.lstrip(' ')
                novo_despacho = False #ainda não sei se é uma linha válida como despacho

                if re.match("\(Cd\)", line, 0):
                    f_out.write(line)
                    last = '(Cd)'
                    pointer_codigo = line[5:-1]     #Código de despacho
                    despacho = despachos(pointer_codigo)
                    despacho.rpi = file[1:-4]
                    novo_despacho = True

                elif re.match("\(Co\)", line, 0):
                    f_out.write(line)
                    last = '(Co)'
                    despacho.Co = line[5:-1]        #Base legal / Comentário

                elif re.match("\(co\)", line, 0):
                    f_out.write(line)
                    last = '(co)'
                    despacho.co = line[5:-1]        #Requerente / Comentário

                elif re.match('\(De\)', line, 0):
                    f_out.write(line)
                    last = '(De)'
                    despacho.decisao = line[5:-1]   #Decisão

                elif re.match("\(Di\)", line, 0):
                    f_out.write(line)
                    last = '(Di)'
                    despacho.divisao = line[5:-1]    #Divisão

                elif re.match('\(Im\)', line, 0):
                    f_out.write(line)
                    last = '(Im)'
                    despacho.im = line[5:-1]        #Interessado???

                elif re.match('\(Re\)', line, 0):                                   #Requisitante
                    f_out.write(line)
                    last = '(Re)'
                    despacho.requisitante = line.split(';', -1)
                    # ajusta a formatação do campo requisitante
                    despacho.requisitante[0] = str.strip(despacho.requisitante[0], '\(Re\) ') #Retira o código (Re) do início da linha
                    for i in range(1, len(despacho.requisitante)):
                        despacho.requisitante[i] = str.lstrip(despacho.requisitante[i], ' ')
                    # retirar o \n do final da linha
                    despacho.requisitante[len(despacho.requisitante) - 1] = str.rstrip(
                        despacho.requisitante[len(despacho.requisitante) - 1], '\n')

                elif re.match('\(00\)', line, 0):
                    f_out.write(line)
                    last = '(00)'
                    despacho.protocolo = line[5:-1] #Número do protocolo

                elif re.match('\(11\)', line, 0) and last != '(57)':    #Número do registro
                    f_out.write(line)
                    last = '(11)'
                    pointer = line.split()
                    for i in range (1,len(pointer)): despacho.numero_pedido += pointer[i]
                    if despacho.numero_pedido.find('-') != -1: despacho.numero_pedido = despacho.numero_pedido[0:-2]

                elif re.match('\(15\)', line, 0) and last != '(57)':    #Data do Registro/Data da Prorrogação
                    f_out.write(line)
                    last = '(15)'
                    despacho.data_prorrogacao = line[5:-1]

                elif re.match("\(21\)", line, 0):    #Número do pedido
                    f_out.write(line)
                    last = '(21)'
                    pointer = line.split()
                    for i in range (1,len(pointer)): despacho.numero_pedido += pointer[i]
                    if despacho.numero_pedido.find('-') != -1: despacho.numero_pedido = despacho.numero_pedido[0:-2]

                elif re.match("\(Np\)", line, 0):    #Número da petição
                    f_out.write(line)
                    last = '(Np)'
                    pointer = line.split()
                    for i in range(1, len(pointer)):
                        despacho.numero_pedido += pointer[i]
                    if len(despacho.numero_pedido) == 16 and despacho.numero_pedido.find('-') != -1:
                        despacho.numero_pedido = despacho.numero_pedido[
                                                                                                                           0:-2]

                elif re.match('\(22\)', line, 0):
                    f_out.write(line)
                    last = '(22)'
                    despacho.data_deposito = line[5:-1] #Data do depósito

                elif re.match('\(23\)', line, 0) and last != '(57)':
                    f_out.write(line)
                    last = '(23)'
                    despacho.data_complementacao = line[5:-1]   #Data da complementação da garantia da prioridade

                elif re.match('\(30\)', line, 0):
                    f_out.write(line)
                    last = '(30)'
                    despacho.dados_prioridade_unionista = line[5:-1]    #Dados da prioridade unionista (data de depósito, país, número)

                elif re.match('\(43\)', line, 0):
                    f_out.write(line)
                    last = '(43)'
                    despacho.data43_publicacao = line[5:-1] #Data de publicação do pedido & Data de publicação do desenho industrial (antes de ser examinado)

                elif re.match('\(44\)', line, 0) and last != '(57)':
                    f_out.write(line)
                    last = '(44)'
                    despacho.data44_exame = line[5:-1]      #Data de publicação do desenho industrial (depois de examinado, mas antes da concessão do registro)

                elif re.match('\(45\)', line, 0):
                    f_out.write(line)
                    last = '(45)'
                    despacho.data45_concessao = line[5:-1]  #Data da concessão da patente/certificado & Data de publicação do desenho industrial (após concessão)

                elif re.match('\(51\)', line, 0):
                    f_out.write(line)
                    last = '(51)'
                    despacho.classificacao_int = line[5:-1] #Classificação internacional

                elif re.match('\(52\)', line, 0) and last != '(57)':
                    f_out.write(line)
                    last = '(52)'
                    despacho.classificacao_nac = line[5:-1] #Classificação nacional

                elif re.match('\(53\)', line, 0):
                    f_out.write(line)
                    last = '(53)'
                    despacho.nome_programa = line[5:-1]            #Título

                elif re.match('\(54\)', line, 0):
                    f_out.write(line)
                    last = '(54)'
                    despacho.titulo = line[5:-1]            #Título

                elif re.match('\(57\)', line, 0):
                    f_out.write(line)
                    last = '(57)'
                    despacho.resumo = line[5:-1]            #Resumo

                elif re.match('\(61\)', line, 0):
                    f_out.write(line)
                    last = '(61)'
                    despacho.pedido_original_adicao = line[5:-1]    #Dados do pedido original do qual o presente é uma adição (número e data de depósito)

                elif re.match('\(62\)', line, 0):
                    f_out.write(line)
                    last = '(62)'
                    despacho.pedido_original_divisao = line[5:-1]   #Dados do pedido original do qual o presente é uma divisão (número e data de depósito)

                elif re.match('\(66\)', line, 0):
                    f_out.write(line)
                    last = '(66)'
                    despacho.dados_prioridade_interna = line[5:-1]   #Dados da prioridade interna (número e data de depósito)

                elif re.match('\(71\)', line, 0):
                    f_out.write(line)
                    last = '(71)'
                    despacho.depositante = line[5:-1]   #Nome do depositante

                elif re.match('\(72\)', line, 0):   #Nome do inventor
                    f_out.write(line)
                    last = '(72)'
                    despacho.inventor = line.split(';', -1)
                    # ajusta a formatação do campo inventor
                    despacho.inventor[0] = str.strip(despacho.inventor[0], '\(72\) ')
                    for i in range(1, len(despacho.inventor)):
                        despacho.inventor[i] = str.lstrip(despacho.inventor[i], ' ')
                    # retirar o \n do final da linha
                    despacho.inventor[len(despacho.inventor) - 1] = str.rstrip(despacho.inventor[len(despacho.inventor) - 1], '\n')

                elif re.match('\(73\)', line, 0):   #Nome do titular
                    f_out.write(line)
                    last = '(73)'
                    despacho.titular = line.split(';', -1)
                    # ajusta a formatação do campo titular
                    despacho.titular[0] = str.strip(despacho.titular[0], '\(73\) ')
                    for i in range(1, len(despacho.titular)):
                        despacho.titular[i] = str.lstrip(despacho.titular[i], ' ')
                    # retirar o \n do final da linha
                    despacho.titular[len(despacho.titular) - 1] = str.rstrip(despacho.titular[len(despacho.titular) - 1],
                                                                             '\n')
                elif re.match('\(74\)', line, 0):   #Nome do procurador
                    f_out.write(line)
                    last = '(74)'
                    despacho.procurador = line.split(';', -1)
                    # ajusta a formatação do campo procurador
                    despacho.procurador[0] = str.strip(despacho.procurador[0], '\(74\) ')
                    for i in range(1, len(despacho.procurador)):
                        despacho.procurador[i] = str.lstrip(despacho.procurador[i], ' ')
                    # retirar o \n do final da linha
                    despacho.procurador[len(despacho.procurador) - 1] = str.rstrip(despacho.procurador[len(despacho.procurador) - 1], '\n')

                elif re.match('\(81\)', line, 0):   #Países designados
                    f_out.write(line)
                    last = '(81)'
                    despacho.paises_designados = line.split(';', -1)
                    # ajusta a formatação
                    despacho.paises_designados[0] = str.strip(despacho.paises_designados[0], '\(81\) ')
                    for i in range(1, len(despacho.paises_designados)):
                        despacho.paises_designados[i] = str.lstrip(despacho.paises_designados[i], ' ')
                    # retirar o \n do final da linha
                    despacho.paises_designados[len(despacho.paises_designados) - 1] = str.rstrip(despacho.paises_designados[len(despacho.paises_designados) - 1], '\n')

                elif re.match('\(85\)', line, 0):
                    f_out.write(line)
                    last = '(85)'
                    despacho.data_inicio_fase_nacional = line[5:-1]     #Data do início da fase nacional

                elif re.match('\(86\)', line, 0):
                    f_out.write(line)
                    last = '(86)'
                    despacho.pct = line[5:-1]   #PCT = Número, idioma e data do depósito internacional

                elif re.match('\(87\)', line, 0):
                    f_out.write(line)
                    last = '(87)'
                    despacho.wo = line[5:-1]    #WO = Número, idioma e data de publicação internacional

                elif re.match('\(98\)', line, 0):
                    f_out.write(line)
                    last = '(98)'
                    despacho.complemento = line[5:-1]   #Complemento

                elif re.match('\(99\)', line, 0):
                    f_out.write(line)
                    last = '(99)'
                    despacho.comentarios = line[5:-1]   #Comentários / Desconhecido

                elif re.match('\(Np\)', line, 0):
                    f_out.write(line)
                    last = '(Np)'
                    despacho.processo = line[5:-1]   #Processo: (Contratos & Programa de computador)

                elif re.match('\(Pt\)', line, 0):
                    f_out.write(line)
                    last = '(Pt)'
                    despacho.peticao = line[5:-1]   #Petição: (Contratos & Programa de computador)

                elif re.match('\(Ui\)', line, 0):
                    f_out.write(line)
                    last = '(Ui)'
                    despacho.ultima_informacao = line[5:-1]   #Com última informação de: (Contratos)

                elif re.match('\(Ca\)', line, 0):
                    f_out.write(line)
                    last = '(Ca)'
                    despacho.certificado_averbacao = line[5:-1]   #Certificado de averbação: (Contratos)

                elif re.match('\(Cs\)', line, 0):
                    f_out.write(line)
                    last = '(Cs)'
                    despacho.cessionaria = line[5:-1]   #Cesseionária: (Contratos)

                elif re.match('\(Ce\)', line, 0):
                    f_out.write(line)
                    last = '(Ce)'
                    despacho.cedente = line[5:-1]   #Cedente: (Contratos)

                elif re.match('\(Pe\)', line, 0):
                    f_out.write(line)
                    last = '(Pe)'
                    despacho.pais_cedente = line[5:-1]   #País da cedente: (Contratos)

                elif re.match('\(Ps\)', line, 0):
                    f_out.write(line)
                    last = '(Ps)'
                    despacho.pais_cessionaria = line[5:-1]   #País da cessionária: (Contratos)

                elif re.match('\(Se\)', line, 0):
                    f_out.write(line)
                    last = '(Se)'
                    despacho.setor = line[5:-1]   #Setor: (Contratos)

                elif re.match('\(Is\)', line, 0):
                    f_out.write(line)
                    last = '(Is)'
                    despacho.cnpj_cpf = line[5:-1]   #CNPF/CPF: (Contratos)

                elif re.match('\(Es\)', line, 0):
                    f_out.write(line)
                    last = '(Es)'
                    despacho.endereco_cessionaria = line[5:-1]   #Endereço cessionária: (Contratos)

                elif re.match('\(Nd\)', line, 0):
                    f_out.write(line)
                    last = '(Nd)'
                    despacho.natureza_documento = line[5:-1]   #Natureza do documento: (Contratos)

                elif re.match('\(Ob\)', line, 0):
                    f_out.write(line)
                    last = '(Ob)'
                    despacho.objeto = line[5:-1]   #Objeto: (Contratos)

                elif re.match('\(Mo\)', line, 0):
                    f_out.write(line)
                    last = '(Mo)'
                    despacho.moeda_pagamento = line[5:-1]   #Moeda de pagamento: (Contratos)

                elif re.match('\(Va\)', line, 0) or re.match(' \(Va\)', line, 0): #tratamento do arquivo 1136.txt, linha de despacho começando com espaço.
                    f_out.write(line)
                    last = '(Va)'
                    despacho.valor = line[5:-1]   #Valor: (Contratos)

                elif re.match('\(Pg\)', line, 0):
                    f_out.write(line)
                    last = '(Pg)'
                    despacho.forma_pagamemto = line[5:-1]   #Forma de pagamento: (Contratos)

                elif re.match('\(Pz\)', line, 0):
                    f_out.write(line)
                    last = '(Pz)'
                    despacho.prazo = line[5:-1]   #Prazo: (Contratos)

                elif re.match('\(Rp\)', line, 0):
                    f_out.write(line)
                    last = '(Rp)'
                    despacho.resp_IR = line[5:-1]   #Responsável pelo pagamento do Imposto de Renda: (Contratos)

                elif re.match('\(Ia\)', line, 0):
                    f_out.write(line)
                    last = '(Ia)'
                    despacho.servicos_despesas_isentas_averbacao = line[5:-1]   #Serviços/Despesas isentas de averbação: (Contratos)

                elif re.match('\(Cp\)', line, 0):
                    f_out.write(line)
                    last = '(Cp)'
                    despacho.complemento += ";"+line[5:-1]   #Complemento: (Contratos)

                elif re.match('\(Rq\)', line, 0):
                    f_out.write(line)
                    last = '(Rq)'
                    despacho.requerente = line[5:-1]   #Requerente: (Contratos)

                # elif re.match('\(De\)', line, 0):
                #     f_out.write(line)
                #     last = '(De)'
                #     despacho.data_entrada = line[5:-1]   #Data de entrada: (Contratos)

                elif re.match('\(Cr\)', line, 0):
                    f_out.write(line)
                    last = '(Cr)'
                    despacho.criador = line[5:-1]   #Criador: (Programa de computador)

                elif re.match('\(Lg\)', line, 0):
                    f_out.write(line)
                    last = '(Lg)'
                    despacho.linguagem = line[5:-1]   #Linguagem: (Programa de computador)

                elif re.match('\(Cp\)', line, 0):
                    f_out.write(line)
                    last = '(Cp)'
                    despacho.campo_aplicacao = line[5:-1]   #Campo de aplicação: (Programa de computador)

                elif re.match('\(Tp\)', line, 0):
                    f_out.write(line)
                    last = '(Tp)'
                    despacho.tipo_programa = line[5:-1]   #Tipo de programa: (Programa de computador)

                elif re.match('\(Dl\)', line, 0):
                    f_out.write(line)
                    last = '(Dl)'
                    despacho.data_criacao = line[5:-1]   #Data da criação: (Programa de computador)

                elif re.match('\(Rg\)', line, 0):
                    f_out.write(line)
                    last = '(Rg)'
                    despacho.regime_guarda = line[5:-1]   #Regime de guarda: (Programa de computador)

                elif re.match('\(Dp\)', line, 0):
                    f_out.write(line)
                    last = '(Dp)'
                    despacho.data_peticao = line[5:-1]   #Data da petição: (Programa de computador)

                elif re.match('\(Li\)', line, 0):
                    f_out.write(line)
                    last = '(Li)'
                    despacho.li = line[5:-1]   #???: (Programa de computador)

                elif re.match('\(La\)', line, 0):
                    f_out.write(line)
                    last = '(La)'
                    despacho.la = line[5:-1]   #???: (Programa de computador)

                elif re.match('\(Fo\)', line, 0):
                    f_out.write(line)
                    last = '(Fo)'
                    despacho.fo = line[5:-1]   #???: (Programa de computador)

                elif re.match('\(Rc\)', line, 0):
                    f_out.write(line)
                    last = '(Rc)'
                    despacho.rc = line[5:-1]   #???: (Programa de computador)

                else:
                    if last == '(21)': #Número do pedido
                        f_out.write(line)
                        despacho.lixo.append('(21)'+line[0:-1])
                    elif last == '(22)': #Data de Depósito
                        f_out.write(line)
                        despacho.lixo.append('(22)'+line[0:-1])
                    elif last == '(30)': #Prioridade unionista
                        f_out.write(line)
                        despacho.dados_prioridade_unionista += ' ' + line[0:-1]
                    elif last == '(45)': #Data de concessão
                        f_out.write(line)
                        despacho.lixo.append('(45)'+line[0:-1])
                    elif last == '(51)': #Resumo
                        f_out.write(line)
                        despacho.classificacao_int += line[0:-1]
                    elif last == '(54)': #Resumo
                        f_out.write(line)
                        despacho.titulo += line[0:-1]
                    elif last == '(57)': #Resumo
                        f_out.write(line)
                        despacho.resumo += line[0:-1]
                    elif last == '(71)':  # Depositante
                        f_out.write(line)
                        despacho.lixo.append('(71)' + line[0:-1])
                    elif last == '(72)':  # Inventor
                        f_out.write(line)
                        despacho.lixo.append('(72)' + line[0:-1])
                    elif last == '(73)':  # Titular
                        f_out.write(line)
                        despacho.lixo.append('(73)' + line[0:-1])
                    elif last == '(74)':  # Procurador
                        f_out.write(line)
                        despacho.lixo.append('(74)'+line[0:-1])
                    elif last == '(86)':  # PCT
                        f_out.write(line)
                        despacho.pct += line[0:-1]
                    elif last == '(87)':  # WO
                        f_out.write(line)
                        despacho.wo += line[0:-1]
                    elif last == '(Pz)': #Prazo
                        f_out.write(line)
                        despacho.prazo += line[0:-1]
                    elif last == '(Va)': #Valor
                        f_out.write(line)
                        despacho.valor += line[0:-1]
                    elif last == '(Ob)': #Objeto
                        f_out.write(line)
                        despacho.objeto += line[0:-1]
                    elif last == '(Pg)': #Forma de pagamento
                        f_out.write(line)
                        despacho.forma_pagamemto += line[0:-1]
                    elif last == '(Rc)': #Forma de pagamento
                        f_out.write(line)
                        despacho.rc += line[0:-1]
                    elif last == '(Cr)': #Criador
                        f_out.write(line)
                        despacho.lixo.append('(Cr)'+line[0:-1])
                    elif last == '(De)': #Decisão
                        f_out.write(line)
                        despacho.decisao += line[0:-1]
                    elif last == '(Co)': #Base legal
                        f_out.write(line)
                        despacho.Co += ';'+line[0:-1]
                    elif last == '(co)': #Base legal
                        f_out.write(line)
                        despacho.co += ';'+line[0:-1]
                    elif last == '(Ia)': #Base legal
                        f_out.write(line)
                        despacho.servicos_despesas_isentas_averbacao += line[0:-1]
                    elif last == '(Nd)': #Base legal
                        f_out.write(line)
                        despacho.natureza_documento += line[0:-1]
                    elif last == '(Cp)': #Complemento
                        f_out.write(line)
                        despacho.complemento += line[0:-1]
                    elif last == '(Cd)': #Base legal
                        f_out.write(line)
                        despacho.lixo.append('(Cd)' + line[0:-1])
                    elif last == '(Np)': #Base legal
                        f_out.write(line)
                        despacho.lixo.append('(Np)' + line[0:-1])
                    elif last == '(Ca)': #Certificado de averbação
                        f_out.write(line)
                        despacho.lixo.append('(Ca)' + line[0:-1])
                    elif last == '(Se)': #Setor
                        f_out.write(line)
                        despacho.lixo.append('(Se)' + line[0:-1])
                    elif last == '(Ui)': #com última informação de
                        f_out.write(line)
                        despacho.lixo.append('(Ui)' + line[0:-1])
                    elif last == '(Re)': #Requisitante
                        f_out.write(line)
                        despacho.lixo.append('(Re)' + line[0:-1])
                    elif last == '(Cs)': #Requisitante
                        f_out.write(line)
                        despacho.lixo.append('(Cs)' + line[0:-1])
                    elif last == '(Rg)': #Requisitante
                        f_out.write(line)
                        despacho.lixo.append('(Rg)' + line[0:-1])
                    elif last == '(Rp)': #Requisitante
                        f_out.write(line)
                        despacho.lixo.append('(Rp)' + line[0:-1])
                    elif last == '(Rq)': #Requisitante
                        f_out.write(line)
                        despacho.lixo.append('(Rq)' + line[0:-1])
                    elif last == '(Ce)': #Requisitante
                        f_out.write(line)
                        despacho.lixo.append('(Ce)' + line[0:-1])
                    elif (last != '') and (line.find(file[1:-4]) == -1) and (line.find('|') == -1) and (not(re.match('\(',line,0))) and (line != '\n'):
                        print('Existe uma linha desconhecida no arquivo '+file+', ela não foi processada')
                        log.write(time.strftime('%d/%m/%Y-%H:%M:%S  -  There is an unknown line in the file ' + file + ' the line was skipped!\n'))
                        erro_processamento = True
                if novo_despacho:
                    rpi.append(despacho) # insere o registro no final do vetor
            f_out.close()
            log.write(time.strftime('%d/%m/%Y-%H:%M:%S  -  Parse finished on file ' + file + '. And file ' + './output/' + file[1:-4] +
                                    '_parsed.txt has been saved.\n'))
            log.write(time.strftime('%d/%m/%Y-%H:%M:%S  -  Saving .csv for the files ' + file + '...\n'))
            csv_out = open('./output/' + file[1:-4] + '.csv', 'w',
                           encoding='utf-8')
            csv_out.write(FIRSTLINE)

            #Inserção dos despachos, separados pelo SEPARADOR, no arquivo .csv
            for i in range (0,len(rpi)):
                requisitantes, inventores, titulares, procuradores, paises, lixo = '','','','','',''
                for j in range (0,len(rpi[i].requisitante)):
                    requisitantes = requisitantes + rpi[i].requisitante[j] + ';'
                for j in range (0,len(rpi[i].inventor)):
                    inventores = inventores + rpi[i].inventor[j] + ';'
                for j in range (0,len(rpi[i].titular)):
                    titulares = titulares + rpi[i].titular[j] + ';'
                for j in range (0,len(rpi[i].procurador)):
                    procuradores = procuradores + rpi[i].procurador[j] + ';'
                for j in range (0,len(rpi[i].paises_designados)):
                    paises = paises + rpi[i].paises_designados[j] + ';'
                for j in range (0,len(rpi[i].lixo)):
                    lixo = lixo + rpi[i].lixo[j] + ';'

                # tuple = str(rpi[i].numero_pedido+SEPARADOR+rpi[i].codigo+SEPARADOR+rpi[i].Co+SEPARADOR+rpi[i].decisao+SEPARADOR+rpi[i].divisao+SEPARADOR+rpi[i].im+SEPARADOR+\
                #         requisitantes[0:-1]+SEPARADOR+rpi[i].protocolo+SEPARADOR+rpi[i].data_deposito+SEPARADOR+\
                #         rpi[i].data_complementacao+SEPARADOR+rpi[i].dados_prioridade_unionista+SEPARADOR+rpi[i].data43_publicacao+SEPARADOR+\
                #         rpi[i].data44_exame+SEPARADOR+rpi[i].data45_concessao+SEPARADOR+rpi[i].classificacao_int+SEPARADOR+rpi[i].classificacao_nac+SEPARADOR+\
                #         rpi[i].titulo+SEPARADOR+rpi[i].resumo+SEPARADOR+rpi[i].pedido_original_adicao+SEPARADOR+rpi[i].pedido_original_divisao+SEPARADOR+\
                #         rpi[i].depositante+SEPARADOR+inventores[0:-1]+SEPARADOR+titulares[0:-1]+SEPARADOR+procuradores[0:-1]+SEPARADOR+paises[0:-1]+SEPARADOR+\
                #         rpi[i].data_inicio_fase_nacional+SEPARADOR+rpi[i].pct+SEPARADOR+rpi[i].wo+SEPARADOR+rpi[i].complemento+SEPARADOR+rpi[i].comentarios+SEPARADOR+\
                #         rpi[i].co+SEPARADOR+rpi[i].data_prorrogacao+SEPARADOR+rpi[i].dados_prioridade_interna+SEPARADOR+rpi[i].processo+SEPARADOR+rpi[i].peticao+SEPARADOR+\
                #         rpi[i].ultima_informacao+SEPARADOR+rpi[i].certificado_averbacao+SEPARADOR+rpi[i].cessionaria+SEPARADOR+rpi[i].cedente+SEPARADOR+rpi[i].pais_cedente+SEPARADOR+\
                #         rpi[i].pais_cessionaria+SEPARADOR+rpi[i].setor+SEPARADOR+rpi[i].cnpj_cpf+SEPARADOR+rpi[i].endereco_cessionaria+SEPARADOR+rpi[i].natureza_documento+SEPARADOR+\
                #         rpi[i].objeto+SEPARADOR+rpi[i].moeda_pagamento+SEPARADOR+rpi[i].valor+SEPARADOR+rpi[i].forma_pagamento+SEPARADOR+rpi[i].prazo+SEPARADOR+rpi[i].resp_IR+SEPARADOR+\
                #         rpi[i].servicos_despesas_isentas_averbacao+SEPARADOR+rpi[i].requerente+SEPARADOR+rpi[i].data_entrada+SEPARADOR+rpi[i].criador+SEPARADOR+\
                #         rpi[i].nome_programa+SEPARADOR+rpi[i].linguagem+SEPARADOR+rpi[i].campo_aplicacao+SEPARADOR+rpi[i].tipo_programa+SEPARADOR+rpi[i].data_criacao+SEPARADOR+rpi[i].regime_guarda+SEPARADOR+\
                #         rpi[i].data_peticao+SEPARADOR+rpi[i].li+SEPARADOR+rpi[i].la+SEPARADOR+rpi[i].fo+SEPARADOR+rpi[i].rc+SEPARADOR+lixo[0:-1]+SEPARADOR+rpi[i].rpi+'\n')

                tuple = str(rpi[i].numero_pedido+SEPARADOR+rpi[i].classificacao_int+SEPARADOR+rpi[i].titulo+SEPARADOR+rpi[i].resumo+SEPARADOR+rpi[i].complemento+SEPARADOR+rpi[i].comentarios+SEPARADOR+\
                        rpi[i].rpi+'\n')

                if rpi[i].classificacao_int != '' and rpi[i].titulo != '' \
                        and rpi[i].resumo != '':
                    csv_out.write(tuple)
                    csv_full.write(tuple)

                # db_data = (rpi[i].numero_pedido, rpi[i].codigo, rpi[i].Co, rpi[i].decisao, rpi[i].divisao, rpi[i].im, requisitantes[0:-1], rpi[i].protocolo, rpi[i].data_deposito,\
                #            rpi[i].data_complementacao, rpi[i].dados_prioridade_unionista, rpi[i].data43_publicacao, rpi[i].data44_exame, rpi[i].data45_concessao, rpi[i].classificacao_int,\
                #            rpi[i].classificacao_nac, rpi[i].titulo, rpi[i].resumo, rpi[i].pedido_original_adicao, rpi[i].pedido_original_divisao, rpi[i].depositante, inventores[0:-1],\
                #            titulares[0:-1], procuradores[0:-1], paises[0:-1], rpi[i].data_inicio_fase_nacional, rpi[i].pct, rpi[i].wo, rpi[i].complemento, rpi[i].comentarios,\
                #            rpi[i].co, rpi[i].data_prorrogacao, rpi[i].dados_prioridade_interna, rpi[i].processo, rpi[i].peticao, rpi[i].ultima_informacao, rpi[i].certificado_averbacao,\
                #            rpi[i].cessionaria, rpi[i].cedente, rpi[i].pais_cedente, rpi[i].pais_cessionaria, rpi[i].setor, rpi[i].cnpj_cpf, rpi[i].endereco_cessionaria,\
                #            rpi[i].natureza_documento, rpi[i].objeto, rpi[i].moeda_pagamento, rpi[i].valor, rpi[i].forma_pagamento, rpi[i].prazo, rpi[i].resp_IR,\
                #            rpi[i].servicos_despesas_isentas_averbacao, rpi[i].requerente, rpi[i].data_entrada, rpi[i].criador, rpi[i].nome_programa, rpi[i].linguagem,\
                #            rpi[i].campo_aplicacao, rpi[i].tipo_programa, rpi[i].data_criacao, rpi[i].regime_guarda, rpi[i].data_peticao, rpi[i].li, rpi[i].la, rpi[i].fo, rpi[i].rc,\
                #            lixo[0:-1], rpi[i].rpi)
                # try:
                #     cursor.execute(db_record, db_data)
                # except:
                #     cursor.execute(db_record2, db_data)
                # #print(tuple)
            csv_out.close()

            #Relatório final sobre a quantidade de despachos processados em cada RPI
            print(str(len(rpi)) + ' despachos foram processados na RPI no.' + file[1:-4])
            log.write(time.strftime('%d/%m/%Y-%H:%M:%S  -  ' + str(len(rpi)) + ' dispatchs were parsed on RPI no.' + file[1:-4] + '\n'))
            if not(erro_processamento): os.remove('./input/'+file)

    # db.commit()
    # cursor.close()
    # db.close()
    csv_full.close()

    log.write(time.strftime('%d/%m/%Y'+' - '+'%H:%M:%S'))
    log.write(time.strftime('%d/%m/%Y-%H:%M:%S  -  All .txt files were parsed, execution finished.\n'))
    log.close()
else:
    print('No .txt or .TXT. files found on input directory. Nothing done!\n')