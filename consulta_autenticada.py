# consultas às APIs do PJe - em regra retornam um json ou valor de uma chave
import requests
import datetime


from conexao import verifica_autenticacao
from tempo import hoje, amanha

# CONSULTAS PÚBLICAS MEDIANTE AUTENTICAÇÃO SIMPLES POR USUÁRIO E SENHA
def pega_id(numero_processo_cnj, tribunal = '2', instancia = '1'):
    headers = {'x-grau-instancia' : str(instancia)}
    url = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/dadosbasicos/" + numero_processo_cnj
    resposta = requests.get(url, headers=headers)

    return str(resposta.json()[0]['id'])

# CONSULTAS AUTENTICADAS
def consulta_autenticada(numero_processo_id, autenticacao = None, tribunal = '2', instancia = '1'):
    autenticacao = verifica_autenticacao(autenticacao)
    headers = {'Authorization': 'Bearer {}'.format(autenticacao), 'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br', 'Content-type': 'application/json','x-grau-instancia' : str(instancia)}
    url_consulta = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/" + str(numero_processo_id)
    resposta = requests.get(url_consulta, headers=headers)
    return resposta

def consulta(numero_processo, autenticacao = None, tribunal = '2', instancia = '1'):
    # um filtro bem simples para separar numeração CNJ da id
    numero_processo = str(numero_processo)
    if len(numero_processo) < 10:
        numero_processo_id = numero_processo
    else:
        numero_processo_id = pega_id(numero_processo)
    autenticacao = verifica_autenticacao(autenticacao)
    resultado_consulta = consulta_autenticada(numero_processo_id, autenticacao, tribunal = tribunal, instancia = instancia)
    return resultado_consulta.json()

def orgaos_julgadores(autenticacao, tribunal = '2', instancia = '1'):
    autenticacao = verifica_autenticacao(autenticacao)
    headers = {'Authorization': 'Bearer {}'.format(autenticacao),  'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br', 'Content-type': 'application/json','x-grau-instancia' : str(instancia)}
    url_orgaos = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/orgaosjulgadores?somenteOJCs=true"
    resposta = requests.get(url_orgaos, headers=headers)
    return resposta.json()

def consulta_pauta(data, autenticacao = None, tribunal = '2', instancia = '1', pagina = '1', tamanhoPagina = "20", ordenacaoColuna = 'undefined', ordenacaoCrescente = 'undefined', idOj = '63'):
    # verifica se já tem access token
    autenticacao = verifica_autenticacao(autenticacao)
    # busca a pauta do dia
    headers = {'Authorization': 'Bearer {}'.format(autenticacao),  'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br', 'Content-type': 'application/json','x-grau-instancia' : str(instancia)}
    url_pauta = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/audiencias?pagina=" + pagina + '&tamanhoPagina=' + tamanhoPagina + '&ordenacaoColuna=' + ordenacaoColuna + '&ordenacaoCrescentes=' + ordenacaoCrescente + "&idOj=" + idOj + '&data=' + data
    resultado = requests.get(url_pauta, headers=headers)
    return resultado.json()

def consulta_terceiros(cnpj_parte = "",
                       classe_processo = '326' or '387',
                       data_inicio = hoje,
                       data_fim = hoje,
                       autenticacao = None,
                       tribunal='2',
                       instancia='1',
                       pagina='1',
                       tamanhoPagina="20",
                       ordenacaoColuna='undefined',
                       ordenacaoCrescente='undefined'):
    autenticacao = verifica_autenticacao(autenticacao)
    headers = {'Authorization': 'Bearer {}'.format(autenticacao), 'Accept': 'application/json, text/plain, */*',
               'Accept-Encoding': 'gzip, deflate, br', 'Content-type': 'application/json',
               'x-grau-instancia': str(instancia)}
    uri = "https://pje.trt" + str(
        tribunal) + ".jus.br/pje-consulta-api/api/processos/consultaterceiros?pagina=" + pagina + '&tamanhoPagina=' + tamanhoPagina + '&ordenacaoColuna=' + ordenacaoColuna + '&ordenacaoCrescente=' + ordenacaoCrescente + '&cnpjParte=' + cnpj_parte + '&idClasseProcesso=' + classe_processo + '&dtDistribuicaoInicio=' + data_inicio + 'T00:00:00&' + 'dtDistribuicaoFim=' + data_fim + 'T23:59:59'
    resultado = requests.get(uri, headers=headers)
    return resultado

def consulta_expandida(autenticacao = None, cnpj_parte='', classe_processo='326' or '387',
                        data_inicio=hoje, data_fim=hoje, tribunal='2', instancia='1',
                        pagina='1', tamanhoPagina="20", ordenacaoColuna='undefined',
                        ordenacaoCrescente='undefined'):
    autenticacao = verifica_autenticacao(autenticacao)
    inicio = datetime.date.fromisoformat(data_inicio)
    fim = datetime.date.fromisoformat(data_fim)
    diferenca = fim - inicio
    resultado = []

    quantidade_periodos = diferenca.days // 180 + 1

    for periodo in range(quantidade_periodos):
        data_inicio1 = inicio + datetime.timedelta((periodo) * 180)
        data_fim1 = inicio + datetime.timedelta((periodo + 1) * 180)

        data_inicio1 = str(data_inicio1)
        data_fim1 = str(data_fim1)

        c = consulta_terceiros(cnpj_parte, classe_processo, data_inicio1, data_fim1, autenticacao, tribunal=tribunal,
                               instancia=instancia, pagina=pagina, tamanhoPagina=tamanhoPagina,
                               ordenacaoColuna=ordenacaoColuna, ordenacaoCrescente=ordenacaoCrescente).json()
        #print(c)
        for p in range(c["qtdPaginas"]):
            if 'resultado' in consulta_terceiros(cnpj_parte, classe_processo, data_inicio1, data_fim1, autenticacao,
                                                 tribunal=tribunal, instancia=instancia, pagina=str(p),
                                                 tamanhoPagina=tamanhoPagina, ordenacaoColuna=ordenacaoColuna,
                                                 ordenacaoCrescente=ordenacaoCrescente).json().keys():
                resultado.extend(consulta_terceiros(cnpj_parte, classe_processo, data_inicio1, data_fim1, autenticacao,
                                                    tribunal=tribunal, instancia=instancia, pagina=str(p),
                                                    tamanhoPagina=tamanhoPagina, ordenacaoColuna=ordenacaoColuna,
                                                    ordenacaoCrescente=ordenacaoCrescente).json()['resultado'])

    return resultado
