import threading
import pyautogui as py
import time as tm
from caminhos import caminhoPrograma
from caminhos import PASTA_PLANILHAS
import pandas as pd
from acoes import (
    senha_pos_SALGADARIA_FLORIPA,
    senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_1,
    senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_2,
    senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_3,
    senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_4,
    senha_pos_RECAP_PNEUS_4277,
    senha_pos_RECAP_PNEUS_3214,
    verifica_btn_entrar,
    verifica_erro_senha,
    verifica_logo_sicoob,
    verifica_btn_mais,
    verifica_encerrar_sessao_1920x1080,
    verifica_btn_limpar_1920
)
from pandas_script import filtro_clientes, atualizar_etapa,consultar_progresso,atualizar_status
from titulos import ir_para_titulos
from convenio import ir_para_convenio
from comprovantePix import ir_para_pix
from refresh_session import encerra_sessao
from utils import iniciar_temporizador, verificar_tempo_limite, renovar_sessao, sessao_ativa
from logger import infoLogs
from processo import fazer_login_cliente

# Iniciar a thread de renovação de sessão
thread_renovacao = threading.Thread(target=renovar_sessao, args=(sessao_ativa,), daemon=True)
thread_renovacao.start()





def fazerLogin():
    caminhoPrograma()
    abriu_sicoob = verifica_logo_sicoob()

    if 'nao' in abriu_sicoob:
        print("Erro ao abrir o programa")
        tm.sleep(3)
        py.click(x=1893,y=13)
        tm.sleep(3)
        fazerLogin()
    else:
        iniciar_clientes()
        pass



def iniciar_clientes():
    """
    Itera sobre a lista de clientes e realiza login para cada um.
    """
    try:
        # Supõe-se que filtro_clientes retorna uma lista de clientes e suas etapas
        clientes, etapas = filtro_clientes()

        if not clientes:
            infoLogs().info('Nao existe informações na planilha para continuar')
            return 'finalizado'

        def processar_cliente(cliente, codigo, usuario, senha):
            if not fazer_login_cliente(codigo, usuario, senha):
                infoLogs().info(f'Erro ao fazer login {cliente}')
                return

            while True:
                verificar_tempo_limite()  # Verificação do tempo limite
                etapa_atual = consultar_progresso(cliente)[5].iloc[0]

                if etapa_atual == 'titulos':
                    infoLogs().info(f'Cliente: {cliente} | etapa: {etapa_atual}')
                    ir_para_titulos(cliente)
                    atualizar_etapa(cliente, 'convenio')  # Atualiza para a próxima etapa
                elif etapa_atual == 'convenio':
                    infoLogs().info(f'Cliente: {cliente} | etapa: {etapa_atual}')
                    ir_para_convenio(cliente)
                    atualizar_etapa(cliente, 'pix')  # Atualiza para a próxima etapa
                elif etapa_atual == 'pix':
                    infoLogs().info(f'Cliente: {cliente} | etapa: {etapa_atual}')
                    ir_para_pix(cliente)
                    atualizar_etapa(cliente, 'pdf')  # Atualiza para a próxima etapa
                else:
                    infoLogs().info(f'Processo finalizado para Cliente: {cliente}')
                    verifica_encerrar_sessao_1920x1080()
                    tm.sleep(3)
                    verifica_btn_limpar_1920()
                    atualizar_status(cliente, 'Concluido')
                    break

        cliente_info = {
            'SALGADARIA_3258': ('3258', 'FH4256', senha_pos_SALGADARIA_FLORIPA),
            'IMPETUS_LTDA_4001': ('4001', 'VA6704', senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_1),
            'IMPETUS_LTDA_5004': ('5004', 'SG7802', senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_2),
            'IMPETUS_LTDA_4097': ('4097', 'SP4110', senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_3),
            'IMPETUS_LTDA_4364': ('4364', 'CL9977', senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_4),
            'RECAP_PNEUS_4277': ('4277','UF6627',senha_pos_RECAP_PNEUS_4277),
            'RECAP_PNEUS_3214': ('3214','PJ8932',senha_pos_RECAP_PNEUS_3214)
        }

        for cliente, etapa in zip(clientes, etapas):
            # Verificar se cliente é hashável e não uma Series
            if isinstance(cliente, pd.Series):
                cliente = cliente.iloc[0]  # ou outra maneira de extrair o valor desejado
            if cliente in cliente_info:
                codigo, usuario, senha = cliente_info[cliente]
                processar_cliente(cliente, codigo, usuario, senha)

        infoLogs().info('Todos clientes processados - Etapa Renomear CP')
        return 'seguir'

    except Exception as e:
        infoLogs().info(f'Erro iniciar cliente | {e}')
        return 'nao'
    


    
# # Exemplo de uso da função (supondo que as funções chamadas dentro de iniciar_clientes estão definidas)
# if __name__ == "__main__":
#     resultado = iniciar_clientes()
#     print(f"Resultado da execução: {resultado}")
