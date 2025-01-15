import pyautogui
import time as tm
from extrairTextoPrint import qntComprovante
tm.sleep(2)

#Defina as coordenadas da área que você quer capturar (x, y, largura, altura)

def tiraPrint():

    x = 800
    y = 345
    largura = 160
    altura = 62

    # Capturar a área específica
    screenshot = pyautogui.screenshot(region=(x, y, largura, altura))

    # Salvar a captura de tela
    screenshot.save('prints/captura.png')



def tirarPrintQntComprovanteImposto():  

    x = 686
    y = 300
    largura = 600
    altura = 800

    # Capturar a área específica
    screenshot = pyautogui.screenshot(region=(x, y, largura, altura))

    # Salvar a captura de tela
    screenshot.save('prints/qnt_comprovanteImposto.png')


def tirarPrintQntComprovante():  

    x = 686
    y = 400
    largura = 600
    altura = 600

    # Capturar a área específica
    screenshot = pyautogui.screenshot(region=(x, y, largura, altura))

    # Salvar a captura de tela
    screenshot.save('prints/qnt_comprovante.png')




def tirarPrintPix():
    x = 586
    y = 300
    largura = 600
    altura = 800

    # Capturar a área específica
    screenshot = pyautogui.screenshot(region=(x, y, largura, altura))

    # Salvar a captura de tela
    screenshot.save('prints/qntExtratoPix.png')



def tirarPrintErroPix():
    x = 486
    y = 200
    largura = 600
    altura = 400

    # Capturar a área específica
    screenshot = pyautogui.screenshot(region=(x, y, largura, altura))

    # Salvar a captura de tela
    screenshot.save('prints/erroPix.png')


def tirarPrintErroConvenio():
    x = 486
    y = 200
    largura = 600
    altura = 400

    # Capturar a área específica
    screenshot = pyautogui.screenshot(region=(x, y, largura, altura))

    # Salvar a captura de tela
    screenshot.save('prints/erroConvenioSemInfo.png')


def tirarPrintLogin():
    
    x = 343
    y = 123
    largura = 60
    altura = 20

    # Capturar a área específica
    screenshot = pyautogui.screenshot(region=(x, y, largura, altura))

    # Salvar a captura de tela
    screenshot.save('prints/erroLogin.png')

