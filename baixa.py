# realiza dowloads de arquivos pela API do PJe
import requests
import json
from conexao import verifica_autenticacao
from tempo import pega_data
from consulta_autenticada import pega_id, consulta_autenticada, consulta_pauta

# DOWNLOADS DE ARQUIVOS PDF
def baixa_pdf_pje(numero_processo_id, numero_documento_id, autenticacao = None, tribunal = '2', instancia = '1'):
    autenticacao = verifica_autenticacao(autenticacao)
    headers = {'Authorization': 'Bearer {}'.format(autenticacao),  'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br', 'Content-type': 'application/json','x-grau-instancia' : str(instancia)}
    url_documento = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/" + str(numero_processo_id) + "/documentos/" + str(numero_documento_id)
    resultado = requests.get(url_documento, headers=headers, stream = True)
    nome_do_arquivo = str(numero_processo_id) + "_" + str(numero_documento_id)
    # se pegou o PDF, salva o arquivo
    if resultado.content.startswith(b'%PDF'):
        with open(f'{nome_do_arquivo}.pdf', 'wb') as f:
            f.write(resultado.content)
    # se não deu certo, repete tudo
    else:
        baixa_pdf_pje(numero_processo_id, numero_documento_id, autenticacao, tribunal, instancia)

# usa a função consulta_andamentos_pje para obter os itensProcesso
# se o título de itensProcesso é sentença, descobre o número do documento e aplica a usa a função baixa_docs_pje
def pega_sentenca_id(numero_processo_id, autenticacao = None, tribunal = '2', instancia = '1'):
    headers = {'Authorization': 'Bearer {}'.format(autenticacao),  'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br', 'Content-type': 'application/json','x-grau-instancia' : str(instancia)}
    autenticacao = verifica_autenticacao(autenticacao)
    consulta = consulta_autenticada(numero_processo_id, autenticacao,  tribunal, instancia)
    for item in consulta.json()['itensProcesso']:
        if item['titulo']=='Sentença':
            if item['tipoConteudo']== 'PDF':
                numero_documento_id = str(item['id'])
                print(numero_documento_id + " - " + item['titulo'])
                baixa_pdf_pje(numero_processo_id, numero_documento_id, autenticacao, tribunal, instancia)

def pega_sentenca(numero_processo_cnj, autenticacao = None, tribunal = '2', instancia = '1'):
    autenticacao = verifica_autenticacao(autenticacao)
    headers = {'Authorization': 'Bearer {}'.format(autenticacao),  'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br', 'Content-type': 'application/json','x-grau-instancia' : str(instancia)}
    numero_processo_id = pega_id(numero_processo_cnj)

    consulta = consulta_autenticada(numero_processo_id, autenticacao,  tribunal, instancia)
    for item in consulta.json()['itensProcesso']:
        if item['titulo']== "Sentença" and i['usuarioJuntada']=='GUSTAVO SCHILD SOARES':
            if item['tipoConteudo']== 'PDF':
                numero_documento_id = str(item['id'])
                print(numero_documento_id + " - " + item['titulo'])

                url_documento = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/" + str(numero_processo_id) + "/documentos/" + str(numero_documento_id)
                resultado = requests.get(url_documento, headers=headers, stream = True)
                nome_usuario = item['usuarioJuntada'].replace(" ", '_')
                print(nome_usuario)
                import os
                if os.path.isdir(nome_usuario):
                    pass
                else:
                    os.mkdir(nome_usuario)

                nome_do_arquivo = str(numero_processo_cnj) +"_" + str(numero_processo_id) + "_" + str(item['idUnicoDocumento']) + "_" + str(numero_documento_id)
                if resultado.content.startswith(b'%PDF'):
                    print(os.getcwd())
                    with open(f'{nome_usuario}/{nome_do_arquivo}.pdf', 'wb') as f:
                        f.write(resultado.content)

                else:
                    print('erro')


def baixa_integra_pje_autenticado(numero_processo_id, autenticacao = None, pasta_destino="", tribunal='2', instancia='1'):
    # verifica se já tem access token
    autenticacao = verifica_autenticacao(autenticacao)
    # request para fazer download
    headers = {'Authorization': 'Bearer {}'.format(autenticacao), 'Accept': 'application/json, text/plain, */*',
               'Accept-Encoding': 'gzip, deflate, br', 'Content-type': 'application/json',
               'x-grau-instancia': str(instancia)}
    url_integra  = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/" + str(
        numero_processo_id) + '/integra'
    resultado = requests.get(url_integra, headers=headers)
    # verifica se foi passada uma pasta_destino e, se sim, verifica se tem barra, adicionando, se necessário
    if len(pasta_destino) > 0 and pasta_destino[-1] != '/':
        pasta_destino += '/'
    nome_do_arquivo = pasta_destino + str(numero_processo_id) + "_" + 'integra'  # arquivo destino
    print(nome_do_arquivo)
    # salva
    if resultado.content.startswith(b'%PDF'):  # verifica se o request deu certo e veio o pdf
        with open(f'{nome_do_arquivo}.pdf', 'wb') as f:
            f.write(resultado.content)
    else:  # se não deu certo, chama de novo recursivamente
        baixa_integra_pje_autenticado(numero_processo_id,
                                      autenticacao,
                                      pasta_destino = pasta_destino,
                                      tribunal = tribunal,
                                      instancia = instancia)


def download_pauta(data, autenticacao = None, pasta_destino="", tribunal='2', instancia='1', pagina='1', tamanhoPagina="20",
                   ordenacaoColuna='undefined', ordenacaoCrescente='undefined', idOj='63'):
    autenticacao = verifica_autenticacao(autenticacao)
    pauta = consulta_pauta(data=data, autenticacao=autenticacao, tribunal=tribunal, instancia=instancia, pagina=pagina,
                           tamanhoPagina=tamanhoPagina, ordenacaoColuna=ordenacaoColuna,
                           ordenacaoCrescente=ordenacaoCrescente, idOj=idOj)
    for p in pauta.json()['resultado']:
        numero_processo_id = pega_id(p['numeroProcesso'], tribunal=tribunal, instancia=instancia)
        baixa_integra_pje_autenticado(numero_processo_id, autenticacao, pasta_destino=pasta_destino, tribunal=tribunal,
                                      instancia=instancia)


