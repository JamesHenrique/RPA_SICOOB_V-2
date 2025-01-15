import time as tm
import pyautogui as py
from acoes import verifica_logo_sicoob,verifica_encerrar_sessao_1920x1080,verifica_btn_limpar_1920
# Inicializa o tempo de início
tempo_inicio = tm.time()

# Definir o tempo limite em segundos (15 minutos)
tempo_limite = 2 * 60   # 15 minutos em segundos

def encerra_sessao():
    # Função para encerrar a sessão
    print("Sessão encerrada devido ao limite de tempo.")
    verifica_encerrar_sessao_1920x1080()
    tm.sleep(3)
    verifica_logo_sicoob()
    verifica_btn_limpar_1920()





