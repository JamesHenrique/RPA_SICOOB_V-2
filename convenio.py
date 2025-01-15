import pyautogui as py
import time as tm
from datas import todasDatas, verificaSegunda
from extrairTextoPrint import qntComprovanteImposto,erroTextoConvenio
from tirarPrint import tirarPrintQntComprovanteImposto,tirarPrintErroConvenio
import pyperclip
from acoes import verifica_btn_prox_pagina,verifica_nenhum_cp_selecionado,verifica_btn_gerar_comprovante,verifica_cabecalho_convenio,verifica_btn_consultar,verifica_btn_salvar,verifica_formato_pdf,verifica_btn_salvar_pdf,verifica_btn_voltar
import os
from moverPasta import criar_caminho_onedrive
from pandas_script import salvar_dados_correntes,consultar_progresso,atualizar_etapa
from logger import infoLogs




import threading
from utils import iniciar_temporizador, verificar_tempo_limite, renovar_sessao, sessao_ativa

# Iniciar a thread de renovação de sessão
thread_renovacao = threading.Thread(target=renovar_sessao, args=(sessao_ativa,), daemon=True)
thread_renovacao.start()

"""
2º etapa

"""


dados = []

tempo = 2.5

def cliques_convenio_novamente():
        data1 = " "
        data2 = " "
        tempo = 1.5

        # clica em convenio

        tm.sleep(5)
        py.click(x=1488, y=217)

        # #clica no 1ª campo da data / 2ª data / clica em consultar
        tm.sleep(tempo)
        py.click(x=761, y=547)
        py.hotkey('ctrl','a',interval=1)
        tm.sleep(tempo)

        if "segunda depois das 12h" in verificaSegunda():
             data1 = todasDatas()[1]
             data2 = todasDatas()[0]
        else:
             data1 = todasDatas()[0]
             data2 = todasDatas()[1]

        py.write(data1,interval=0.1)
        tm.sleep(tempo)
        py.press('tab',presses=2)
        py.hotkey('ctrl','a')
        tm.sleep(tempo)
        py.write(data2,interval=0.1)


        # tm.sleep(tempo)
        # py.click(x=722, y=579,clicks=2)
        verifica_btn_consultar()

        achou_cabecalho = verifica_cabecalho_convenio()

        if 'sim' in achou_cabecalho:

            return True
     
        elif 'nao' in achou_cabecalho:
             tirarPrintQntComprovanteImposto()
             infoLogs().info("Não existe comprovantes de imposto")
             return False




def seleciona_cp_convenio(cliente):
   
        total_cp = consultar_progresso(cliente)[4].iloc[0]

        quantidade_comprovantes = total_cp
        
        total_paginas = quantidade_comprovantes/10
        rest_div = total_paginas%10
        if rest_div > 0 and rest_div < 10:
            total_paginas = total_paginas + 1

        troca_pagina = 1
        num_cp = 1
        pagina_atual = 1
        posY = 557
        posX = 664
        total_cp_acumulado = 1
  
        etapa = 'convenio'
       
        caminho_base = criar_caminho_onedrive(cliente)
        while quantidade_comprovantes > 0:
            
            verificar_tempo_limite()

            posX = 664
            

            if num_cp >= 11 and int(total_paginas) > 0:
                
                posY = 557
                num_cp = 1
                total_paginas -= 1

                pagina_atual += 1

                troca_pagina = troca_pagina + 1
                

                infoLogs().info(f'Paginas restantes {total_paginas}')

               
            # if pagina_atual == 1:
            #         infoLogs().info('teste aqui')
            #         pass
               
            if pagina_atual > 1:
               valor = pagina_atual
               while valor > 1:
                    tm.sleep(2)
                    #clique na primeira posição

                    if not verifica_btn_prox_pagina():
                        py.click(975,879) #-> prox pagina 990,886
                    
                    
                    valor = valor - 1
               
            tm.sleep(tempo)
            infoLogs().info(f'Comprovante {num_cp}º')

            tm.sleep(tempo)

            if 'nao' in verifica_cabecalho_convenio():
                 if cliques_convenio_novamente():
                      tm.sleep(tempo)
                      continue
                 
            valor = 7
            while valor > 0:
                 
                 #clique na primeira posição
                 py.click(x=posX, y=posY)
                
                 posX = posX + 20
                 valor = valor - 1
                 infoLogs().info('clicou: posição x: ',posX,'| posicao y: ',posY)


            

            verifica_btn_gerar_comprovante()
          
            nenhum_selecionado = verifica_nenhum_cp_selecionado()
          
            if 'sim' in nenhum_selecionado:
                 infoLogs().info('nenhum comprovante selecionado')
                 valor = 7
                 while valor > 0:

                    posY = posY + 20
                    # #clique na primeira posição
                    # py.click(x=posX, y=posY)
                    
                    posX = posX + 20
                    valor = valor - 1
                    infoLogs().info('clicou: posição x: ',posX,'| posicao y: ',posY)

                 
            

            if not verifica_btn_salvar():
                 cliques_convenio_novamente()
                 tm.sleep(1)
                 continue
                 

            verifica_formato_pdf()


            verifica_btn_salvar_pdf()

         
           
            nome_arquivo = (f'imposto{quantidade_comprovantes}_{todasDatas()[0]}')
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

            verifica_btn_voltar()
            
          
            

                 
            posY +=25 
            quantidade_comprovantes -= 1
            num_cp += 1
            
            total_cp_acumulado = total_cp_acumulado + 1

            dados.append((cliente,total_cp_acumulado,pagina_atual,posY,etapa))
                 
            infoLogs().info(f'posição Y: {posY}')
            
            infoLogs().info(f'pagina atual {pagina_atual}')


        if dados:
            try:
                # Atualizar a etapa para 'convenio' se todos os comprovantes foram processados
                if quantidade_comprovantes == 0:  # Verifica se todos os comprovantes foram processados
                    etapa = 'pix'
                
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
          

        #atualizar_status(cliente,"IMPOSTO BAIXADOS") #toda vez que terminar de baixar cp vai receber o staus
        
            







