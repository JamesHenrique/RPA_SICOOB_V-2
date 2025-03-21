import pyautogui as py
import time as tm
from datas import todasDatas,verificaSegunda
from moverPasta import criar_caminho_onedrive
from extrairTextoPrint import qntComprovante

import pyperclip
from acoes import verifica_total_regis_titulos,verifica_btn_iniciar_cinza,verifica_btn_inicio,verifica_btn_gerar_comprovante,verifica_btn_voltar,verifica_btn_salvar,verifica_btn_prox_pagina,verifica_btn_salvar_pdf,verifica_formato_pdf,verifica_btn_consultar,verifica_cabecalho_convenio
import os
from pandas_script import filtro_clientes,consultar_progresso,salvar_dados_correntes,atualizar_etapa
from logger import infoLogs


import threading
from utils import verificar_tempo_limite, renovar_sessao, sessao_ativa

# Iniciar a thread de renovação de sessão
thread_renovacao = threading.Thread(target=renovar_sessao, args=(sessao_ativa,), daemon=True)
thread_renovacao.start()






"""
2º etapa

"""

dados = []

tempo = 1

# def reiniciar_processo():
   
#     seguir = ''

#     clientes_abertos = filtro_clientes()

#     for i in clientes_abertos:
#         if not i:
#             print(f'nenhum cliente encontrado')
#             seguir = 'nao'
#             break
#         else:
#             seguir = 'sim'

#     infoLogs().info(f'seguir: {seguir}')
        
#     if seguir == 'sim':
#         # Exibe os clientes que estão abertos para consulta
#         infoLogs().info(f"Reiniciando a consulta para os clientes -> {clientes_abertos}")

#         tm.sleep(2)

#         fazerLogin()

    
#     else:
#         infoLogs().info('PROCESSO FINALIZADO')
#         tm.sleep(3)
#         py.click(x=1893, y=13)



def ir_para_titulos_novamente():

    verificar_tempo_limite()

    data1 = ""
    data2 = ""

    tempo = 3


    # #clica em pagamentos
    
    py.click(x=509, y=165)

    # clica em titulos

    tm.sleep(tempo)
    py.click(x=1443, y=204)

    #clica no 1ª campo da data / 2ª data / clica em consultar
    tm.sleep(tempo)
    py.click(x=761, y=547)
    py.hotkey('ctrl','a')
    tm.sleep(tempo)

    if "segunda depois das 12h" in verificaSegunda():
        data1 = todasDatas()[1]
        data2 = todasDatas()[0]
    else:
        data1 = todasDatas()[0]
        data2 = todasDatas()[1]

    py.write(data1)
    tm.sleep(1.5)
    py.press('tab',presses=2)
    py.hotkey('ctrl','a')
    tm.sleep(1.5)
    py.write(data2)


    # tm.sleep(tempo)
    # py.click(x=722, y=579,clicks=2)

    verifica_btn_consultar()
    achou_cabecalho = verifica_cabecalho_convenio()
    if 'sim' in achou_cabecalho:
        infoLogs().info('Continuando processo titulos')
        return True
    
    else:
        #reinicia o processo
        infoLogs().info('REINICIANDO O PROCESSO EM TITULOS')
        # reiniciar_processo()


def seleciona_cp_titulos(cliente):
        
        
        total_cp = consultar_progresso(cliente)[4].iloc[0]

        quantidade_comprovantes = total_cp

        infoLogs().info(f'Total de CP titulos {quantidade_comprovantes}')

        total_paginas = quantidade_comprovantes/10
        rest_div = total_paginas%10
        if rest_div > 0 and rest_div < 10:
            total_paginas = total_paginas + 1
        
       
        num_cp = 1
        pagina_atual = 1
        posY = 557
        total_acumulado_cp = 0
        etapa = 'titulos'
        
        
        caminho_base = criar_caminho_onedrive(cliente)

        while quantidade_comprovantes > 0:

            
            verificar_tempo_limite()

            if num_cp >= 11 and int(total_paginas) > 0:
                posY = 557
                num_cp = 1
                total_paginas -= 1
                pagina_atual += 1


                infoLogs().info(f'Paginas restantes {total_paginas}')

         
            if pagina_atual > 1:
               valor = pagina_atual
               print('valor pagina atual valor', valor)
               while valor > 1:
                    
                    
                    tm.sleep(2)
                    #clique na primeira posição
                    if not verifica_btn_prox_pagina():
                        py.click(975,879) #-> prox pagina 990,886
                    infoLogs().info(f'Valor da pagina {valor}')
            
                    valor = valor - 1
                    

            tm.sleep(tempo)
            
            infoLogs().info(f'Comprovante {num_cp}º')

            tm.sleep(tempo)

            if 'nao' in verifica_cabecalho_convenio():
                 
                 ir_para_titulos_novamente()
                 tm.sleep(tempo)
                 continue

            #clique na primeira posição
            py.click(x=703, y=posY)
            tm.sleep(tempo)


            if 'nao' in verifica_btn_gerar_comprovante():
                ir_para_titulos_novamente()
                continue


            if not verifica_btn_salvar():
                ir_para_titulos_novamente()
                continue
                
          
     
            if 'nao' in verifica_formato_pdf():
                ir_para_titulos_novamente()
                continue
                

            if 'nao' in verifica_btn_salvar_pdf():
                verifica_btn_salvar_pdf()
                continue




            nome_arquivo = (f'titulos{quantidade_comprovantes}_{todasDatas()[0]}')
            tm.sleep(0.5)

            caminho_completo = os.path.join(caminho_base, nome_arquivo)
            tm.sleep(0.5)
           

            # Copiar o caminho completo para a área de transferência e colar (opcional)
            pyperclip.copy(caminho_completo)

            tm.sleep(0.5)
            py.hotkey('ctrl','v')

            tm.sleep(0.5)
    

            py.press('enter')
            tm.sleep(1)
            py.press('enter')
            tm.sleep(1)

     

            if 'nao' in verifica_btn_voltar():
                ir_para_titulos_novamente()
                continue
            
            

            total_acumulado_cp = total_acumulado_cp + 1

            posY +=25 
            quantidade_comprovantes -= 1
            num_cp += 1

            dados.append((cliente,total_acumulado_cp,pagina_atual,posY,etapa))

            infoLogs().info(f'posição Y: {posY}')
            
            infoLogs().info(f'pagina atual {pagina_atual}')

        
        if dados:
            try:
                # Atualizar a etapa para 'convenio' se todos os comprovantes foram processados
                if quantidade_comprovantes == 0:  # Verifica se todos os comprovantes foram processados
                    etapa = 'convenio'
                
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
                
        
        # atualizar_status(cliente,"convenio") #toda vez que terminar de baixar cp vai receber o staus
            



