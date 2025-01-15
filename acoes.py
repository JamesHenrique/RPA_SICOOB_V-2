import pyautogui
import time
import pyautogui as py

# time.sleep(2)

# screenshot = pyautogui.screenshot(r'C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_prox_pagina.png', region=(965,880,50, 20))#x,y,largura,altura

"""
965,883

475,579 - cabecalho_pix

691,412 - 8
602,413

btn_limpar_1920 - 729,445
encerrar_sessao_1920x1080 - 1478,126
nenhum_cp_selecionado - 676,406

check_box_convenio - 594,570

975,879 - prox_pag

307,121 - home
703,530 - cabeçalho_titulos

963,950 - btn_salvar

911,489 - formato_PDF

870,540 - btn_salvar_pdf

712,948 - btn_voltar

681,580 - btn_consultar

455,616 - btn_detalhar

902,866 - btn_imprimir
"""


def verifica_cabecalho_pix():

    time.sleep(1)
    tentativas = 0
    while True:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\cabecalho_pix.png", confidence=0.5) #alterar o confidence sempre que não achar
            if button_location:

                print('cabecalho_pix encontrado')
                
                
                # pyautogui.click(pyautogui.center(button_location))
                return True
                
        except:
            # py.press('esc',presses=2)
            # py.scroll(-)
            tentativas += 1
            print(f'tentando localizar - cabecalho_pix | {tentativas}x')

            if tentativas == 10:
                return False
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente



def verifica_btn_iniciar_cinza():

    time.sleep(1)
 
    while True:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_iniciar_cinza.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:

                print('btn_iniciar_cinza clicado')
                pyautogui.click(pyautogui.center(button_location))
                return 'sim'
        except:
            # py.press('esc',presses=2)
            # py.hotkey('alt','tab')
            
            print('tentando localizar - btn_iniciar_cinza')
        
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente




def verifica_btn_sim():

    time.sleep(1)
 
    while True:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\img_sim.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:

                print('btn_sim clicado')
                pyautogui.click(pyautogui.center(button_location))
                return 'sim'
        except:
            # py.press('esc',presses=2)
            # py.hotkey('alt','tab')
            
            print('tentando localizar - btn_sim')
        
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente



def verifica_btn_limpar_1920():
    time.sleep(1)

    while True:


        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_limpar_1920.png", confidence=0.9)
            if button_location:
                print('limpar campos...')
                pyautogui.click(pyautogui.center(button_location))
                tm.sleep(2)
                pyautogui.press('tab', presses=2, interval=0.3)
                return 'sim'
        except Exception as e:
            print(f"Erro ao tentar localizar o botão: {e}")
            print('tentando localizar - btn_limpar_1920')

        time.sleep(3)  # Espera 3 segundos antes de tentar novamente




def verifica_encerrar_sessao_1920x1080():
    time.sleep(1)

    while True:
       
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\encerrar_sessao_1920x1080.png", confidence=0.7)
            if button_location:
                print('encerrando sessao...')
                pyautogui.click(pyautogui.center(button_location))
                return 'sim'
        except Exception as e:
            print(f"Erro ao tentar localizar o botão: {e}")
            print('tentando localizar - encerrar_sessao_1920x1080')

        time.sleep(3)  # Espera 3 segundos antes de tentar novamente

def verifica_app_sicoob():

    time.sleep(1)
 
    while True:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\app_sicoob.png", confidence=0.7) #alterar o confidence sempre que não achar
            if button_location:
                print('app_sicoob')

                pyautogui.click(pyautogui.center(button_location))
                return 'sim'
        except:
            # py.press('esc',presses=2)
            
            print('tentando localizar - app_sicoob')
        
        time.sleep(3)  # Espera 1 segundo antes de tentar novamente

