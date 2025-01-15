

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
    valor_pattern = r'Valor Documento:\s*([\d.,]+)'
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
                    
# Função para renomear PDFs na pasta de imposto
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
                    
                    # Renomeia o arquivo
                    os.rename(caminho_arquivo, novo_caminho_arquivo)
                    infoLogs().info(f'IMPOSTO - Arquivo renomeado para: {novo_nome_arquivo}')
                else:
                    infoLogs().info(f'IMPOSTO - Valor total não encontrado no arquivo: {nome_arquivo}')
            else:
                infoLogs().info(f'IMPOSTO - Arquivo não corresponde ao padrão: {nome_arquivo}')

    infoLogs().info(f'Etapa renomear IMPOSTO finalizada')   

def renomearPix(pastas):
    # Função para extrair texto do PDF
    def extrair_texto_pdf(caminho_pdf):
        with open(caminho_pdf, 'rb') as arquivo_pdf:
            leitor_pdf = PdfReader(arquivo_pdf)
            texto_total = ''
            for pagina in leitor_pdf.pages:
                texto_total += pagina.extract_text()
        return texto_total

    # Função para extrair informações do texto
    def extrair_informacoes(texto):
        valor_pagamento = re.search(r'Valor do Pagamento: (\d+,\d+)', texto).group(1)
        nomes = re.findall(r'Nome: \s*(.*)', texto)
        nome_destinatario = nomes[1] if len(nomes) > 1 else None
        id_transacao = re.search(r'ID Transação: (.*?)\s+OUVIDORIA SICOOB', texto).group(1)
        return valor_pagamento, nome_destinatario, id_transacao

    # Função para verificar se o ID de transação é o mesmo entre dois arquivos
    def verificar_id_transacao(caminho_existente, id_transacao_novo):
        texto_existente = extrair_texto_pdf(caminho_existente)
        _, _, id_transacao_existente = extrair_informacoes(texto_existente)
        return id_transacao_existente == id_transacao_novo

    # Dicionário para armazenar transações anteriores
    transacoes = {}

    for caminho in pastas:
        for nome_arquivo in os.listdir(caminho):
            if nome_arquivo.lower().startswith('pix') and nome_arquivo.lower().endswith('.pdf'):
                caminho_pdf = os.path.join(caminho, nome_arquivo)
                
                try:
                    # Extrair texto do PDF
                    texto_pdf = extrair_texto_pdf(caminho_pdf)
                    
                    # Extrair informações do texto
                    valor_pagamento, nome_destinatario, id_transacao = extrair_informacoes(texto_pdf)
                    
                    if nome_destinatario:
                        # Limitar o nome do destinatário a 20 caracteres
                        nome_destinatario = nome_destinatario[:20]
                        
                        # Substituir caracteres inválidos no nome do destinatário
                        nome_destinatario = re.sub(r'[<>:"/\\|?*\n\r]+', '_', nome_destinatario).strip()
                        
                        # Remover vírgulas do valor e substituir por ponto
                        valor_pagamento = valor_pagamento.replace(",", ".")
                        
                        # Determinar o nome do arquivo
                        novo_nome_pdf = f"{todasDatas()[0]}_CP_{nome_destinatario}_R${valor_pagamento}.pdf"
                        caminho_novo_pdf = os.path.join(caminho, novo_nome_pdf)
                        
                        if os.path.exists(caminho_novo_pdf):
                            # Se o arquivo já existe, verificar ID de transação
                            if verificar_id_transacao(caminho_novo_pdf, id_transacao):
                                print(f"O arquivo {novo_nome_pdf} já existe com o mesmo ID de transação. Pulando renomeação.")
                                continue
                            else:
                                # IDs diferentes, adicionar sufixo "_V2"
                                novo_nome_pdf = f"{todasDatas()[0]}_CP_{nome_destinatario}_R${valor_pagamento}_V2.pdf"
                                caminho_novo_pdf = os.path.join(caminho, novo_nome_pdf)
                        
                        # Renomear o arquivo
                        os.rename(caminho_pdf, caminho_novo_pdf)
                        print(f"Arquivo renomeado para: {novo_nome_pdf}")
                        
                    else:
                        print(f"Nome do destinatário não encontrado no arquivo: {nome_arquivo}")
                
                except FileNotFoundError:
                    print(f"Arquivo {caminho_pdf} não encontrado.")
                
                except PermissionError as e:
                    print(f"Erro ao renomear o arquivo: {nome_arquivo}. O arquivo está em uso. {e}")
                
                except Exception as e:
                    print(f"Erro desconhecido ao renomear o arquivo: {nome_arquivo}. {e}")



    infoLogs().info(f'Etapa renomear PIX finalizada')    

# Função para remover caracteres inválidos do nome do arquivo
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\n\r]+', '_', filename)


# pastas = [R'C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - v2\TESTE_CP']

# renomearPdfs(pastas)
# renomearPix(pastas)
# renomeiImposto(pastas)


