import pyautogui as py
import pandas as pd
import time as tm
from datas import todasDatas,verificaSegunda
from extrairTextoPrint import qntComprovantePix, erroTextoPix
from tirarPrint import tirarPrintPix, tirarPrintErroPix
import pyperclip
from datetime import datetime, timedelta
from acoes import verifica_total_regis_pix,verifica_btn_consultar,verifica_btn_voltar, verifica_btn_detalhar,verifica_btn_imprimir,verifica_cabecalho_pix,verifica_btn_prox_pagina
from moverPasta import criar_caminho_onedrive
import os
from pandas_script import atualizar_etapa,salvar_dados_correntes,atualizar_status,consultar_progresso
from caminhos import PASTA_PLANILHAS
from logger import infoLogs

import threading
from utils import  verificar_tempo_limite, renovar_sessao, sessao_ativa

# Iniciar a thread de renovação de sessão
thread_renovacao = threading.Thread(target=renovar_sessao, args=(sessao_ativa,), daemon=True)
thread_renovacao.start()



tempo = 1



dados = []


tentativas = 0
max_tentativas = 5

def encerrar_processo():
    infoLogs().info("Encerrando o processo em pix")
    tm.sleep(3)
    py.click(x=1893,y=13)
    tm.sleep(3)
    


def ir_para_pix_novamente():
    global tentativas
    tentativas += 1

    verificar_tempo_limite()
    
    apenas_dia1 = ""
    apenas_dia2 = ""

    # Posição tela PIX
    tm.sleep(2)  # Variável 'tempo' não definida, substitui por 2 segundos
    py.click(x=1073, y=151)

    # Clique em extrato PIX
    tm.sleep(1)
    py.click(x=1090, y=204)

    # Clique no 1º campo de data
    tm.sleep(2)
    py.click(x=573, y=621)
    tm.sleep(2)

    # Verifica se é "segunda depois das 12h" e define as datas
    if "segunda depois das 12h" in verificaSegunda():
        apenas_dia1 = todasDatas()[1].split('.')[0]
        apenas_dia2 = todasDatas()[0].split('.')[0]
    else:
        apenas_dia1 = todasDatas()[0].split('.')[0]
        apenas_dia2 = todasDatas()[1].split('.')[0]

    # Escreve as datas nos campos
    py.write(apenas_dia1, interval=0.5)
    tm.sleep(1)
    py.write(apenas_dia2, interval=0.5)

    # Verifica e clica no botão consultar
    verifica_btn_consultar()

    # Verifica o cabeçalho PIX
    if not verifica_cabecalho_pix():
        infoLogs().info('erro ao encontrar o cabeçalho novamente')
        if tentativas < max_tentativas:
            ir_para_pix_novamente()
        else:
            infoLogs().info('Número máximo de tentativas atingido')
            encerrar_processo()
    return True


def seleciona_cp_pix(cliente):

    total_cp = consultar_progresso(cliente)[4].iloc[0]

    quantidade_comprovantes = total_cp
    
    infoLogs().info(f'Total de CP pix {quantidade_comprovantes}')

    total_paginas = quantidade_comprovantes / 10
    rest_div = total_paginas % 10
    if rest_div > 0 and rest_div < 10:
        total_paginas += 1

    troca_pagina = 1
    num_cp = 1
    pagina_atual = 1
    posY = 466
    etapa = 'pix'
    total_acumulado = 1

    caminho_base = criar_caminho_onedrive(cliente)
    # Começar de onde parou
    while quantidade_comprovantes > 0:

        verificar_tempo_limite()


        if num_cp >= 11 and int(total_paginas) > 0:
            posY = 466
            num_cp = 1
            total_paginas -= 1
            pagina_atual += 1
            troca_pagina += 1

            # if not verifica_btn_prox_pagina():
            #     py.click(774, 793)  # -> próxima página

            py.click(774, 793)  # -> próxima página

        tm.sleep(2)
        infoLogs().info(f'Comprovante {num_cp}º')
        

        if not verifica_cabecalho_pix():
            ir_para_pix_novamente()
            tm.sleep(1)
            continue
            
            
        tm.sleep(2)

        py.click(500,500)

        tm.sleep(2)

        py.scroll(-1000)
       
        tm.sleep(2)
  
        py.click(x=475, y=posY)


        tm.sleep(1)

        if 'nao' in verifica_btn_detalhar():
            infoLogs().info("Erro no botao detalhar\n Reiniciando o processo")
            ir_para_pix_novamente()
            continue


        tm.sleep(2)

        py.scroll(-1000)

        if not verifica_btn_imprimir():
            infoLogs().info('Verificar imprimir falhou - retornando ao começo do pix')
            ir_para_pix_novamente()
            tm.sleep(1)
            continue

        tm.sleep(1.5)
        verifica_btn_imprimir()

        tm.sleep(1.5)
        py.press('enter')
        tm.sleep(1.5)

        nome_arquivo = f'pix{quantidade_comprovantes}_{todasDatas()[0]}'

        tm.sleep(0.5)

        caminho_completo = os.path.join(caminho_base, nome_arquivo)


        tm.sleep(0.5)
        # Copiar o caminho completo para a área de transferência e colar (opcional)
        pyperclip.copy(caminho_completo)

        tm.sleep(0.5)
        py.hotkey('ctrl','v')

        tm.sleep(1)
        py.press('enter')

        tm.sleep(0.5)
    

        #feche a tela de imprimir
        py.click(x=562,y=18)
        tm.sleep(1.5) #antes 2.5



        if  'nao' in verifica_btn_voltar():
            ir_para_pix_novamente()
            continue


        if not verifica_cabecalho_pix():
           ir_para_pix_novamente()
           continue
        

        
        tm.sleep(tempo)

        py.scroll(-1000)

        total_acumulado = total_acumulado + 1

        posY +=25 
        quantidade_comprovantes -= 1
        num_cp += 1

       

        dados.append((cliente,total_acumulado,pagina_atual,posY,etapa))
            
        infoLogs().info(f'posição Y: {posY}')
        
        infoLogs().info(f'pagina atual {pagina_atual}')
    
    if dados:
            try:
                # Atualizar a etapa para 'convenio' se todos os comprovantes foram processados
                if quantidade_comprovantes == 0:  # Verifica se todos os comprovantes foram processados
                    etapa = 'pdf'
                
                # Obtém os últimos dados do processamento
                cliente, total_acumulado_cp, pagina_atual, posY, etapa_atual = dados[-1]
                
                # Atualiza a etapa para salvar na planilha
                salvar_dados_correntes(cliente, total_acumulado_cp, pagina_atual, posY, etapa)
                infoLogs().info(f'Dados enviados para planilha. - Cliente: {cliente}, Etapa: {etapa}')
                return etapa
            except Exception as save_error:
                infoLogs().info(f"Erro ao salvar dados: {save_error}")
    else:
            infoLogs().info(f"Nenhum dado para salvar. - Cliente: {cliente} | Dados: {dados}")
            
    