def ir_para_convenio(cliente):
        
        verificar_tempo_limite()

        data1 = " "
        data2 = " "
        tempo = 1.5
        

        # #clica em pagamentos
        
        py.click(x=509, y=165)


        # clica em convenio

        tm.sleep(5)
        py.click(x=1488, y=217)

        # #clica no 1ª campo da data / 2ª data / clica em consultar
        tm.sleep(tempo)
        py.click(x=761, y=547)
        py.hotkey('ctrl','a',interval=1)
        tm.sleep(tempo)

        if "segunda depois das 12h" in verificaSegunda():
             data1 = todasDatas()[1]
             data2 = todasDatas()[0]
        else:
             data1 = todasDatas()[0]
             data2 = todasDatas()[1]

        py.write(data1)
        tm.sleep(tempo)
        py.press('tab',presses=2)
        py.hotkey('ctrl','a')
        tm.sleep(tempo)
        py.write(data2)


        verifica_btn_consultar()
        achou_cabecalho = verifica_cabecalho_convenio()

        if 'sim' in achou_cabecalho:
            tirarPrintQntComprovanteImposto()
            tm.sleep(3)

            qntComprovanteImposto(cliente)
            try:
                total_cp = consultar_progresso(cliente)[4].iloc[0]
                    
                if total_cp > 0:

                    if cliente == 'SALGADARIA_3258':
                        seleciona_cp_convenio('SALGADARIA_3258',)

                    elif cliente == 'IMPETUS_LTDA_4001':
                        seleciona_cp_convenio('IMPETUS_LTDA_4001',)

                    elif cliente == 'IMPETUS_LTDA_5004':
                        seleciona_cp_convenio('IMPETUS_LTDA_5004',)
                    
                    elif cliente == 'IMPETUS_LTDA_4097':
                        seleciona_cp_convenio('IMPETUS_LTDA_4097',)

                    elif cliente == 'IMPETUS_LTDA_4364':
                        seleciona_cp_convenio('IMPETUS_LTDA_4364',)
                    
                else:
                    infoLogs().info(f"Nenhum cp encontrado para imposto - Cliente: {cliente}")
                    infoLogs().info('Indo para pix')
                    atualizar_etapa(cliente,'pix')
                    return 
                     
            except Exception as e:
                infoLogs().info(f"Erro no sistema Sicoob - IMPOSTO\n{e}")
                infoLogs().info('Retomando convenio')
                atualizar_etapa(cliente,'convenio')
                return
        else:
            infoLogs().info(f"2 - Nao existe cp de imposto para periodo informado - Cliente {cliente}")
            infoLogs().info('Indo para pix')
            atualizar_etapa(cliente,'pix')
            return 

            

