from consulta_autenticada import consulta_expandida, consulta
from tempo import hoje

# IDEIAS PARA EXECUÇÃO
# TESTE DE CONSULTA DE TERCEIROS POR CNPJ

cnpj = " 	46523270000188" #46.523.270/0001-88"
c = consulta_expandida(autenticacao = None, cnpj_parte= cnpj, classe_processo='326' or '387',
                        data_inicio='2023-08-01', data_fim=hoje, tribunal='2', instancia='1',
                        pagina='1', tamanhoPagina="20", ordenacaoColuna='undefined',
                        ordenacaoCrescente='undefined')


for item in c:
    if item is list:
        print(item)
    else:
        print(consulta(str(item['id'])))


