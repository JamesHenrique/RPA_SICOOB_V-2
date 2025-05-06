import threading
import pyautogui as py
import time as tm
from caminhos import caminhoPrograma
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

)

from utils import iniciar_temporizador, renovar_sessao, sessao_ativa
from logger import infoLogs

# Iniciar a thread de renovação de sessão
thread_renovacao = threading.Thread(target=renovar_sessao, args=(sessao_ativa,), daemon=True)
thread_renovacao.start()

def fazer_login_cliente(agencia, chave_acesso, funcao_senha):
    """
    Realiza login para um cliente específico.
    """
    sessao_ativa.set()  # Ativa o evento de sessão
    tm.sleep(1.5)
    py.write(agencia)  # Agência
    py.press('tab')
    py.write(chave_acesso)  # Chave de acesso
    verifica_btn_mais()
    tm.sleep(1.5)
    funcao_senha()  # Função de senha personalizada
    verifica_btn_entrar()  # Clique no botão de entrar

    if verifica_erro_senha() == 'sim':
        infoLogs().info("Erro de senha. Reiniciando abertura.")
        tm.sleep(3)
        input('Erro ao fazer login... esperando uma resposta')
        return False

    infoLogs().info(f"Login realizado com sucesso - {agencia}")
    iniciar_temporizador()

    return True


clientes_info = {
    'SALGADARIA_3258': {
        'agencia': 3258,
        'chave': 'FH4256',
        'senha_func': senha_pos_SALGADARIA_FLORIPA
    },
    'IMPETUS_LTDA_4001': {
        'agencia': 4001,
        'chave': 'VA6704',
        'senha_func': senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_1
    },
    'IMPETUS_LTDA_5004': {
        'agencia': 5004,
        'chave': 'SG7802',
        'senha_func': senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_2
    },
    'IMPETUS_LTDA_4097': {
        'agencia': 4097,
        'chave': 'SP4110',
        'senha_func': senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_3
    },
    'IMPETUS_LTDA_4364': {
        'agencia': 4364,
        'chave': 'CL9977',
        'senha_func': senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_4
    },
    'RECAP_PNEUS_4277': {
        'agencia': 4277,
        'chave': 'UF6627',
        'senha_func': senha_pos_RECAP_PNEUS_4277
    },
    'RECAP_PNEUS_3214': {
        'agencia': 3214,
        'chave': 'PJ8932',
        'senha_func': senha_pos_RECAP_PNEUS_3214
    },
}

def funcao_senha(cliente):
    info = clientes_info.get(cliente)
    if info:
        info['senha_func']()
    else:
        infoLogs().error(f"Cliente {cliente} não encontrado na base de dados.")



def refaz_login_cliente(cliente):
    info = clientes_info.get(cliente)
    
    if not info:
        infoLogs().error(f"Cliente {cliente} não encontrado.")
        return False

    agencia = info['agencia']
    chave_acesso = info['chave']

    sessao_ativa.set()
    tm.sleep(1.5)
    py.write(str(agencia))
    py.press('tab')
    py.write(chave_acesso)
    verifica_btn_mais()
    tm.sleep(1.5)

    info['senha_func']()  # ou: funcao_senha(cliente)
    verifica_btn_entrar()

    if verifica_erro_senha() == 'sim':
        infoLogs().info("Erro de senha. Reiniciando abertura.")
        tm.sleep(3)
        refaz_login()
        

    infoLogs().info(f"Login realizado com sucesso - {agencia}")
    iniciar_temporizador()
    return True



def refaz_login():
    tenta = 0
    caminhoPrograma()

    while True:
        abriu_sicoob = verifica_logo_sicoob()
        
        if 'nao' != abriu_sicoob:
            return True
        
        print("Erro ao abrir o programa")
        infoLogs().warning(f"Tentativa {tenta+1} de login")

        py.click(x=1893, y=13)  # Fecha o programa
        tm.sleep(3)
        
        tenta += 1
        if tenta > 10:
            infoLogs().error(f"Número máximo de tentativas atingido em 'refaz_login': {tenta}")
            return False
        
        caminhoPrograma()  # Tenta abrir de novo
        tm.sleep(3)


