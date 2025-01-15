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

def caminhoPastaAreaDeTrabalho(cliente):
    # Define o caminho da pasta de trabalho para cada cliente

    if cliente == 'SALGADARIA_3258':
        pasta_trabalho = criaPasta(0)

    elif cliente == 'IMPETUS_LTDA_4001':
        pasta_trabalho = criaPasta(1)

    elif cliente == 'IMPETUS_LTDA_5004':
        pasta_trabalho = criaPasta(2)
    
    elif cliente == 'IMPETUS_LTDA_4097':
        pasta_trabalho = criaPasta(3)

    elif cliente == 'IMPETUS_LTDA_4364':
        pasta_trabalho = criaPasta(4)
                    
    


    if os.path.exists(pasta_trabalho):
        return pasta_trabalho
    else:
        print(f"A pasta de trabalho {pasta_trabalho} não existe.")
        return None

def moveArquivoOneDrive(cliente):
    # Caminho da pasta destino
    destino = criar_caminho_onedrive(cliente)
    
    # Verificação da pasta destino
    if not destino:
        print(f"Erro ao criar ou acessar o caminho de destino para o cliente {cliente}.")
        return
    
    # Caminho da pasta de origem
    origem = caminhoPastaAreaDeTrabalho(cliente)
    if not origem:
        print(f"O caminho de origem {origem} não existe.")
        return

    arquivos_existentes = []
    for arquivo in os.listdir(origem):
        if arquivo.endswith('.pdf'):
            caminho_origem = os.path.join(origem, arquivo)
            caminho_destino = os.path.join(destino, arquivo)

            # Verificar se o caminho de destino é muito longo
            if len(caminho_destino) > 260:
                print(f"O caminho de destino {caminho_destino} é muito longo.")
                continue

            # Verificar se o arquivo de origem existe antes de mover
            if not os.path.exists(caminho_origem):
                print(f"O arquivo de origem {caminho_origem} não foi encontrado.")
                continue  # Passa para o próximo arquivo

            # Imprimir os caminhos para depuração
            print(f"Movendo de {caminho_origem} para {caminho_destino}")
            
            # Verificar se o arquivo já existe no destino
            if os.path.exists(caminho_destino):
                arquivos_existentes.append(arquivo)
            else:
                try:
                    shutil.move(caminho_origem, caminho_destino)
                    print(f"Arquivo movido com sucesso de {caminho_origem} para {caminho_destino}")
                except Exception as e:
                    print(f"Erro ao mover {caminho_origem} para {caminho_destino}: {e}")

    # Listar arquivos que já existem no destino
    if arquivos_existentes:
        print("Os seguintes arquivos já existem no destino:")
        for arquivo in arquivos_existentes:
            print(arquivo)
    else:
        print("Todos os arquivos foram movidos com sucesso.")

# Testa a função para diferentes clientes
# moveArquivoOneDrive('IMPETUS_LTDA_4001')
# moveArquivoOneDrive('IMPETUS_LTDA_5004')
# moveArquivoOneDrive('SALGADARIA_3258')
# moveArquivoOneDrive('IMPETUS_LTDA_4097')
# moveArquivoOneDrive('IMPETUS_LTDA_4364')


# print(criar_caminho_onedrive('IMPETUS_LTDA_4001'))
# print(criar_caminho_onedrive('IMPETUS_LTDA_5004'))
# print(criar_caminho_onedrive('SALGADARIA_3258'))
# print(criar_caminho_onedrive('IMPETUS_LTDA_4097'))
# print(criar_caminho_onedrive('IMPETUS_LTDA_4364'))

