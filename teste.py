import os
import shutil
from datetime import datetime
from datas import todasDatas
from caminhos import ONE_DRIVE_SALGADARIA, ONE_DRIVE_IMPETUS
from criaPasta import criaPasta

# Obtém o ano e mês atual
ano_atual = datetime.now().strftime('%Y')
mes_atual = datetime.now().strftime('%m.%Y')

def criar_caminho_onedrive(cliente):
    # Define as raízes base para cada cliente
    raiz_impetus = ONE_DRIVE_IMPETUS
    raiz_salgadaria = ONE_DRIVE_SALGADARIA

    if cliente == 'SALGADARIA_3258':
        nome_pasta = rf'02. COMPROVANTES DE PAGAMENTO\{todasDatas()[0]}_SICOOB_20287-8'
        caminho_base = raiz_salgadaria

    elif cliente == 'IMPETUS_LTDA_4001':
        nome_pasta = rf'SICOOB_4001_123787-0\{todasDatas()[0]}'
        caminho_base = raiz_impetus

    elif cliente == 'IMPETUS_LTDA_5004':
        nome_pasta = rf'SICOOB_5004_1077316-9\{todasDatas()[0]}'
        caminho_base = raiz_impetus
    
    elif cliente == 'IMPETUS_LTDA_4097':
        nome_pasta = rf'SICOOB_4097_25353-7\{todasDatas()[0]}'
        caminho_base = raiz_impetus

    elif cliente == 'IMPETUS_LTDA_4364':
        nome_pasta = rf'SICOOB_4364_40075-8\{todasDatas()[0]}'
        caminho_base = raiz_impetus
    
    else:
        print(f"Cliente {cliente} não reconhecido.")
        return None
    
    # Constrói o caminho completo
    caminho_completo = os.path.join(caminho_base, nome_pasta)
    
    # Cria a pasta se não existir
    if not os.path.exists(caminho_completo):
        os.makedirs(caminho_completo)
        print(f'Criando a pasta no servidor para o cliente {cliente}')
    else:
   
        print(f'A pasta no servidor já existe para o cliente {cliente}')

    return caminho_completo



from datas import todasDatas
from PyPDF2 import PdfReader
import re
import os
from criaPasta import criaPasta

import os
import re
from PyPDF2 import PdfReader

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

# Função principal para renomear PDFs
def renomearPdfs(pastas):
    # Padrões para buscar os campos específicos
    nome_pattern = r'Nome/Razão Social do Beneficiário:\s*(.*)'
    valor_pattern = r'Valor Documento:\s*([\d.,]+)'

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

                        # Extrai texto de todas as páginas e busca os campos específicos
                        for page_num in range(len(pdf_reader.pages)):
                            text = extract_text_from_page(pdf_reader, page_num)
                            if not nome_beneficiario:
                                nome_beneficiario = extract_fields(text, nome_pattern)
                            if not valor_documento:
                                valor_documento = extract_fields(text, valor_pattern)

                    # Após o `with`, o arquivo será fechado

                    if nome_beneficiario and valor_documento:
                        nome_beneficiario = sanitize_filenamev2(nome_beneficiario)[:20]
                        # Extrair o primeiro valor da lista se necessário
                        if isinstance(valor_documento, list) and len(valor_documento) > 0:
                            valor_documento = valor_documento[0]

                        # Define o novo nome do arquivo
                        novo_nome = f"{todasDatas()[0]}_CP_{nome_beneficiario}_R${valor_documento}.pdf"
                        novo_caminho = os.path.join(caminho, novo_nome)

                        # Verifica se o arquivo já existe
                        if os.path.exists(novo_caminho):
                            print(f"Arquivo já existe: {novo_nome}. Pulando...")
                            continue

                        # Tenta renomear o arquivo
                        os.rename(file_path, novo_caminho)
                        print(f"Renomeado: {filename} para {novo_nome}")
                    else:
                        print(f"Campos não encontrados em: {filename}")
                except PermissionError:
                    print(f"O arquivo está sendo usado por outro processo: {file_path}")
                except Exception as e:
                    print(f"Erro ao processar {filename}: {e}")


                    
# Função para renomear PDFs na pasta de imposto
def renomeiImposto(pastas):
    # Padrões de regex
    padrao_comprovante = r'COMPROVANTE DE (?:PAGAMENTO(?: - SIMPLES NACIONAL| DARF)?|AGENDAMENTO - SIMPLES NACIONAL|AGENDAMENTO DE CONVÊNIO)'
    padrao_valor = r'VALOR TOTAL:\s*([\d.,]+)'
    padrao_convenio = r'Convênio:\s*([^\n\r]+)'


    for caminho in pastas:
        # Percorre todos os arquivos na pasta
        for nome_arquivo in os.listdir(caminho):
            if nome_arquivo.lower().startswith('imposto') and nome_arquivo.lower().endswith('.pdf'):
                print(f'Imposto - Verificando arquivo: {nome_arquivo}')
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
                    print(f'Arquivo renomeado para: {novo_nome_arquivo}')
                else:
                    print(f'Valor total não encontrado no arquivo: {nome_arquivo}')
            else:
                print(f'Imposto - Arquivo não corresponde ao padrão: {nome_arquivo}')

# Função para renomear PDFs na pasta de pix
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
        return valor_pagamento, nome_destinatario

    for caminho in pastas:
        # Percorrer todos os arquivos na pasta
        for nome_arquivo in os.listdir(caminho):
            if nome_arquivo.lower().startswith('pix') and nome_arquivo.lower().endswith('.pdf'):
                caminho_pdf = os.path.join(caminho, nome_arquivo)
                
                try:
                    # Extrair texto do PDF
                    texto_pdf = extrair_texto_pdf(caminho_pdf)
                    
                    # Extrair informações do texto
                    valor_pagamento, nome_destinatario = extrair_informacoes(texto_pdf)
                    
                    if nome_destinatario:
                        # Limitar o nome do destinatário a 10 caracteres
                        nome_destinatario = nome_destinatario[:20]
                        
                        # Substituir caracteres inválidos no nome do destinatário
                        nome_destinatario = re.sub(r'[<>:"/\\|?*\n\r]+', '_', nome_destinatario).strip()
                        
                        # Remover vírgulas do valor e substituir por ponto
                        valor_pagamento = valor_pagamento.replace(",", ".")

                        # Novo nome do arquivo PDF
                        novo_nome_pdf = f"{todasDatas()[0]}_CP_{nome_destinatario}_R${valor_pagamento}.pdf"
                        caminho_novo_pdf = os.path.join(caminho, novo_nome_pdf)
                        
                        # Verifique se o novo nome já existe
                        if os.path.exists(caminho_novo_pdf):
                            print(f"O arquivo {novo_nome_pdf} já existe. Pulando renomeação.")
                            continue
                        
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

# Função para remover caracteres inválidos do nome do arquivo
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\n\r]+', '_', filename)











    


