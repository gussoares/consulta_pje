import datetime
agora = datetime.datetime.now()

# MANIPULA DATAS

hoje = agora.strftime("%Y-%m-%d")
amanha = (agora + datetime.timedelta(1)).strftime("%Y-%m-%d")
ontem = (agora + datetime.timedelta(-1)).strftime("%Y-%m-%d")


def pega_data(data_longo):
    data = datetime.datetime.strptime(data_longo, '%Y-%m-%dT%H:%M:%S.%f')
    data = data.strftime("%d/%m/%Y")
    #print(data)
    return data

#print(hoje)