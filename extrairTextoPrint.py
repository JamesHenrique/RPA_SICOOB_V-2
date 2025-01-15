import cv2
import pytesseract
from caminhos import  CAMINHO_EXTRATO_TITULOS,CAMINHO_EXTRATO_PIX,CAMINHO_EXTRATO_IMPOSTO
import re
from pandas_script import atualizar_total_cp









def qntComprovante(cliente):
    # Carregar a imagem'
    imagem = cv2.imread(CAMINHO_EXTRATO_TITULOS)

    #configuração Tesseract
    caminho = r"C:\Users\axlda\AppData\Local\Programs\Tesseract-OCR"
    pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

    # Converter para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro de desfoque
    imagem_desfocada = cv2.GaussianBlur(imagem_cinza, (1, 1), 0) #antes era 1,1 - 3 - 3

    # Aplicar OCR na imagem
    texto = pytesseract.image_to_string(imagem_desfocada)


   

    # # Usando expressão regular para encontrar o número após "Total de registros: "
    # # Usando expressão regular para encontrar o número após "Total de registros: "
    match = re.search(r": (\d+),", texto)

 
    info = ''
    
    if 'Emro intemo. Por favor, contate o suport' in texto:
        info = "Erro do programa. Informações não encontradas. Feche o programa  e tente novamente"
    

    elif match:
        infos = int(match.group(1))
        print(infos)
        atualizar_total_cp(cliente,infos)
    
    else:
        infos = "Nenhum valor encontrado"
        # info = 0
        atualizar_total_cp(cliente,infos)

   




def qntComprovanteImposto(cliente):
    
    info = ''
    try:
        # Carregar a imagem'
        imagem = cv2.imread(CAMINHO_EXTRATO_IMPOSTO)

        #configuração Tesseract
        caminho = r"C:\Users\axlda\AppData\Local\Programs\Tesseract-OCR"
        pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

        # Converter para escala de cinza
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        # Aplicar filtro de desfoque
        imagem_desfocada = cv2.GaussianBlur(imagem_cinza, (1,1), 0) #antes erar 1,1

        # Aplicar OCR na imagem
        texto = pytesseract.image_to_string(imagem_desfocada)


    
        # Usando expressão regular para encontrar o número após "Total de registros: "
        match = re.search(r": (\d+),", texto)
        info = ''
        
        # Usando expressão regular para encontrar o número após "Total de registros: "
        match = re.search(r": (\d+),", texto)
        info = ''
        
        if 'Emro intemo. Por favor, contate o suport' in texto:
            info = "Erro do programa. Informações não encontradas. Feche o programa  e tente novamente"
        

        elif match:
            infos = int(match.group(1))
            info = infos
            print(infos)
            atualizar_total_cp(cliente,info)
        
        else:
            print("Nenhum valor encontrado - imposto - 1")
            info = 0

            atualizar_total_cp(cliente,info)
    except:
        print("Nenhum valor encontrado - imposto - 2")
        info = 0
        atualizar_total_cp(cliente,info)
        pass
        





def qntComprovantePix(cliente):
    # Carregar a imagem'
    imagem = cv2.imread(CAMINHO_EXTRATO_PIX)

    #configuração Tesseract
    caminho = r"C:\Users\axlda\AppData\Local\Programs\Tesseract-OCR"
    pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

    # Converter para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro de desfoque
    imagem_desfocada = cv2.GaussianBlur(imagem_cinza, (1, 1), 0)#antes erar 1,1

    # Aplicar OCR na imagem
    texto = pytesseract.image_to_string(imagem_desfocada)


   
    # Usando expressão regular para encontrar o número após "Total de registros: "
    match = re.search(r": (\d+),", texto)
    numero = ''
    
    try:
        if match:
            numeros = match.group(1)
            numero = int(numeros)

            atualizar_total_cp(cliente,numero)
            print(numero)

        else:
            # numero = "Não existe comprovantes pix"
            atualizar_total_cp(cliente,0)
    except:
        numero = "Valor vazio"
        atualizar_total_cp(cliente,0)
        pass          





def erroTextoPix():
    # Carregar a imagem'
    imagem = cv2.imread(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB\prints\erroPix.png")

    #configuração Tesseract
    caminho = r"C:\Users\axlda\AppData\Local\Programs\Tesseract-OCR"
    pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

    # Converter para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro de desfoque
    imagem_desfocada = cv2.GaussianBlur(imagem_cinza, (1, 1), 0)

    # Aplicar OCR na imagem
    texto = pytesseract.image_to_string(imagem_desfocada)
    
    if 'No existe movimento PIX para o periodo informado' in texto:
        texto = "Não existe pix para o periodo informado"
    
    return texto


    
def erroTextoConvenio():
    # Carregar a imagem'
    imagem = cv2.imread(r"C:\Users\axlda\OneDrive\1. Area de Trabalho_Note Dell_Alexandre David\BANCOS_OP\RPA_SICOOB\prints\erroConvenioSemInfo.png")

    #configuração Tesseract
    caminho = r"C:\Users\axlda\AppData\Local\Programs\Tesseract-OCR"
    pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

    # Converter para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro de desfoque
    imagem_desfocada = cv2.GaussianBlur(imagem_cinza, (1, 1), 0)

    # Aplicar OCR na imagem
    texto = pytesseract.image_to_string(imagem_desfocada)
    
    if ' Nenhum agendamento foi recuperad' in texto:
        texto = "Não existe nenhum agendamento"
    
    return texto       




# # Exibir a imagem processada
# cv2.imshow('Imagem Processada', imagem_cinza)
# cv2.waitKey(0)
# cv2.destroyAllWindows()






