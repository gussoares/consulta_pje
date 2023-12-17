# com base no número id do processo e id do documento, baixa o documento em pdf
# esta função parte do tokenDesafio e usa a função quebra_captcha_pje
import requests
from quebra_captcha_pje import quebra_captcha_pje
from consulta_publica import consulta_publica, pega_id

def baixa_pdf_pje(numero_processo, numero_documento_id, tribunal = '2', instancia = '1'):
    if len(str(numero_processo)) < 10:
        numero_processo_id = numero_processo
    else:
        numero_processo_id = pega_id(numero_processo)
    # faz um get usando o número id do processo para pegar o tokenDesafio
    headers = {'x-grau-instancia' : str(instancia)}
    url_consulta = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/" + str(numero_processo_id)
    resposta = requests.get(url_consulta, headers=headers)
    re_json = resposta.json()
    re_img_txt = re_json[r'imagem'] #pega a string dos bytes da imagem do captcha
    td = re_json[r'tokenDesafio']
    # já com o token desafio, pega o documento, usando a função quebra_captcha_pje
    url_documento = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/" + str(numero_processo_id) + "/documentos/" + str(numero_documento_id) + "?tokenDesafio=" + td + "&resposta=" + str(quebra_captcha_pje(re_img_txt))
    resposta = requests.get(url_documento, headers=headers, stream = True)
    # cria o nome do arquivo com base no número do processo e número do documento - altere à vontade!
    nome_do_arquivo = str(numero_processo_id) + "_" + str(numero_documento_id)
    # se pegou o PDF, salva o arquivo
    if resposta.content.startswith(b'%PDF'):
        with open(f'{nome_do_arquivo}.pdf', 'wb') as f:
            f.write(resposta.content)
    # se não deu certo, repete tudo
    else:
        baixa_pdf_pje(numero_processo_id, numero_documento_id, tribunal, instancia)


def baixa_pdf_pje_v2(numero_processo_id, numero_documento_id, tribunal = '2', instancia = '1'):
    headers = {'x-grau-instancia' : str(instancia)}
    url_documento = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/" + str(numero_processo_id) + "/documentos/"  + str(numero_documento_id) + "/conteudo?tokenCaptcha=" + pega_captchatoken(numero_processo_id, tribunal, instancia)
    r4 = requests.get(url_documento, headers=headers, stream = True)
    # cria o nome do arquivo com base no número do processo e número do documento - altere à vontade!
    nome_do_arquivo = str(numero_processo_id) + "_" + str(numero_documento_id)
    # se pegou o PDF, salva o arquivo
    if r4.content.startswith(b'%PDF'):
        with open(f'{nome_do_arquivo}.pdf', 'wb') as f:
            f.write(r4.content)
    # se não deu certo, repete tudo
    else:
        baixa_pdf_pje_v2(numero_processo_id, numero_documento_id, tribunal, instancia)




# não é a integra de verdade pois o acesso público (com captcha) é limitado
# usa a função pega_captchatoken, mas pode adaptar para usa o captcha token eventualmente já obtido ou, ainda, usar a função quebra_captcha_pje
def baixa_integra_pje(numero_processo_id, tribunal='2', instancia='1'):
    headers = {'x-grau-instancia': str(instancia)}
    url3a = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/" + str(
        numero_processo_id) + '/integra?tokenCaptcha=' + pega_captchatoken(numero_processo_id, tribunal='2',
                                                                           instancia='1')
    r2 = requests.get(url3a, headers=headers)
    nome_do_arquivo = str(numero_processo_id) + "_" + 'integra'
    if r2.content.startswith(b'%PDF'):
        with open(f'{nome_do_arquivo}.pdf', 'wb') as f:
            f.write(r2.content)
    else:
        baixa_integra_pje(numero_processo_id, numero_documento_id, tribunal, instancia)



# usa a função consulta_publica para obter os itensProcesso
# se o título de itensProcesso é sentença, descobre o número do documento e aplica a usa a função baixa_docs_pje

