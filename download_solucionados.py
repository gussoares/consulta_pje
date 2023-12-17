import pandas as pd
import os
from glob import glob
from baixa import pega_sentenca
from baixa import pega_sentenca
from baixa_publica import pega_sentenca_cnj


# TESTE DOWNLOADS DE SENTENÇAS A PARTIR DE ARQUIVO CSV DE PROCESSOS SOLUCIONADOS

#print(os.getcwd())

destino = '/mnt/sdb1/trt2'
def filtra_e_pega(x):
    try:
        if len(x)==25:
            pega_sentenca_cnj(x, destino) #pega_sentenca(x)
            return x

    except:
        print('erro')


arquivo = '(B).csv' # já foi D, e (F erro) A
caminho = '/home/gustavo/Downloads/B.4.1_-_Com_Exame_de_Mérito/'
origem = glob(caminho + arquivo)
#print(destino)
data = pd.read_csv(origem[0]) #, chunksize = 100000)
#print(data.columns)
#
print(data['Magistrado'])

data['Magistrado'].fillna(method='ffill', inplace=True)
print(data['Magistrado'])
###data.filter(data['Número do Processo'])
#data1[data1['Magistrado']=='GUSTAVO SCHILD SOARES']

data1 = data[data['Magistrado']=='GUSTAVO SCHILD SOARES']
data['Número do Processo'].apply(lambda x: filtra_e_pega(x))
'''for p in data1['Número do Processo'][:-1]:
    print(p)
    pega_sentenca(data1['Número do Processo'][0])'''
