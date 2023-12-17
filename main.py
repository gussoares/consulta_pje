# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import consulta_autenticada, consulta_publica, baixa, baixa_publica, quebra_captcha_pje, tempo, auxiliar, conexao


from consulta_autenticada import consulta, consulta_expandida
from consulta_publica import consulta_publica, pega_id
from baixa_publica import pega_sentenca_cnj

from baixa import pega_sentenca
import requests
import json


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    username = # AQUI VAI O USUÁRIO
    password = # AQUI VAI A SENHA
    exemplo = # UM EXEMPLO '1000238-08.2022.5.02.0371'
    #print([i for i in consulta(exemplo)['itensProcesso'] if i['titulo'].startswith('Julgado')])# if i['titulo'] == "Sentença" and i['usuarioJuntada']=='GUSTAVO SCHILD SOARES'], "\n############################################")
    print([i for i in consulta(exemplo)['itensProcesso']]) # if i['titulo'] == "Sentença" and i['usuarioJuntada']=='GUSTAVO SCHILD SOARES']) #, "\n############################################")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx")
    print(consulta_publica(pega_id(exemplo)).json())

    #print(consulta(pega_id(exemplo))[0])
    #print(len(consulta_expandida()))
    print("YYYYYYYYYYYYYYYYYYYYYYYYYYYyy")

    #import os
    #print(os.getcwd())
    #print(os.path.isdir())
    #pega_sentenca(exemplo)
    #pega_sentenca_cnj(exemplo)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/