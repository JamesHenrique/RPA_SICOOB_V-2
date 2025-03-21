

from datas import todasDatas
from PyPDF2 import PdfReader
import re
import os

from moverPasta import criar_caminho_onedrive

from logger import infoLogs

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

# Função principal para renomear PDFs
def renomearPdfs(pastas):
    # Padrões para buscar os campos específicos
    nome_pattern = r'Nome/Razão Social do Beneficiário:\s*(.*)'
    #antes valor_pattern = r'Valor Documento:\s*([\d.,]+)'
    valor_pattern = r'Valor Pago:\s*([\d.,]+)'
    no_agendamento_pattern = r'No\. Agendamento:\s*(.*?)\s+Instituição Emissora:'

    infoLogs().info(f'Etapa renomear TITULOS iniciada')
    for caminho in pastas:
        for filename in os.listdir(caminho):
            if (filename.startswith('titulos') or filename.startswith('TITULOS')) and filename.endswith('.pdf'):
                file_path = os.path.join(caminho, filename)
                try:
                    # Lê o conteúdo do PDF antes de tentar renomear
                    with open(file_path, 'rb') as pdf_file:
                        pdf_reader = PdfReader(pdf_file)

                        nome_beneficiario = None
                        valor_documento = None
                        no_agendamento = None

                        # Extrai texto de todas as páginas e busca os campos específicos
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
                        # Extrair o primeiro valor da lista se necessário
                        if isinstance(valor_documento, list) and len(valor_documento) > 0:
                            valor_documento = valor_documento[0]

                        # Define o novo nome do arquivo
                        novo_nome = f"{todasDatas()[0]}_CP_{nome_beneficiario}_R${valor_documento}.pdf"
                        novo_caminho = os.path.join(caminho, novo_nome)

                        # Verifica se o arquivo já existe
                        if os.path.exists(novo_caminho):
                            if verificar_no_agendamento(novo_caminho, no_agendamento):
                                infoLogs().info(f"TITULOS - Arquivo já existe com o mesmo No. Agendamento: {novo_nome}. Pulando...")
                                continue
                            else:
                                # No. Agendamento diferente, adicionar sufixo "_V2"
                                novo_nome = f"{todasDatas()[0]}_CP_{nome_beneficiario}_R${valor_documento}_V2.pdf"
                                novo_caminho = os.path.join(caminho, novo_nome)

                        # Renomear o arquivo
                        os.rename(file_path, novo_caminho)
                        infoLogs().info(f"TITULOS - Renomeado: {filename} para {novo_nome}")
                    else:
                        infoLogs().info(f"TITULOS - Campos não encontrados em: {filename}")
                except PermissionError:
                    infoLogs().info(f"TITULOS - O arquivo está sendo usado por outro processo: {file_path}")
                except Exception as e:
                    infoLogs().info(f"TITULOS - Erro ao processar {filename}: {e}")

    infoLogs().info(f'Etapa renomear TITULOS finalizada')
                    
