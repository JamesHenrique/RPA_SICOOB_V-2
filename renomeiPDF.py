

from datas import todasDatas
from PyPDF2 import PdfReader
import re
import os

from moverPasta import criar_caminho_onedrive

from logger import infoLogs



def gerar_nome_com_sufixo_unico(caminho, nome_base, no_agendamento_novo):
    sufixo = 0
    while True:
        sufixo_txt = f"_V{sufixo}" if sufixo > 0 else ""
        nome_tentativa = f"{nome_base}{sufixo_txt}.pdf"
        caminho_tentativa = os.path.join(caminho, nome_tentativa)

        if os.path.exists(caminho_tentativa):
            if verificar_no_agendamento(caminho_tentativa, no_agendamento_novo):
                return None, None  # Já existe com o mesmo No. Agendamento → pular
        else:
            return nome_tentativa, caminho_tentativa  # Nome livre com agendamento novo
        sufixo += 1


# Função para extrair texto de uma página específica
def extract_text_from_page(pdf_reader, page_number):
    page = pdf_reader.pages[page_number]
    text = page.extract_text()
    return text

# Função para extrair campos específicos usando expressões regulares
def extract_fields(text, pattern):
    matches = re.findall(pattern, text)
    return matches

# Função para remover caracteres inválidos do nome do arquivo
def sanitize_filenamev2(filename):
    if isinstance(filename, list):  # Verifica se é uma lista e pega o primeiro elemento
        filename = filename[0] if filename else ""
    return re.sub(r'[<>:"/\\|?*\n\r]+', '_', str(filename))

