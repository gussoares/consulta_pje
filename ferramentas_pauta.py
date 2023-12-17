from tempo import hoje, amanha
import datetime
from consulta_autenticada import consulta_pauta
from baixa import baixa_integra_pje_autenticado


# FERRAMENTAS PARA CONTROLE DE PAUTA

def proxima_pauta(data = hoje):
    consulta = consulta_pauta(data)
    contador = 0
    if 'resultado' in consulta.keys():
        for p in consulta['resultado']:
            if p['indice'] < 9:
                print(p)   #['idProcesso'])

            #baixa_integra_pje_autenticado(p['idProcesso'])
    else:
        print("Aparentemente não há pauta: ", consulta)
        contador =+1
        data = datetime.datetime.strptime(data, '%Y-%m-%d')
        proxima = ((data + datetime.timedelta(contador)).strftime("%Y-%m-%d"))
        consulta = proxima_pauta(proxima)

#proxima_pauta()

'''['resultado']:
    print(p['resumoPoloPassivo'])'''


import uno
# import time

context = uno.getComponentContext()
resolver = context.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", context)
ctx = resolver.resolve( "uno:socket,host=localhost,port=12345;urp;StarOffice.ComponentContext" )
smgr = ctx.ServiceManager

desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
act =desktop.getActiveFrame()
doc = desktop.getCurrentFrame().loadComponentFromURL(
        "private:factory/swriter", "_default", 0, ())# "_blank", 0, ())
#doc = desktop.getCurrentComponent()
#print(dir(uno))
print(dir(doc))

#print(doc.getText())
print(dir(desktop))
print(dir(desktop.getSupportedServiceNames()))
print(dir(desktop.getCurrentFrame()))
print(dir(act))
print(dir(ctx))
print(dir(smgr))
if not hasattr(doc, "Text"):
    doc = desktop.getCurrentFrame().loadComponentFromURL(
        "private:factory/swriter", "_default", 0, ())# "_blank", 0, ())
doc.Frame.setTitle('casa')
print(dir(doc))
#print(doc.Title)