def ir_para_pix(cliente):

    verificar_tempo_limite()
    
    apenas_dia1 = ""
    apenas_dia2 = ""

    # Posição tela PIX
    tm.sleep(20) #antes tempo
    py.click(x=1073, y=151)

    # Clique em extrato PIX
    tm.sleep(5)
    py.click(x=1090, y=204)

    # Clique 1ª campo data
    tm.sleep(5)#antes 2
    py.click(x=573, y=621)
    tm.sleep(2)

    if "segunda depois das 12h" in verificaSegunda():
        apenas_dia1 = todasDatas()[1].split('.')[0]
        apenas_dia2 = todasDatas()[0].split('.')[0]
    else:
        apenas_dia1 = todasDatas()[0].split('.')[0]
        apenas_dia2 = todasDatas()[1].split('.')[0]

    py.write(apenas_dia1, interval=0.5)
    tm.sleep(1)
    py.write(apenas_dia2, interval=0.5)

    if not verifica_btn_consultar():
        infoLogs().log('Erro ao encontrar o btn_consultar pix\nReiniciando')
        ir_para_pix_novamente()

    # Verificar se tem comprovantes PIX ou não
    # tirarPrintErroPix()
    tm.sleep(30) #antes 5
    py.scroll(-1000, x=509, y=694)
    # tirarPrintPix()
    if  not verifica_total_regis_pix():
        print(f"Não existe comprovantes pix cliente {cliente}")
        print('Encerrando pix')
        atualizar_etapa(cliente,'pdf')
        return

    qntComprovantePix(cliente)
    try:
        total_cp = consultar_progresso(cliente)[4].iloc[0]
                    
        if total_cp > 0:
            if cliente == 'SALGADARIA_3258':
                seleciona_cp_pix('SALGADARIA_3258')

            elif cliente == 'IMPETUS_LTDA_4001':
                seleciona_cp_pix('IMPETUS_LTDA_4001')

            elif cliente == 'IMPETUS_LTDA_5004':
                seleciona_cp_pix('IMPETUS_LTDA_5004')

            elif cliente == 'IMPETUS_LTDA_4097':
                seleciona_cp_pix('IMPETUS_LTDA_4097')

            elif cliente == 'IMPETUS_LTDA_4364':
                seleciona_cp_pix('IMPETUS_LTDA_4364')
            
            elif cliente == 'RECAP_PNEUS_4277':
                seleciona_cp_pix('RECAP_PNEUS_4277')
            
            elif cliente == 'RECAP_PNEUS_3214':
                seleciona_cp_pix('RECAP_PNEUS_3214')

        else:
            print(f"Não existe comprovantes pix cliente {cliente}")
            print('Encerrando pix')
            atualizar_etapa(cliente,'pdf')
            return

    except Exception as e:
        print(f"Erro no sistema Sicoob - PIX \n{e}")

        print('Retomando pix')
        atualizar_etapa(cliente,'pix')
        return



