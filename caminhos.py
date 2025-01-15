from datas import todasDatas
import subprocess
from criaPasta import  criaPasta
from datetime import datetime



numeroDaConta = '20287-8'
data = todasDatas()[0]
banco = 'SICOOB'
finalPasta = f'{data}_{banco}_{numeroDaConta}'

# Obtém o mês e ano atuais
mes_atual = datetime.now().strftime('%m.%Y')
ano_atual = datetime.now().strftime("%Y")
nome_comprovante = "02. COMPROVANTES DE PAGAMENTO"



CAMINHO_PASTA_PDFS = r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - v2\pdf"

ONE_DRIVE_SALGADARIA =  rf"C:\Users\axlda\iFinance\iFinance - Dados\IFINANCE RIBEIRÃO PRETO\01. CLIENTES\002. SALGADARIA DA ILHA LTA ME\1. ARQUIVADOS\{ano_atual}\{mes_atual}"

ONE_DRIVE_IMPETUS =  rf'C:\Users\axlda\iFinance\iFinance - Dados\IFINANCE RIBEIRÃO PRETO\01. CLIENTES\004. IMPETUS ENERGY E BUSINESS LTDA\1. ARQUIVADOS\02. COMPROVANTES DE PAGAMENTO\{ano_atual}\{mes_atual}'

CAMINHO_EXTRATO_PIX = rf"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - v2\prints\qntExtratoPix.png"

CAMINHO_EXTRATO_IMPOSTO = r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - v2\prints\qnt_comprovanteImposto.png"

CAMINHO_EXTRATO_TITULOS = r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - v2\prints\qnt_comprovante.png"

PASTA_PLANILHAS = r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - v2\planilhas"

CAMINHO_LOGS = rf'C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - v2\Logs'

def caminhoPrograma():
    import pyautogui as py
    import time as tm
    from acoes import verifica_app_sicoob

    py.press('winleft')
    tm.sleep(2)
    # py.scroll(-500)
    verifica_app_sicoob()