def pega_sentenca_cnj(numero_processo_cnj, destino = None, tribunal = '2', instancia = '1'):
    numero_processo_id = pega_id(numero_processo_cnj)
    headers = {'x-grau-instancia': str(instancia)}

    consulta = consulta_publica(numero_processo_id, tribunal, instancia)
    while 'captchatoken' not in consulta.headers:
        consulta = consulta_publica(numero_processo_id, tribunal, instancia)
    captcha = consulta.headers['captchatoken']

    for item in consulta.json()['itensProcesso']:
        if item['titulo']== "Sentença": # and i['usuarioJuntada']=='GUSTAVO SCHILD SOARES':
            if item['tipoConteudo']== 'PDF':

                numero_documento_id = str(item['id'])
                id_documento = str(item['idUnicoDocumento'])
                print(numero_processo_cnj, numero_documento_id + " - " + item['titulo'])

                url_documento = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/" + str(
                    numero_processo_id) + "/documentos/" + str(
                    numero_documento_id) + "/conteudo?tokenCaptcha=" + captcha
                    #+ "?tokenDesafio=" + td + "&resposta=" + str(quebra_captcha_pje(re_img_txt))'''
                resposta = requests.get(url_documento, headers=headers, stream=True)
                nome_usuario = item['usuarioJuntada'].strip().replace(" ", '_')

                nome_do_arquivo = str(numero_processo_cnj) + "_" + str(numero_processo_id) + "_" + str(
                    item['idUnicoDocumento']) + "_" + str(numero_documento_id)

                if destino != None:
                    pasta = destino + "/" + nome_usuario
                    print(pasta)

                else:
                    pasta = nome_usuario
                    print(pasta)

                import os
                if os.path.isdir(pasta):
                    print('pasta já existe')
                    pass
                else:
                    os.mkdir(pasta)
                    print('pasta nao existe')

                if resposta.content.startswith(b'%PDF'):
                    print(os.getcwd())

                    with open(f'{pasta}/{nome_do_arquivo}.pdf', 'wb') as f:
                        f.write(resposta.content)
                        print(f'{pasta}/{nome_do_arquivo}.pdf')

                else:
                    print('erro')

def pega_sentenca_id(numero_processo_id, tribunal = '2', instancia = '1'):
    headers = {'x-grau-instancia' : str(instancia)}
    consulta = consulta_publica(numero_processo_id, tribunal, instancia)
    for item in consulta.json()['itensProcesso']:
        if item['titulo']=='Sentença':
            if item['tipoConteudo']== 'PDF':
                numero_documento_id = str(item['id'])
                baixa_pdf_pje(numero_processo_id, numero_documento_id, tribunal, instancia)


# usa a função consulta_publica para obter os itensProcesso
# se o título de itensProcesso é ata, descobre o número do documento e aplica a usa a função baixa_docs_pje
def pega_ata_pje(numero_processo_id, tribunal='2', instancia='1'):
    headers = {'x-grau-instancia': str(instancia)}
    consulta = consulta_publica(numero_processo_id, tribunal, instancia)
    for item in consulta.json()['itensProcesso']:

        if item['titulo'] == 'Ata da Audiência':
            if item['tipoConteudo'] == 'PDF':
                numero_documento_id = str(item['id'])
                baixa_pdf_pje(numero_processo_id, numero_documento_id, tribunal, instancia)

def pega_acordao_pje(numero_processo_cnj, tribunal='2', instancia='1'):
    headers = {'x-grau-instancia': str(instancia)}
    numero_processo_id = \
    dados_basicos_pje(numero_processo_cnj=numero_processo_cnj, tribunal=tribunal, instancia=instancia).json()[0][
        'id']
    consulta = consulta_publica(numero_processo_id, tribunal=tribunal, instancia=instancia)
    tc = consulta.headers['captchatoken']
    for item in consulta.json()['itensProcesso']:
        if item['titulo'] == "Acórdão":
            id_documento = str(item['idUnicoDocumento'])
            numero_documento_id = str(item['id'])
            nome_do_arquivo = numero_processo_cnj + '_' + str(
                numero_processo_id) + "_" + id_documento + "_" + numero_documento_id
            url5 = "https://pje.trt" + str(tribunal) + ".jus.br/pje-consulta-api/api/processos/" + str(
                numero_processo_id) + "/documentos/" + str(numero_documento_id) + "/conteudo?tokenCaptcha=" + tc
            r4 = requests.get(url5, headers=headers, stream=True)
            with open(f'{nome_do_arquivo}.pdf', 'wb') as f:
                print(r4.headers)
                print(r4.content)
                f.write(r4.content)