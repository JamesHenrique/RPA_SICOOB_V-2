import tkinter as tk
import pandas as pd
from datetime import datetime
from login import iniciar_clientes, fazerLogin
from pandas_script import filtro_clientes
from renomeiPDF import renomearPdfs, renomearPix, renomeiImposto
from moverPasta import moveArquivoOneDrive
from criaPasta import criaPasta
import time as tm
import os

from caminhos import PASTA_PLANILHAS

def iniciar_tela():
    try:
        # Variável para controlar o retorno baseado no fechamento da janela
        window_closed = False

        # Função para selecionar ou desmarcar todos os checkboxes
        def selecionar_todos():
            novo_estado = not var_opcao1.get()  # Baseado no primeiro checkbox
            var_opcao1.set(novo_estado)
            var_opcao2.set(novo_estado)
            var_opcao3.set(novo_estado)
            var_opcao4.set(novo_estado)
            var_opcao5.set(novo_estado)
            atualizar_estado_botao()  # Atualizar o estado do botão após alterar os checkboxes

        # Função para obter os valores selecionados
        def obter_valores():
            valores_selecionados = []
            # Verificar os valores dos checkboxes
            if var_opcao1.get():
                valores_selecionados.append("SALGADARIA_3258")
            if var_opcao2.get():
                valores_selecionados.append("IMPETUS_LTDA_4001")
            if var_opcao3.get():
                valores_selecionados.append("IMPETUS_LTDA_5004")
            if var_opcao4.get():
                valores_selecionados.append("IMPETUS_LTDA_4097")
            if var_opcao5.get():
                valores_selecionados.append("IMPETUS_LTDA_4364")

            data = datetime.now().strftime("%d-%m-%Y")

            # Dados iniciais
            cp = ''
            pagina = ''
            posY = ''
            total_cp = ''
            etapa = 'titulos'
            status = 'Em andamento'

            df = pd.DataFrame({
                'clientes': valores_selecionados,
                'cp': cp,
                'pagina': pagina,
                'posY': posY,
                'total_cp': total_cp,
                'etapa': etapa,
                'status': status,
                'data_consulta': data
            })

            arquivo_planilha = os.path.join(PASTA_PLANILHAS, 'devolutivas.xlsx')

            try:
                if os.path.exists(arquivo_planilha):
                    # Carregar planilha existente
                    existente = pd.read_excel(arquivo_planilha)
                    # Concatenar com os novos dados
                    df = pd.concat([existente, df], ignore_index=True)
                    print('Planilha carregada e atualizada.')
                else:
                    print('Planilha não encontrada. Criando uma nova...')
                
                # Salvar os dados no arquivo Excel
                df.to_excel(arquivo_planilha, index=False)
                print('Planilha salva com sucesso.')

            except Exception as e:
                print(f'Ocorreu um erro ao manipular a planilha: {e}')

            existente = pd.read_excel(fr'{PASTA_PLANILHAS}\devolutivas.xlsx')
            
            janela.destroy()  # Fechar a janela após salvar os valores

            tm.sleep(2)

            fazerLogin()
            
            iniciar_clientes()  # Inicia a varredura da planilha para verificar os clientes selecionados

        # Função para repetir a informação da planilha
        def repetir_info_planilha():
            # Chama a função filtro_clientes() para obter os clientes filtrados

            try:
                clientes_abertos = filtro_clientes()

            except Exception as e:
          
                print(f'Nao existe informações na planilha para continuar {e}')
                return 'finalizado'

            if clientes_abertos:
                # Exibe os clientes que estão abertos para consulta
                print("Reiniciando a consulta para os clientes:")
                print(clientes_abertos)
                
                janela.destroy()  # Fechar a janela após repetir as informações da planilha

                tm.sleep(2)

                fazerLogin()

                # Inicia o processo novamente com esses clientes
                iniciar_clientes()  # Chama a função que você usa para iniciar o processo de consulta

        # Função para repetir a informação da planilha
        def renomear_pdfs_novamente():
            pastas = [
                criaPasta(0),
                criaPasta(1),
                criaPasta(2),
                criaPasta(3),
                criaPasta(4)
            ]

            # Renomear arquivos em cada pasta
            renomearPdfs(pastas)
            renomeiImposto(pastas)
            renomearPix(pastas)

            moveArquivoOneDrive('IMPETUS_LTDA_4001')
            moveArquivoOneDrive('IMPETUS_LTDA_5004')
            moveArquivoOneDrive('SALGADARIA_3258')
            moveArquivoOneDrive('IMPETUS_LTDA_4097')
            moveArquivoOneDrive('IMPETUS_LTDA_4364')

            # janela.destroy()  # Fechar a janela após repetir as informações da planilha

        # Função para lidar com o evento de fechamento da janela
        def on_closing():
            nonlocal window_closed
            print("Janela fechada pelo usuário.")
            window_closed = True
            janela.destroy()

        # Função para atualizar o estado do botão com base nos checkboxes
        def atualizar_estado_botao():
            # Habilitar o botão se pelo menos um checkbox estiver marcado
            if var_opcao1.get() or var_opcao2.get() or var_opcao3.get() or var_opcao4.get() or var_opcao5.get():
                btn_obter.config(state=tk.NORMAL)
            else:
                btn_obter.config(state=tk.DISABLED)

        # Criar a janela principal
        janela = tk.Tk()
        janela.title("Seleção de Opções")
        janela.geometry("500x500")

        # Definir o comportamento ao fechar a janela
        janela.protocol("WM_DELETE_WINDOW", on_closing)

        # Variáveis para os checkboxes
        var_opcao1 = tk.BooleanVar()
        var_opcao2 = tk.BooleanVar()
        var_opcao3 = tk.BooleanVar()
        var_opcao4 = tk.BooleanVar()
        var_opcao5 = tk.BooleanVar()

        # Criar os checkboxes com comando para atualizar o estado do botão
        tk.Checkbutton(janela, text="SALGADARIA_3258", variable=var_opcao1, command=atualizar_estado_botao).pack()
        tk.Checkbutton(janela, text="IMPETUS ENERGY E BUSINESS LTDA_4001", variable=var_opcao2, command=atualizar_estado_botao).pack()
        tk.Checkbutton(janela, text="IMPETUS ENERGY E BUSINESS LTDA_5004", variable=var_opcao3, command=atualizar_estado_botao).pack()
        tk.Checkbutton(janela, text="IMPETUS ENERGY E BUSINESS LTDA_4097", variable=var_opcao4, command=atualizar_estado_botao).pack()
        tk.Checkbutton(janela, text="IMPETUS ENERGY E BUSINESS LTDA_4364", variable=var_opcao5, command=atualizar_estado_botao).pack()

        # Criar o botão para obter os valores selecionados, desabilitado inicialmente
        btn_obter = tk.Button(janela, text="Obter Selecionados", command=obter_valores, state=tk.DISABLED)
        btn_obter.pack()

        # Botão para selecionar ou desmarcar todos
        tk.Button(janela, text="Selecionar Todos", command=selecionar_todos).pack()

        # Botão para repetir as informações da planilha
        tk.Button(janela, text="Repetir info da planilha", command=repetir_info_planilha).pack()

        # Botão para renomear os PDFs novamente
        tk.Button(janela, text="Renomear-Substituir CPs", command=renomear_pdfs_novamente).pack()

        # Iniciar o loop da interface gráfica
        janela.mainloop()

        # Verifica se a janela foi fechada pelo usuário
        if window_closed:
            return 'nao'
        else:
            return 'seguir'
    except Exception as e:
        print(f'Erro ao executar tela: {e}')
        return 'nao'

