import requests
import json

username = '93729880063'
password = "SabrinA85$"

def pega_autenticacao(usuario, senha, tribunal = '2', instancia = '1'):
    payload = {'login' : usuario, 'senha' : senha}
    data = json.dumps(payload)
    headers = {'Accept-Encoding': 'gzip, deflate, br', 'Content-type': 'application/json',
               'x-grau-instancia': str(instancia)}
    url_autenticacao = 'https://pje.trt' + str(tribunal) + '.jus.br/pje-consulta-api/api/auth'  # auth
    r = requests.post(url_autenticacao, data, headers=headers)
    autenticacao = r.json()['access_token']
    return autenticacao

def verifica_autenticacao(autenticacao):
    if autenticacao == None:
        autenticacao = pega_autenticacao(username, password)
    return autenticacao