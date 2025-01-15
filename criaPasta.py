from datas import todasDatas
import os
import shutil

def dadosConta_salgaderia():
    numeroDaConta = 'SALGADARIA_3258'
    data = todasDatas()[0]
    banco = 'SICOOB'
    return numeroDaConta, data, banco

def dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA1():
    numeroDaConta = 'IMPETUS_4001'
    data = todasDatas()[0]
    banco = 'SICOOB'
    return numeroDaConta, data, banco

def dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA2():
    numeroDaConta = 'IMPETUS_5004'
    data = todasDatas()[0]
    banco = 'SICOOB'
    return numeroDaConta, data, banco

def dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA3():
    numeroDaConta = 'IMPETUS_4097'
    data = todasDatas()[0]
    banco = 'SICOOB'
    return numeroDaConta, data, banco

def dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA4():
    numeroDaConta = 'IMPETUS_4364'
    data = todasDatas()[0]
    banco = 'SICOOB'
    return numeroDaConta, data, banco

def criaPasta(indice=None):
    """
    Cria pastas para as contas e permite acessar um caminho específico.
    
    :param indice: (opcional) Índice da pasta desejada, começando do 0. 
                   Se None, retorna o último caminho criado.
    :return: Caminho da pasta selecionada ou o último caminho criado.
    """
    # Caminho base para a criação das pastas
    # base_path = r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David"
    
    base_path = rf'C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - v2\Comprovantes'

    # Funções de dados das contas
    contas = [
        dadosConta_salgaderia(),
        dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA1(),
        dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA2(),
        dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA3(),
        dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA4()

    ]

    # Lista para armazenar os caminhos criados
    caminhos = []

    # Criar as 5 pastas
    for conta in contas:
        numero_da_conta, data, banco = conta
        caminho = os.path.join(base_path, f"{data}_{banco}_{numero_da_conta}")

        try:
            os.makedirs(caminho)
            print(f'Estrutura de pasta criada em: {caminho}')
        except FileExistsError:
            # print(f'já existe em: {caminho}')
            pass
        
        # Adiciona o caminho à lista
        caminhos.append(caminho)
    
    # Retorna um caminho específico ou o último caminho criado
    if indice is not None and 0 <= indice < len(caminhos):
        return caminhos[indice]
    return caminhos[-1]



def exclui_pastas_criadas_todos():
    # Caminho base das pastas
    base_path = r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB - v2\Comprovantes"

    # Funções de dados das contas
    contas = [
        dadosConta_salgaderia(),
        dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA1(),
        dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA1(),
        dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA2(),
        dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA3(),
        dadosConta_IMPETUS_ENERGY_E_BUSINESS_LTDA4()

    ]

    # Excluir as 5 pastas
    for conta in contas:
        numero_da_conta, data, banco = conta
        caminho = os.path.join(base_path, f"{data}_{banco}_{numero_da_conta}")

        # Verificar se a pasta existe antes de tentar excluí-la
        if os.path.exists(caminho):
            shutil.rmtree(caminho)
            print(f'{caminho} foi excluído.')
        else:
            print(f'A pasta {caminho} não existe.')




def excluir_arquivos_pdf(pastas):

    try:
        # Padrões para os nomes dos arquivos a serem excluídos
        prefixes = ("pix", "imposto", "titulos")

        for caminho in pastas:
            for filename in os.listdir(caminho):
                # Verifica se o arquivo é um PDF e começa com um dos prefixos
                if filename.lower().startswith(prefixes) and filename.endswith('.pdf'):
                    file_path = os.path.join(caminho, filename)
                    try:
                        os.remove(file_path)
                        print(f"Arquivo excluído: {file_path}")
                    except Exception as e:
                        print(f"Erro ao excluir {file_path}: {e}")
    except Exception as e:
        print('Nao existem arquivos pix, imposto ou titulos nas pastas.')
        

