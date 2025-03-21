from renomeiPDF import renomearPdfs, renomearPix, renomeiImposto
from criaPasta import criaPasta, exclui_pastas_criadas_todos,excluir_arquivos_pdf
from moverPasta import moveArquivoOneDrive,criar_caminho_onedrive
from config_tela import iniciar_tela
from moverPasta import criar_caminho_onedrive
from logger import infoLogs
import pyautogui as py
import time as tm       
import messagebox as mg

def main():
    try:
        # # Exclui pastas criadas previamente na área de trabalho
        # exclui_pastas_criadas_todos()

        # Inicia a configuração da tela e verifica se deve seguir com a automação
        if 'seguir' in iniciar_tela():
            tm.sleep(1)

           
            #tenta renomear novamente os cps
            pastas = [
                
                criar_caminho_onedrive('IMPETUS_LTDA_4001'),
                criar_caminho_onedrive('IMPETUS_LTDA_5004'),
                criar_caminho_onedrive('SALGADARIA_3258'),
                criar_caminho_onedrive('IMPETUS_LTDA_4097'),
                criar_caminho_onedrive('IMPETUS_LTDA_4364'),
                criar_caminho_onedrive('RECAP_PNEUS_4277'),
                criar_caminho_onedrive('RECAP_PNEUS_3214')
            ]


            # # Renomear arquivos em cada pasta 
            renomearPdfs(pastas)
            renomeiImposto(pastas)
            renomearPix(pastas)


            # Fecha a tela utilizando o pyautogui
            fechar_tela()


            
            # #exclui os cps com nome pix, titulos e imposto se existir
            excluir_arquivos_pdf(pastas)

            # Mostra mensagem de conclusão
            mg.showinfo("Automação concluída", "Automação finalizada com sucesso")
        else:
            infoLogs().info("Tela fechada com sucesso ")
    except Exception as e:
        infoLogs().info(f"Erro durante a automação: {e}")
        mg.showerror("Erro na Automação", f"Ocorreu um erro durante a automação: {e}")

def move_arquivos_para_onedrive(*clientes):
    """Move arquivos para a pasta OneDrive para cada cliente fornecido."""
    for cliente in clientes:
        moveArquivoOneDrive(cliente)

def fechar_tela():
    """Fecha a tela utilizando o pyautogui e espera alguns segundos."""
    tm.sleep(3)
    py.click(x=1893, y=13)
    tm.sleep(3)

if __name__ == '__main__':
    main()