# Função para verificar se os valores de No. Agendamento são iguais
def verificar_no_agendamento(caminho_existente, no_agendamento_novo):
    with open(caminho_existente, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            text = extract_text_from_page(pdf_reader, page_num)
            no_agendamento_existente = extract_fields(text, r'No\. Agendamento:\s*(.*?)\s+Instituição Emissora:')
            if no_agendamento_existente:
                return no_agendamento_existente == no_agendamento_novo
    return False

def renomearPdfs(pastas):
    nome_pattern = r'Nome/Razão Social do Beneficiário:\s*(.*)'
    valor_pattern = r'Valor Pago:\s*([\d.,]+)'
    no_agendamento_pattern = r'No\. Agendamento:\s*(.*?)\s+Instituição Emissora:'

    infoLogs().info(f'Etapa renomear TITULOS iniciada')
    for caminho in pastas:
        for filename in os.listdir(caminho):
            if (filename.startswith('titulos') or filename.startswith('TITULOS')) and filename.endswith('.pdf'):
                file_path = os.path.join(caminho, filename)
                try:
                    with open(file_path, 'rb') as pdf_file:
                        pdf_reader = PdfReader(pdf_file)

                        nome_beneficiario = None
                        valor_documento = None
                        no_agendamento = None

                        for page_num in range(len(pdf_reader.pages)):
                            text = extract_text_from_page(pdf_reader, page_num)
                            if not nome_beneficiario:
                                nome_beneficiario = extract_fields(text, nome_pattern)
                            if not valor_documento:
                                valor_documento = extract_fields(text, valor_pattern)
                            if not no_agendamento:
                                no_agendamento = extract_fields(text, no_agendamento_pattern)

                    if nome_beneficiario and valor_documento and no_agendamento:
                        nome_beneficiario = sanitize_filenamev2(nome_beneficiario)[:20]
                        if isinstance(valor_documento, list) and len(valor_documento) > 0:
                            valor_documento = valor_documento[0]

                        nome_base = f"{todasDatas()[0]}_CP_{nome_beneficiario}_R${valor_documento}"
                        novo_nome, novo_caminho = gerar_nome_com_sufixo_unico(caminho, nome_base, no_agendamento)

                        if not novo_nome:
                            infoLogs().info(f"TITULOS - Arquivo já existe com o mesmo No. Agendamento: {nome_base}. Pulando...")
                            continue

                        os.rename(file_path, novo_caminho)
                        infoLogs().info(f"TITULOS - Renomeado: {filename} para {novo_nome}")
                    else:
                        infoLogs().info(f"TITULOS - Campos não encontrados em: {filename}")
                except PermissionError:
                    infoLogs().info(f"TITULOS - O arquivo está sendo usado por outro processo: {file_path}")
                except Exception as e:
                    infoLogs().info(f"TITULOS - Erro ao processar {filename}: {e}")

    infoLogs().info(f'Etapa renomear TITULOS finalizada')
                    
def verificar_agendamento_duplicado(caminho_existente, agendamento_novo):
    try:
        with open(caminho_existente, 'rb') as f:
            leitor = PdfReader(f)
            texto = ''.join(p.extract_text() for p in leitor.pages)
            agendamento_existente = re.findall(r'(?:No\. Agendamento:|NÚMERO DO AGENDAMENTO:)\s*(.*?)\s+(?:Instituição Emissora:|BANCO EMISSOR:)?', texto)
            if agendamento_existente:
                return agendamento_existente[0].strip() == agendamento_novo.strip()
    except:
        pass
    return False

def gerar_nome_unico_para_imposto_com_agendamento(caminho, nome_base, agendamento_novo):
    sufixo = 0
    while True:
        sufixo_txt = f"_V{sufixo}" if sufixo > 0 else ""
        nome_tentativa = f"{nome_base}{sufixo_txt}.pdf"
        caminho_tentativa = os.path.join(caminho, nome_tentativa)

        if os.path.exists(caminho_tentativa):
            if verificar_agendamento_duplicado(caminho_tentativa, agendamento_novo):
                return None, None  # Arquivo igual já existe
            else:
                sufixo += 1  # Conteúdo diferente, tenta com novo sufixo
        else:
            return nome_tentativa, caminho_tentativa

def renomeiImposto(pastas):
    padrao_comprovante = r'COMPROVANTE DE (?:PAGAMENTO(?: - SIMPLES NACIONAL| DARF)?|AGENDAMENTO - SIMPLES NACIONAL|AGENDAMENTO DE CONVÊNIO)'
    padrao_valor = r'(?:VALOR TOTAL|VALOR):\s*([\d.,]+)'
    padrao_convenio = r'Convênio:\s*([^\n\r]+)'
    padrao_agendamento = r'(?:No\. Agendamento:|NÚMERO DO AGENDAMENTO:)\s*(.*?)\s+(?:Instituição Emissora:|BANCO EMISSOR:)?'

    infoLogs().info(f'Etapa renomear IMPOSTO iniciada')
    for caminho in pastas:
        for nome_arquivo in os.listdir(caminho):
            if nome_arquivo.lower().startswith('imposto') and nome_arquivo.lower().endswith('.pdf'):
                caminho_arquivo = os.path.join(caminho, nome_arquivo)

                try:
                    with open(caminho_arquivo, 'rb') as arquivo:
                        leitor_pdf = PdfReader(arquivo)
                        texto = ''.join(pagina.extract_text() for pagina in leitor_pdf.pages)

                    resultado_comprovante = re.search(padrao_comprovante, texto, re.IGNORECASE)
                    resultado_valor = re.search(padrao_valor, texto, re.IGNORECASE)
                    resultado_convenio = re.search(padrao_convenio, texto, re.IGNORECASE)
                    resultado_agendamento = re.search(padrao_agendamento, texto, re.IGNORECASE)

                    if resultado_valor and resultado_agendamento:
                        valor_total = resultado_valor.group(1).replace('.', '').replace(',', '.')
                        agendamento = resultado_agendamento.group(1).strip()

                        if resultado_convenio:
                            nome = resultado_convenio.group(1).strip().upper()
                        elif resultado_comprovante:
                            nome = resultado_comprovante.group(0).strip().upper()
                        else:
                            nome = "SEM_NOME"

                        nome = sanitize_filename(nome)[:20]
                        nome_base = f'{todasDatas()[0]}_CP_{nome}_R${valor_total}'.replace(' ', '_')

                        novo_nome_arquivo, novo_caminho_arquivo = gerar_nome_unico_para_imposto_com_agendamento(
                            caminho, nome_base, agendamento
                        )

                        if not novo_nome_arquivo:
                            infoLogs().info(f'IMPOSTO - Arquivo já existe com mesmo agendamento: {nome_base}.pdf')
                            continue

                        os.rename(caminho_arquivo, novo_caminho_arquivo)
                        infoLogs().info(f'IMPOSTO - Arquivo renomeado para: {novo_nome_arquivo}')
                    else:
                        infoLogs().info(f'IMPOSTO - Valor ou agendamento não encontrado no arquivo: {nome_arquivo}')
                except Exception as e:
                    infoLogs().error(f'IMPOSTO - Erro ao processar o arquivo {nome_arquivo}: {str(e)}')
            else:
                infoLogs().info(f'IMPOSTO - Arquivo não corresponde ao padrão: {nome_arquivo}')

    infoLogs().info(f'Etapa renomear IMPOSTO finalizada')



def extrair_id_transacao_pdf(caminho_pdf):
    try:
        with open(caminho_pdf, 'rb') as f:
            leitor = PdfReader(f)
            texto = ''.join(p.extract_text() for p in leitor.pages)
            resultado = re.search(r'ID Transação:\s*(\S+)', texto)
            if resultado:
                return resultado.group(1).strip()
    except:
        pass
    return None

def renomearPix(pastas):
    def extrair_texto_pdf(caminho_pdf):
        with open(caminho_pdf, 'rb') as arquivo_pdf:
            leitor_pdf = PdfReader(arquivo_pdf)
            texto_total = ''
            for pagina in leitor_pdf.pages:
                texto_total += pagina.extract_text()
        return texto_total

    def extrair_informacoes(texto):
        valor_pagamento_match = re.search(r'Valor do\s+Pagamento:\s*([\d.,]+)', texto)
        valor_pagamento = valor_pagamento_match.group(1) if valor_pagamento_match else None

        nome_destinatario_matches = re.findall(r'Nome:\s*(.+)', texto)
        nome_destinatario = nome_destinatario_matches[1] if len(nome_destinatario_matches) > 1 else None

        id_transacao_match = re.search(r'ID Transação:\s*(\S+)', texto)
        id_transacao = id_transacao_match.group(1) if id_transacao_match else None

        return valor_pagamento, nome_destinatario, id_transacao

    def gerar_nome_unico_para_pix(caminho, nome_base, id_novo):
        sufixo = 0
        while True:
            sufixo_txt = f"_V{sufixo}" if sufixo > 0 else ""
            nome_tentativa = f"{nome_base}{sufixo_txt}.pdf"
            caminho_tentativa = os.path.join(caminho, nome_tentativa)

            if os.path.exists(caminho_tentativa):
                id_existente = extrair_id_transacao_pdf(caminho_tentativa)
                if id_existente == id_novo:
                    return None, None  # Arquivo já existe com mesmo conteúdo
                else:
                    sufixo += 1
            else:
                return nome_tentativa, caminho_tentativa

    infoLogs().info(f'Etapa renomear PIX iniciada')

    for caminho in pastas:
        for nome_arquivo in os.listdir(caminho):
            if nome_arquivo.lower().startswith('pix') and nome_arquivo.lower().endswith('.pdf'):
                caminho_pdf = os.path.join(caminho, nome_arquivo)
                try:
                    texto_pdf = extrair_texto_pdf(caminho_pdf)
                    valor_pagamento, nome_destinatario, id_transacao = extrair_informacoes(texto_pdf)

                    if not all([valor_pagamento, nome_destinatario, id_transacao]):
                        infoLogs().info(f"DADOS INCOMPLETOS - {nome_arquivo}. Pulando...")
                        continue

                    nome_destinatario = sanitize_filename(nome_destinatario[:20])
                    valor_pagamento = valor_pagamento.replace(",", ".")

                    nome_base = f"{todasDatas()[0]}_CP_{nome_destinatario}_R${valor_pagamento}".replace(' ', '_')

                    novo_nome_pdf, caminho_novo_pdf = gerar_nome_unico_para_pix(caminho, nome_base, id_transacao)

                    if not novo_nome_pdf:
                        infoLogs().info(f'PIX - Já existe: {nome_base}.pdf com mesmo ID. Pulando...')
                        continue

                    os.rename(caminho_pdf, caminho_novo_pdf)
                    infoLogs().info(f'PIX - Arquivo renomeado para: {novo_nome_pdf}')
                except Exception as e:
                    infoLogs().error(f'PIX - Erro ao processar {nome_arquivo}: {str(e)}')

    infoLogs().info(f'Etapa renomear PIX finalizada')


 

# Função para remover caracteres inválidos do nome do arquivo
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\n\r]+', '_', filename)


# pastas = [R'C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - v2\TESTE_CP']


# pastas = [
    
#                 rf"C:\Users\axlda\iFinance\iFinance - Dados\IFINANCE RIBEIRÃO PRETO\01. CLIENTES\002. SALGADARIA DA ILHA LTDA ME\1. ARQUIVADOS\2025\04.2025\02. COMPROVANTES DE PAGAMENTO\22.04.2025_SICOOB_20287-8",
       
          
#             ]
# renomearPdfs(pastas)
# renomearPix(pastas)
# renomeiImposto(pastas)

# print(criar_caminho_onedrive('RECAP_PNEUS_3214'))




