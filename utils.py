import time as tm
import threading
from acoes import verifica_btn_sim

# Evento para controlar a execução
sessao_ativa = threading.Event()

TEMPO_LIMITE = 950 #15min
inicio_tempo = None

def iniciar_temporizador():
    global inicio_tempo
    inicio_tempo = tm.time()  # Marca o início do tempo

def verificar_tempo_limite():
    global inicio_tempo
    if inicio_tempo and tm.time() - inicio_tempo >= TEMPO_LIMITE:
        print("Tempo limite atingido. Esperando ação do usuário...")
        
        verifica_btn_sim()
        
        # input('Pressione Enter para continuar...')  # Pausa o fluxo até uma ação do usuário
        iniciar_temporizador()  # Reinicia o temporizador após a ação do usuário

def verifica_sessao_expirada():
    return not sessao_ativa.is_set()

def renovar_sessao(sessao_ativa):
    while True:
        sessao_ativa.wait()  # Aguarda até que a sessão esteja ativa
        try:
            if verifica_sessao_expirada():
                print("Sessão expirada. Tentando renovar a sessão...")
                input('Digite algo para continuar...')
                print("Sessão renovada com sucesso.")
                sessao_ativa.set()  # Reativa a sessão
            else:
                pass

            tm.sleep(10)  # Aguarda 10 segundos antes de verificar novamente

        except Exception as e:
            print(f"Erro ao renovar a sessão: {e}")
            tm.sleep(10)  # Aguarda 10 segundos antes de tentar novamente