def verifica_btn_prox_pagina():
    time.sleep(1)

    tent = 0
    while tent != 5:
       
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_prox_pagina.png", confidence=0.8)
            if button_location:
                print('btn_prox_pagina')
                pyautogui.click(pyautogui.center(button_location))
                return True
        except Exception as e:
            tent = tent + 1
            print(f"Erro ao tentar localizar o botão: {e}")
            print(f'tentando localizar - btn_prox_pagina {tent}x')

        time.sleep(3)  # Espera 3 segundos antes de tentar novamente
    return False



def verifica_btn_inicio():
    time.sleep(1)
    tentativas = 0
    while tentativas != 10:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_inicio.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('btn_inicio')

                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - btn_inicio')
            tentativas += 1
        time.sleep(3)  # Espera 1 segundo antes de tentar novamente
    return 'nao'



def verifica_cabecalho_convenio():
 
    time.sleep(1)
    tentativas = 0
    tentativas_max = 3

    while tentativas < tentativas_max:


        try:
            button_location = pyautogui.locateOnScreen(
                r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\cabecalho_titulos.png",
                confidence=0.5
            )
            if button_location:
                print("Cabeçalho encontrado.")
                return 'sim'
        except:
            print(f"Tentando localizar - cabeçalho_titulos | {tentativas + 1}x")
            tentativas += 1

        time.sleep(2.5)  # Espera antes de tentar novamente

    return 'nao'




def verifica_nenhum_cp_selecionado():

    tentativas = 0
    tentativas_max = 3

    while True:
       

        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\nenhum_cp_selecionado.png", confidence=0.99)
            if button_location:
                print("Localizado: nenhum_cp_selecionado")
                return 'sim'
        except:
            print(f"Tentando localizar - nenhum_cp_selecionado | {tentativas + 1}x")
            tentativas += 1

            if tentativas >= tentativas_max:
                return 'seguir'

        time.sleep(1)  # Espera antes da próxima tentativa

    return 'nao'



def verifica_cabecalho_convenio():
    time.sleep(1)
    tentativas = 0
    while tentativas < 2:
       
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\cabecalho_titulos.png", confidence=0.5)
            if button_location:
                print('cabeçalho localizado.')
                return 'sim'
        except:
            print(f'tentando localizar - cabeçalho |{tentativas}x')
            tentativas += 1
        time.sleep(2.5)
    return 'nao'

def verifica_cabecalho_titulos():
    time.sleep(1)
    tentativas = 0
    while tentativas < 3:
       
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\cabecalho_titulos.png", confidence=0.7)
            if button_location:
                print('cabeçalho_titulos localizado.')
                pyautogui.click(pyautogui.center(button_location))
                return 'sim'
        except:
            print(f'tentando localizar - cabeçalho_titulos | tentativas {tentativas + 1}x')
            tentativas += 1
        time.sleep(3)
    return 'nao'

def verifica_btn_detalhar():
    time.sleep(1)
    tentativas = 0
    while tentativas < 5:
        
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_detalhar.png", confidence=0.9)
            if button_location:
                print('btn_detalhar localizado.')
                pyautogui.click(pyautogui.center(button_location))
                return 'sim'
        except:
            print(f'tentando localizar - btn_detalhar | tentativas {tentativas + 1}x')
            # pyautogui.scroll(-1000, x=509, y=694)
            tentativas += 1
        time.sleep(3)
    return 'nao'

def verifica_btn_imprimir():
    time.sleep(1)
    tentativas = 0
    while tentativas < 10:
        
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_imprimir.png", confidence=0.9)
            if button_location:
                print('btn_imprimir localizado.')
                pyautogui.click(pyautogui.center(button_location))
                return True
        except:
            py.scroll(-500)
            print(f'tentando localizar - btn_imprimir | tentativas {tentativas + 1}x')
            tentativas += 1
        time.sleep(3)
    return False