def renomeiImposto(pastas):
    # Padrões de regex
    padrao_comprovante = r'COMPROVANTE DE (?:PAGAMENTO(?: - SIMPLES NACIONAL| DARF)?|AGENDAMENTO - SIMPLES NACIONAL|AGENDAMENTO DE CONVÊNIO)'
    padrao_valor = r'VALOR TOTAL:\s*([\d.,]+)'
    padrao_convenio = r'Convênio:\s*([^\n\r]+)'

    infoLogs().info(f'Etapa renomear IMPOSTO iniciada')
    for caminho in pastas:
        # Percorre todos os arquivos na pasta
        for nome_arquivo in os.listdir(caminho):
            if nome_arquivo.lower().startswith('imposto') and nome_arquivo.lower().endswith('.pdf'):
                # infoLogs().info(f'Imposto - Verificando arquivo: {nome_arquivo}')
                caminho_arquivo = os.path.join(caminho, nome_arquivo)
                
                # Abra o arquivo PDF
                try:
                    with open(caminho_arquivo, 'rb') as arquivo:
                        leitor_pdf = PdfReader(arquivo)
                        texto = ''

                        # Itera sobre cada página do PDF
                        for pagina in leitor_pdf.pages:
                            texto += pagina.extract_text()

                    # Procura pelos padrões no texto extraído
                    resultado_comprovante = re.search(padrao_comprovante, texto, re.IGNORECASE)
                    resultado_valor = re.search(padrao_valor, texto, re.IGNORECASE)
                    resultado_convenio = re.search(padrao_convenio, texto, re.IGNORECASE)

                    if resultado_valor:
                        valor_total = resultado_valor.group(1).replace('.', '').replace(',', '.')

                        # Nome do convênio ou comprovante
                        if resultado_convenio:
                            nome = resultado_convenio.group(1).strip().upper()  # Nome do convênio em maiúsculas
                        elif resultado_comprovante:
                            nome = resultado_comprovante.group(0).strip().upper()
                        else:
                            nome = "SEM_NOME"  # Nome padrão caso nenhum seja encontrado

                        # Sanitize o nome para remover caracteres inválidos
                        nome = sanitize_filename(nome)[:20]

                        # Gera o novo nome do arquivo
                        novo_nome_arquivo = f'{todasDatas()[0]}_CP_{nome}_R$ {valor_total}.pdf'.replace(' ', '_')
                        novo_caminho_arquivo = os.path.join(caminho, novo_nome_arquivo)

                        # Verifica se o arquivo já existe
                        if os.path.exists(novo_caminho_arquivo):
                            infoLogs().info(f'IMPOSTO - Arquivo já existe e não será renomeado: {novo_nome_arquivo}')
                        else:
                            # Renomeia o arquivo
                            os.rename(caminho_arquivo, novo_caminho_arquivo)
                            infoLogs().info(f'IMPOSTO - Arquivo renomeado para: {novo_nome_arquivo}')
                    else:
                        infoLogs().info(f'IMPOSTO - Valor total não encontrado no arquivo: {nome_arquivo}')
                except Exception as e:
                    infoLogs().error(f'IMPOSTO - Erro ao processar o arquivo {nome_arquivo}: {str(e)}')

            else:
                infoLogs().info(f'IMPOSTO - Arquivo não corresponde ao padrão: {nome_arquivo}')

    infoLogs().info(f'Etapa renomear IMPOSTO finalizada')



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

    transacoes = {}

    for caminho in pastas:
        for nome_arquivo in os.listdir(caminho):
            if nome_arquivo.lower().startswith('pix') and nome_arquivo.lower().endswith('.pdf'):
                caminho_pdf = os.path.join(caminho, nome_arquivo)
                try:
                    texto_pdf = extrair_texto_pdf(caminho_pdf)
                    valor_pagamento, nome_destinatario, id_transacao = extrair_informacoes(texto_pdf)

                    if not all([valor_pagamento, nome_destinatario, id_transacao]):
                        print(f"Dados incompletos para {nome_arquivo}. Pulando...")
                        continue
                    
                    nome_destinatario = re.sub(r'[<>:"/\\|?*\n\r]+', '_', nome_destinatario[:20]).strip()
                    valor_pagamento = valor_pagamento.replace(",", ".")
                    
                    base_nome = f"{todasDatas()[0]}_CP_{nome_destinatario}_R${valor_pagamento}"
                    
                    if base_nome not in transacoes:
                        transacoes[base_nome] = []
                    
                    if id_transacao in transacoes[base_nome]:
                        print(f"Arquivo com mesmo ID já existe: {nome_arquivo}. Pulando...")
                        continue
                    
                    transacoes[base_nome].append(id_transacao)
                    versao = len(transacoes[base_nome])
                    novo_nome_pdf = f"{base_nome}_V{versao}.pdf" if versao > 1 else f"{base_nome}.pdf"
                    caminho_novo_pdf = os.path.join(caminho, novo_nome_pdf)
                    
                    os.rename(caminho_pdf, caminho_novo_pdf)
                    print(f"Arquivo renomeado para: {novo_nome_pdf}")
                except Exception as e:
                    print(f"Erro ao processar {nome_arquivo}: {e}")
    
    infoLogs().info(f'Etapa renomear PIX finalizada')

 

# Função para remover caracteres inválidos do nome do arquivo
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\n\r]+', '_', filename)


# pastas = [R'C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - v2\TESTE_CP']


# pastas = [
    
#                 rf"C:\Users\axlda\iFinance\iFinance - Dados\IFINANCE RIBEIRÃO PRETO\01. CLIENTES\002. SALGADARIA DA ILHA LTDA ME\1. ARQUIVADOS\2025\02.2025\02. COMPROVANTES DE PAGAMENTO\24.02.2025_SICOOB_20287-8",
       
          
#             ]
# renomearPdfs(pastas)
# renomearPix(pastas)
# renomeiImposto(pastas)

# print(criar_caminho_onedrive('RECAP_PNEUS_4277'))


