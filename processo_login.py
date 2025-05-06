
import threading
import pyautogui as py
import time as tm
from caminhos import caminhoPrograma
from caminhos import PASTA_PLANILHAS
import pandas as pd
from acoes import (
    verifica_btn_entrar,
    verifica_erro_senha,
    verifica_btn_mais

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