def verifica_btn_gerar_comprovante():
    time.sleep(1)
    while True:
       
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_gerar_comprovante.png", confidence=0.9)
            if button_location:
                print('btn_gerar_comprovante localizado.')
                pyautogui.click(pyautogui.center(button_location))
                return 'localizado'
        except:
            print('tentando localizar - btn_gerar_comprovante')
        time.sleep(3)
    return 'nao'



def verifica_btn_salvar():
    time.sleep(1)
    tentativas = 0
    while tentativas < 5:
        
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_salvar.png", confidence=0.9)
            if button_location:
                print('btn_salvar localizado.')
                pyautogui.click(pyautogui.center(button_location))
                return True
        except:
            print(f'tentando localizar - btn_salvar | {tentativas + 1}x')
            tentativas += 1
        time.sleep(3)
    return False


def verifica_formato_pdf():
    time.sleep(1)
    while True:
       
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\formato_pdf.png", confidence=0.9)
            if button_location:
                print('formato_pdf localizado.')
                pyautogui.click(pyautogui.center(button_location))
                return 'localizado'
        except:
            print('tentando localizar - formato_pdf')
        time.sleep(3)
    return 'nao localizado'


def verifica_btn_salvar_pdf():
    time.sleep(1)
    while True:
      
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_salvar_pdf.png", confidence=0.9)
            if button_location:
                print('btn_salvar_pdf localizado.')
                pyautogui.click(pyautogui.center(button_location))
                return 'localizado'
        except:
            print('tentando localizar - btn_salvar_pdf')
        time.sleep(3)
    return 'nao localizado'


def verifica_btn_voltar():
    time.sleep(1)
    tentativas = 0
    while tentativas < 10:
 
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_voltar.png", confidence=0.9)
            if button_location:
                print('btn_voltar localizado.')
                pyautogui.click(pyautogui.center(button_location))
                return 'localizado'
        except:
            tentativas += 1
            py.scroll(-500)
            print(f'tentando localizar - btn_voltar | {tentativas}x')
        time.sleep(5)

    print('Número máximo de tentativas atingido. Encerrando sessão...')

    return 'nao localizado'




def verifica_btn_consultar():
    time.sleep(1)
    while True:
       
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_consultar.png", confidence=0.9)
            if button_location:
                print('btn_consultar localizado')
                pyautogui.click(pyautogui.center(button_location))
                return 'localizado'
        except Exception as e:
            print(f"Erro ao tentar localizar o botão: {e}")
            print('tentando localizar - btn_consultar')

        time.sleep(3)  # Espera antes de tentar novamente


