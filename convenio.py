import pyautogui as py
import time as tm
from datas import todasDatas, verificaSegunda
from extrairTextoPrint import qntComprovanteImposto,erroTextoConvenio
from tirarPrint import tirarPrintErroConvenio
import pyperclip
from acoes import pos_inicio_imposto,verifica_total_regis_convenio,verifica_btn_prox_pagina,verifica_nenhum_cp_selecionado,verifica_btn_gerar_comprovante,verifica_cabecalho_convenio,verifica_btn_consultar,verifica_btn_salvar,verifica_formato_pdf,verifica_btn_salvar_pdf,verifica_btn_voltar
import os
from moverPasta import criar_caminho_onedrive
from pandas_script import salvar_dados_correntes,consultar_progresso,atualizar_etapa
from logger import infoLogs
from processo import refaz_login,refaz_login_cliente




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


def reinicia_processo(cliente):
    infoLogs().info("Encerrando o processo em imposto")
    tm.sleep(3)
    py.click(x=1893,y=13)
    tm.sleep(3)
    tm.sleep(10)
    infoLogs().info(f'Reiniciando processo em imposto cliente - {cliente} ')
    if not refaz_login():
        infoLogs().log(f'Erro no sistema - imposto')
        return False
    
    refaz_login_cliente(cliente)

def cliques_convenio_novamente(cliente, max_tentativas=2): #antes 10
    tempo = 1.5

    for tentativa in range(max_tentativas):
        try:
            # Etapa 1: Clica em convênio
            tm.sleep(5)
            py.click(x=509, y=165)
            tm.sleep(10)

            # Etapa 2: Outro clique
            py.click(x=1488, y=217)
            tm.sleep(30)

            # Etapa 3: Define as datas
            py.click(x=761, y=547)
            py.hotkey('ctrl', 'a', interval=1)
            tm.sleep(tempo)

            if "segunda depois das 12h" in verificaSegunda():
                data1, data2 = todasDatas()[1], todasDatas()[0]
            else:
                data1, data2 = todasDatas()[0], todasDatas()[1]

            py.write(data1, interval=0.1)
            tm.sleep(tempo)
            py.press('tab', presses=2)
            py.hotkey('ctrl', 'a')
            tm.sleep(tempo)
            py.write(data2, interval=0.1)

            # Etapa 4: Clica em consultar
            verifica_btn_consultar()
            tm.sleep(20)

            # Etapa 5: Verifica se encontrou
            if 'sim' in verifica_cabecalho_convenio():
                return True
            else:
                infoLogs().info(f"Tentativa {tentativa+1}/{max_tentativas}: Cabeçalho não encontrado.")
        
        except Exception as e:
            infoLogs().error(f"Erro na tentativa {tentativa+1}: {str(e)}")

    # Se chegou aqui, não conseguiu encontrar
    infoLogs().warning(f"Não foi possível encontrar comprovantes após {max_tentativas} tentativas. Reiniciando processo...")
    reinicia_processo(cliente)
    return False




def seleciona_cp_convenio(cliente):
        
        #retorno da função que pega a primeira posição checkbox
        posX,posY = pos_inicio_imposto()

        troca_pagina = 1
        num_cp = 1
        pagina_atual = 1
        total_cp_acumulado = 1
  
        etapa = 'convenio'
        print(posX,posY)
   
        total_cp = consultar_progresso(cliente)[4].iloc[0]

        quantidade_comprovantes = total_cp
        
        infoLogs().info(f'Total de CP imposto {quantidade_comprovantes}')
        
        total_paginas = quantidade_comprovantes/10
        rest_div = total_paginas%10
        if rest_div > 0 and rest_div < 10:
            total_paginas = total_paginas + 1

        
       
        caminho_base = criar_caminho_onedrive(cliente)
        while quantidade_comprovantes > 0:  
            
            verificar_tempo_limite()
 

            if num_cp >= 11 and int(total_paginas) > 0:
            
                posX,posY = pos_inicio_imposto()
                num_cp = 1
                total_paginas -= 1

                pagina_atual += 1

                troca_pagina = troca_pagina + 1
                

                infoLogs().info(f'Paginas restantes {total_paginas}')


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
                 if cliques_convenio_novamente(cliente):
                      tm.sleep(tempo)
                      continue

            py.click(x=posX, y=posY)  
            print(f'Clicando nno ckeckbox {py.position()}')
            posY += 25

            if 'nao' in verifica_btn_gerar_comprovante():
                cliques_convenio_novamente(cliente)
                continue
          
            nenhum_selecionado = verifica_nenhum_cp_selecionado()
          
            if 'sim' in nenhum_selecionado:
                 infoLogs().info('nenhum comprovante selecionado- reiniciando os cliqus')
                 cliques_convenio_novamente(cliente)
                 continue
                #  valor = 7
                #  while valor > 0:

                #     posY = posY + 20
                #     # #clique na primeira posição
                #     # py.click(x=posX, y=posY)
                    
                #     posX = posX + 20
                #     valor = valor - 1
                #     infoLogs().info(f'clicou: posição x: ',posX,'| posicao y: ',posY)

                 
            

            if not verifica_btn_salvar():
                 cliques_convenio_novamente(cliente)
                 tm.sleep(1)
                 continue
                 

            if 'nao' in verifica_formato_pdf():
                cliques_convenio_novamente(cliente)
                continue

            if 'nao' in verifica_btn_salvar_pdf():
                verifica_btn_salvar_pdf()
                continue

         
           
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

            if 'nao' in verifica_btn_voltar():
                cliques_convenio_novamente(cliente)
                continue
            
          
            

                 
            
            quantidade_comprovantes -= 1
            num_cp += 1
            
            total_cp_acumulado = total_cp_acumulado + 1

            dados.append((cliente,total_cp_acumulado,pagina_atual,posY,etapa))
                 
            infoLogs().info(f'posição X: {posX} | posição Y: {posY}')
            
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
        tm.sleep(5)
        
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


        if not verifica_btn_consultar(): 
            infoLogs().info('Nao localizado o botão consultar | Reiniciando o processo em convenio')
            cliques_convenio_novamente(cliente)

        achou_cabecalho = verifica_cabecalho_convenio()

        if 'sim' in achou_cabecalho:
            
            if not verifica_total_regis_convenio():
                infoLogs().info(f"Nenhum cp encontrado para imposto - Cliente: {cliente}")
                infoLogs().info('Indo para pix')
                atualizar_etapa(cliente,'pix')
                return 

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
                    
                    elif cliente == 'RECAP_PNEUS_4277':
                        seleciona_cp_convenio('RECAP_PNEUS_4277',)

                    elif cliente == 'RECAP_PNEUS_3214':
                        seleciona_cp_convenio('RECAP_PNEUS_3214',)
                    
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

            