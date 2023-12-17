import numpy as np
import base64
from pytesseract import *
import cv2


def quebra_captcha_pje(imagem_str): # imagem_str são os bytes na forma de string
    """Função que recebe a imagem e devolve o texto com uma boa margem de acerto (mas nem sempre).
    imagem_str são os bytes na forma de string"""
    # converte string de bytes em imagem
    imagem_b64 = base64.b64decode(imagem_str)
    # converte em array
    imagem_array = np.asarray(bytearray(imagem_b64), dtype="uint8")
    # array em escala de cinza
    imagem_array_pb = cv2.imdecode(imagem_array, 0) # 0 para escala de cinza
    # eliminando excesso de riscos
    kernel_size = (3,3)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
    closing = cv2.morphologyEx(imagem_array_pb, cv2.MORPH_CLOSE, kernel)
    # pegando o texto
    frase = image_to_string(closing)
    frase = ''.join(frase.strip().split())
    # limpando qualquer leitura que encontre pontuação/símbolos
    import re
    pontuacao = re.compile('(\.|\?|,|\\|~|\^|´|:|-|;_|@)')
    frase = re.sub(pontuacao, '', frase)
    return frase