def ir_para_titulos(cliente):

    verificar_tempo_limite()

    data1 = ""
    data2 = ""

    tempo = 3

    achou_inicio = verifica_btn_inicio()

    
    if 'nao' in achou_inicio:
        # if verifica_btn_iniciar_cinza():
        #     return 
        
        py.click(x=1893,y=13)
        tm.sleep(3)
        infoLogs().info('erro ao apos o login - ')

        ir_para_titulos_novamente()
            
            
    # #clica em pagamentos
    
    py.click(x=509, y=165)

    # clica em titulos

    tm.sleep(tempo)
    py.click(x=1443, y=204)

    #clica no 1ª campo da data / 2ª data / clica em consultar
    tm.sleep(tempo)
    py.click(x=761, y=547)
    py.hotkey('ctrl','a')
    tm.sleep(tempo)

    if "segunda depois das 12h" in verificaSegunda():
        data1 = todasDatas()[1]
        data2 = todasDatas()[0]
    else:
        data1 = todasDatas()[0]
        data2 = todasDatas()[1]

    py.write(data1)
    tm.sleep(1.5)
    py.press('tab',presses=2)
    py.hotkey('ctrl','a')
    tm.sleep(1.5)
    py.write(data2)


    # tm.sleep(tempo)
    # py.click(x=722, y=579,clicks=2)

    if not verifica_btn_consultar(): 
        infoLogs().info('Nao localizado o botão consultar | Reiniciando o processo em titulos')
        ir_para_titulos_novamente()

    achou_cabecalho = verifica_cabecalho_convenio()
    if 'sim' in achou_cabecalho:

        if not verifica_total_regis_titulos():
            infoLogs().info(f"Nenhum cp encontrado para titulos - Cliente: {cliente}")
            atualizar_etapa(cliente,'convenio')
            return


        tm.sleep(tempo)
        
        qntComprovante(cliente)
        try:
            total_cp = consultar_progresso(cliente)[4].iloc[0]
            
            total_cp = int(total_cp)

            if total_cp > 0:

                if cliente == 'SALGADARIA_3258':
                    seleciona_cp_titulos('SALGADARIA_3258')

                elif cliente == 'IMPETUS_LTDA_4001':
                    seleciona_cp_titulos('IMPETUS_LTDA_4001')

                elif cliente == 'IMPETUS_LTDA_5004':
                    seleciona_cp_titulos('IMPETUS_LTDA_5004')
                
                elif cliente == 'IMPETUS_LTDA_4097':
                    seleciona_cp_titulos('IMPETUS_LTDA_4097')

                elif cliente == 'IMPETUS_LTDA_4364':
                    seleciona_cp_titulos('IMPETUS_LTDA_4364')
                
                elif cliente == 'RECAP_PNEUS_4277':
                    seleciona_cp_titulos('RECAP_PNEUS_4277')

                elif cliente == 'RECAP_PNEUS_3214':
                    seleciona_cp_titulos('RECAP_PNEUS_3214')
                
            else:
                infoLogs().info(f"Nenhum cp encontrado para titulos - Cliente: {cliente}")
                atualizar_etapa(cliente,'convenio')
                return 
        except Exception as e:
            infoLogs().info(f"Erro no sistema Sicoob - TITULOS 2 {e}")
            atualizar_etapa(cliente,'titulos')
            return
    else:
        infoLogs().info("Nao existe cp de Titulos para periodo informado")
        atualizar_etapa(cliente,'convenio')
        return
    

