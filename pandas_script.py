
import pandas as pd

from caminhos import PASTA_PLANILHAS
from logger import infoLogs

import openpyxl
from datetime import datetime





def filtro_clientes():
    df = pd.read_excel(fr'{PASTA_PLANILHAS}\devolutivas.xlsx')

    hoje = datetime.now().strftime("%d-%m-%Y")

    try:
        df['data_consulta'] = pd.to_datetime(df['data_consulta'], format="%d-%m-%Y")

        # Data de hoje como datetime
        hoje = datetime.now().date()
        filtro = df[(df['data_consulta'].dt.date == hoje) & (df['status'] == 'Em andamento')]

        if not filtro.empty:
            clientes = filtro['clientes'].tolist()
            etapas = filtro['etapa'].tolist()
            return clientes, etapas
        else:
            infoLogs().info('Todos clientes marcados como concluidos')
            return [], []

    except Exception as e:
        infoLogs().info(f'Erro ao filtrar clientes: {e}')
        return [], []



def atualizar_total_cp(cliente, total_cp):
    try:
        # Carregar o arquivo Excel
        df = pd.read_excel(rf'{PASTA_PLANILHAS}\devolutivas.xlsx')
        
        # Garantir que a coluna 'data_consulta' seja do tipo datetime
        df['data_consulta'] = pd.to_datetime(df['data_consulta'], format="%d-%m-%Y", errors='coerce')
        
        # Data de hoje como datetime.date
        hoje = datetime.now().date()
        
        # Atualizar o valor na coluna 'total_cp' para o cliente na data de hoje
        mask = (df['clientes'] == cliente) & (df['data_consulta'].dt.date == hoje)
        
        if mask.any():  # Verificar se existe alguma linha correspondente
            df.loc[mask, 'total_cp'] = total_cp
            # Salvar o arquivo Excel atualizado
            df.to_excel(rf'{PASTA_PLANILHAS}\devolutivas.xlsx', index=False)


            # Converter a coluna para o formato 'DD-MM-YYYY'
            df['data_consulta'] = pd.to_datetime(df['data_consulta'], errors='coerce')  # Certifica que os valores sejam convertidos para datetime

            # Formatar as datas para 'DD-MM-YYYY'
            df['data_consulta'] = df['data_consulta'].dt.strftime('%d-%m-%Y')

            # Salvar novamente no Excel com as datas formatadas
            df.to_excel(rf'{PASTA_PLANILHAS}\devolutivas.xlsx', index=False)  


            infoLogs().info('Total de CP salvo na planilha.')
        else:
            infoLogs().info(f'Nenhuma linha encontrada para o cliente "{cliente}" e a data de hoje.')
    except Exception as e:
        infoLogs().info(f'Erro ao atualizar total_cp: {e}')







def atualizar_status(cliente, status):
    df = pd.read_excel(rf'{PASTA_PLANILHAS}\devolutivas.xlsx')

    hoje = datetime.now().strftime("%d-%m-%Y")

    df['data_consulta'] = pd.to_datetime(df['data_consulta'], format="%d-%m-%Y")

    # Data de hoje como datetime
    hoje = datetime.now().date()
    # filtro = df[(df['data_consulta'].dt.date == hoje) & (df['status'] == 'Em andamento') & (df['clientes'] == cliente)]


    df.loc[(df['clientes'] == cliente) & (df['data_consulta'].dt.date == hoje), 'status'] = status


    df.to_excel(rf'{PASTA_PLANILHAS}\devolutivas.xlsx', index=False)

            # Converter a coluna para o formato 'DD-MM-YYYY'
    df['data_consulta'] = pd.to_datetime(df['data_consulta'], errors='coerce')  # Certifica que os valores sejam convertidos para datetime

    # Formatar as datas para 'DD-MM-YYYY'
    df['data_consulta'] = df['data_consulta'].dt.strftime('%d-%m-%Y')

    # Salvar novamente no Excel com as datas formatadas
    df.to_excel(fr'{PASTA_PLANILHAS}\devolutivas.xlsx', index=False) 

    infoLogs().info('Status atualizado com sucesso')

def atualizar_etapa(cliente, etapa):
    df = pd.read_excel(rf'{PASTA_PLANILHAS}\devolutivas.xlsx')

    hoje = datetime.now().strftime("%d-%m-%Y")

    df['data_consulta'] = pd.to_datetime(df['data_consulta'], format="%d-%m-%Y")

    # Data de hoje como datetime
    hoje = datetime.now().date()
    # filtro = df[(df['data_consulta'].dt.date == hoje) & (df['etapa'] == 'Em andamento') & (df['clientes'] == cliente)]


    df.loc[(df['clientes'] == cliente) & (df['data_consulta'].dt.date == hoje), 'etapa'] = etapa


    df.to_excel(rf'{PASTA_PLANILHAS}\devolutivas.xlsx', index=False)

            # Converter a coluna para o formato 'DD-MM-YYYY'
    df['data_consulta'] = pd.to_datetime(df['data_consulta'], errors='coerce')  # Certifica que os valores sejam convertidos para datetime

    # Formatar as datas para 'DD-MM-YYYY'
    df['data_consulta'] = df['data_consulta'].dt.strftime('%d-%m-%Y')

    # Salvar novamente no Excel com as datas formatadas
    df.to_excel(fr'{PASTA_PLANILHAS}\devolutivas.xlsx', index=False) 

    infoLogs().info('Etapa atualizado com sucesso')




