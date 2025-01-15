from datetime import datetime, timedelta

#data para gerar o relatório
def todasDatas():
    hoje = datetime.now().date()
    verificaSegunda = datetime.now().weekday()
    antes12 = datetime.now()
    
    

    if verificaSegunda == 0 :
        if antes12.hour < 12: #deve pegar apenas de sexta feira
            primeiraData = hoje
            ontem = timedelta(days=3)
            filtro = hoje - ontem
            primeiraData = filtro.strftime("%d.%m.%Y")#modificado para leitura
            segundaData =  filtro.strftime("%d.%m.%Y")
            return primeiraData,segundaData
        else:
            ontem = timedelta(days=2)
            filtro = hoje - ontem
            primeiraData = hoje.strftime("%d.%m.%Y")#modificado para leitura
            segundaData = filtro.strftime("%d.%m.%Y")
            return primeiraData,segundaData
    else:
        if antes12.hour < 12:
            ontem = timedelta(days=1)
            filtro = hoje - ontem
            primeiraData = filtro.strftime("%d.%m.%Y")#modificado para leitura
            segundaData = filtro.strftime("%d.%m.%Y")
            return primeiraData,segundaData
        else:
            primeiraData = hoje.strftime("%d.%m.%Y") #modificado para leitura
            segundaData = hoje.strftime("%d.%m.%Y")
            return primeiraData,segundaData


   


def verificaSegunda():
   
    hoje_segunda = ""

    verificaSegunda = datetime.now().weekday()
    antes12 = datetime.now()
    
    if verificaSegunda == 0 and antes12.hour > 12:
        hoje_segunda = "segunda depois das 12h"
    else:
        hoje_segunda = "não segunda"
    
    return hoje_segunda