def verifica_logo_sicoob():
    time.sleep(20)
    tentativas = 0
    while tentativas != 5:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\logo_sicoob.png", confidence=0.9) #alterar o confidence sempre que não achar
            if button_location:
                print('logo sicoob localizado')
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - logo sicoob')
            tentativas += 1
        time.sleep(20)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def verifica_erro_senha():
    time.sleep(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\erro_senha.png", confidence=0.7) #alterar o confidence sempre que não achar
            if button_location:
                print('erro_senha localizado')
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - erro_senha')
            tentativas += 1
        time.sleep(2)  # Espera 1 segundo antes de tentar novamente
    return 'nao'

def verifica_btn_entrar():
    time.sleep(1)
    tentativas = 0
    while True:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_entrar.png", confidence= 0.9) #alterar o confidence sempre que não achar
            if button_location:
                pyautogui.click(button_location)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - btn_entrar')
            tentativas += 1
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente


def verifica_btn_mais():
    time.sleep(1)
    tentativas = 0
    while True:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\btn_mais.png", confidence= 0.99) #alterar o confidence sempre que não achar
            if button_location:
                pyautogui.click(button_location,clicks=3)
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - btn_mais')
            tentativas += 1
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente





def num_0():
    time.sleep(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\0.png", confidence= 0.99) #alterar o confidence sempre que não achar
            if button_location:
                pyautogui.click(button_location)
                print('clicou: 0 - ',pyautogui.position())
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - erro_senha num_0')
            tentativas += 1
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def num_1():
    time.sleep(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\1.png", confidence= 0.9) #alterar o confidence sempre que não achar
            if button_location:
                pyautogui.click(button_location)
                print('clicou: 1 - ',pyautogui.position())
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - erro_senha num_1')
            tentativas += 1
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def num_2():
    time.sleep(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\2.png", confidence= 0.9) #alterar o confidence sempre que não achar
            if button_location:
                pyautogui.click(button_location)
                print('clicou: 2 - ',pyautogui.position())
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - erro_senha num_2')
            tentativas += 1
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'

def num_3():
    time.sleep(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\3.png", confidence= 0.9) #alterar o confidence sempre que não achar
            if button_location:
                pyautogui.click(button_location)
                print('clicou: 3 - ',pyautogui.position())
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - num_3')
            tentativas += 1
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'
 
 
def num_4():
    time.sleep(1)
    tentativas = 0
    while tentativas != 4:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\4.png", confidence= 0.9) #alterar o confidence sempre que não achar
            if button_location:
                pyautogui.click(button_location)
                print('clicou: 4 - ',pyautogui.position())
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - num_4')
            tentativas += 1
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'

def num_5():
    time.sleep(1)
    tentativas = 0
    while tentativas != 4:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\5.png", confidence= 0.9) #alterar o confidence sempre que não achar
            if button_location:
                pyautogui.click(button_location)
                print('clicou: 5 - ',pyautogui.position())
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - num_5')
            tentativas += 1
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def num_6():
    time.sleep(1)
    tentativas = 0
    while tentativas != 4:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\6.png", confidence= 0.9) #alterar o confidence sempre que não achar
            if button_location:
                pyautogui.click(button_location)
                print('clicou: 6 - ',pyautogui.position())
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - num_6')
            tentativas += 1
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def num_7():
    time.sleep(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\7.png", confidence= 0.9) #alterar o confidence sempre que não achar
            if button_location:
                pyautogui.click(button_location)
                print('clicou: 7 - ',pyautogui.position())
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - num_7')
            tentativas += 1
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'

def num_8():
    time.sleep(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\8.png", confidence= 0.99) #alterar o confidence sempre que não achar
            if button_location:
                pyautogui.click(button_location)
                print('clicou: 8 - ',pyautogui.position())
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - num_8')
            tentativas += 1
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'


def num_9():
    time.sleep(1)
    tentativas = 0
    while tentativas != 3:
        try:
            button_location = pyautogui.locateOnScreen(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - V2\prints\9.png", confidence= 0.9) #alterar o confidence sempre que não achar
            if button_location:
                pyautogui.click(button_location)
                print('clicou: 9 - ',pyautogui.position())
                return 'sim'
        except:
            # py.press('esc',presses=2)
            print('tentando localizar - num_9')
            tentativas += 1
        time.sleep(5)  # Espera 1 segundo antes de tentar novamente
    return 'nao'



import time as tm
tempo = 1.5

def senha_pos_SALGADARIA_FLORIPA():
    num_7()
    num_8()
    num_3()
    num_8()
    num_4()
    num_0()
    num_8()
    num_7()




def senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_1():
    num_3()
    num_3()
    num_2()
    num_8()
    num_2()
    num_8()
    num_7()
    num_7()
    






def senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_2():
    #senha/acesso - 33282877
    num_3()
    num_3()
    num_2()
    num_8()
    num_2()
    num_8()
    num_7()
    num_7()  
    
def senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_3():
    #senha/acesso - 96804156
    num_9()
    num_6()
    num_8()
    num_0()
    num_4()
    num_1()
    num_5()
    num_6() 


    
def senha_pos_IMPETUS_ENERGY_E_BUSINESS_LTDA_4():
    #senha/acesso - 33282877
    num_3()
    num_3()
    num_2()
    num_8()
    num_2()
    num_8()
    num_7()
    num_7() 

