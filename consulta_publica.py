# consultas às APIs do PJe - em regra retornam um json ou valor de uma chave
import requests
from quebra_captcha_pje import quebra_captcha_pje


# CONSULTAS PÚBLICAS
def pega_id(numero_processo_cnj, tribunal = '2', instancia = '1'):
    headers = {'x-grau-instancia' : str(instancia)}
    url = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/dadosbasicos/" + numero_processo_cnj
    resposta = requests.get(url, headers=headers)
    return resposta.json()[0]['id']

# a partir do numero id do processo, devolve o request que carrega o json dos andamentos
# para pegar só o json, use a função consulta_andamentos_pje
def consulta_pje(numero_processo_id, tribunal = '2', instancia = '1'):
    headers = {'x-grau-instancia' : str(instancia)}
    url_consulta = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/" + str(numero_processo_id)
    resposta = requests.get(url_consulta, headers=headers)
    re_json = resposta.json()
    re_img_txt = re_json[r'imagem'] #pega a string dos bytes da imagem do captcha
    td = re_json[r'tokenDesafio']
    url_consulta = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/" + str(numero_processo_id) + "?tokenDesafio=" + td + "&resposta=" + str(quebra_captcha_pje(re_img_txt))
    resposta = requests.get(url_consulta, headers=headers)
    return resposta

# esta função é basicamente a reiteração da função acima, com a diferença que ele roda várias vezes
# até que a função quebra_captcha_pje funcione e a função consulta_api_pje venha completa
def consulta_publica(numero_processo, tribunal = '2', instancia = '1'):
    if len(str(numero_processo)) < 10:
        numero_processo_id = numero_processo
    else:
        numero_processo_id = pega_id(numero_processo)
    consulta =  consulta_pje(numero_processo_id, tribunal, instancia)

    while 'captchatoken' not in consulta.headers:
        consulta =  consulta_pje(numero_processo_id, tribunal, instancia)
    else:
        return consulta