def cp_restantes():
    hoje = datetime.now().strftime("%d-%m-%Y")
    
    df = pd.read_excel(rf'{PASTA_PLANILHAS}\devolutivas.xlsx')
    
    df['data_consulta'] = pd.to_datetime(df['data_consulta'], format="%d-%m-%Y")

    # Obter a data atual no mesmo formato
    hoje = datetime.now().date()  # Apenas a parte da data
    try:
        # Aplicando o filtro
        filtro = df[(df['data_consulta'].dt.date == hoje) & (df['status'] == 'Em andamento')]
        
        # Verificando se o filtro retornou resultados
        if not filtro.empty:
            # Acessando o primeiro valor da Série usando iloc[0] e convertendo para int
            cp = int(filtro['cp'].iloc[0])
            total_cp = int(filtro['total_cp'].iloc[0])
            pagina = int(filtro['pagina'].iloc[0])
            posY = int(filtro['posY'].iloc[0])
            etapa = filtro['etapa'].iloc[0]
            cliente = filtro['clientes'].iloc[0]
            
            if cp == total_cp:
                infoLogs().info(f'Todos os comprovantes {etapa} baixados')
            
                #chamar funçao verifica_status() para mudar o status de Em andamento para Concluido


                return 'seguir'
            else:
                return cp, posY, pagina,cliente,total_cp
        else:
            infoLogs().info('Nenhuma linha encontrada com os critérios')
            return None
    except Exception as e:
        infoLogs().info(f'Valores vazios - Iniciar com padrão')
        return 'padrao'


def salvar_dados_correntes(cliente,cp,pagina,posY,etapa):
    hoje = datetime.now().strftime("%d-%m-%Y")

    df = pd.read_excel(fr'{PASTA_PLANILHAS}\devolutivas.xlsx')
    
    df['data_consulta'] = pd.to_datetime(df['data_consulta'], format="%d-%m-%Y")

    # Obter a data atual no mesmo formato
    hoje = datetime.now().date()  # Apenas a parte da data

    
    filtro = (df['data_consulta'].dt.date == hoje) & (df['status'] == 'Em andamento') & (df['clientes'] == cliente)
    if filtro.any():
        df.loc[filtro, 'cp'] = cp
        df.loc[filtro, 'posY'] = posY 
        df.loc[filtro, 'pagina'] = pagina 
        df.loc[filtro, 'etapa'] = etapa 

        # Salve novamente, se necessário
        df.to_excel(fr'{PASTA_PLANILHAS}\devolutivas.xlsx', index=False)
        
        
                # Converter a coluna para o formato 'DD-MM-YYYY'
        df['data_consulta'] = pd.to_datetime(df['data_consulta'], errors='coerce')  # Certifica que os valores sejam convertidos para datetime

        # Formatar as datas para 'DD-MM-YYYY'
        df['data_consulta'] = df['data_consulta'].dt.strftime('%d-%m-%Y')

        # Salvar novamente no Excel com as datas formatadas
        df.to_excel(fr'{PASTA_PLANILHAS}\devolutivas.xlsx', index=False) 
        
        infoLogs().info(f'Dados do processo salvos na planilha: Cliente={cliente}')
    else:
        infoLogs().info('Nenhuma linha encontrada com os critérios')
    


def consultar_progresso(cliente):
    df = pd.read_excel(rf'{PASTA_PLANILHAS}\devolutivas.xlsx')

    hoje = datetime.now().strftime("%d-%m-%Y")

    df['data_consulta'] = pd.to_datetime(df['data_consulta'], format="%d-%m-%Y")

    # Data de hoje como datetime
    hoje = datetime.now().date()
    # filtro = df[(df['data_consulta'].dt.date == hoje) & (df['status'] == 'Em andamento') & (df['clientes'] == cliente)]

    try:
        # Filtro para status 'Em andamento'
        filtro = df[(df['data_consulta'].dt.date == hoje) & (df['clientes'] == cliente) & (df['status'] == 'Em andamento')]
        
        if not filtro.empty:
            cliente = filtro['clientes']
            cp = filtro['cp']
            pagina = filtro['pagina']
            posY = filtro['posY']
            total_cp = filtro['total_cp']
            etapa = filtro['etapa']
            status = filtro['status']
            return cliente, cp, pagina, posY, total_cp, etapa, status
        
    except Exception as e:
        infoLogs().info(f"Erro: {e}")

    # Se não encontrou 'Em andamento', tenta 'Concluido'
    filtro = df[(df['data_consulta'].dt.date == hoje) & (df['clientes'] == cliente) & (df['status'] == 'Concluido')]

    # if not filtro.empty:
    #     cliente = filtro['clientes']
    #     cp = filtro['cp']
    #     pagina = filtro['pagina']
    #     posY = filtro['posY']
    #     total_cp = filtro['total_cp']
    #     etapa = filtro['etapa']
    #     status = filtro['status']
    #     return cliente, cp, pagina, posY, total_cp, etapa, status

    # Caso não encontre nenhum registro
    infoLogs().info("Nenhum registro encontrado para o cliente e data especificados.")
    return 'finalizado'
    








