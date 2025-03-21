from extrairTextoPrint import numeroPrint
import pyautogui as py
import time as tm

tempo = 2



def encontrarPosicoes():
    numPrint = numeroPrint()
    senha = [7, 8, 3, 8, 4, 0, 8, 7]

    # Convertendo a lista de senha para inteiros
    numPrint = [int(s) for s in numPrint]
    # Encontrando as posições dos valores da senha em numPrint
    posicoes = []
    for valor in senha:
        if valor in numPrint:
            posicoes.append(numPrint.index(valor))
    return posicoes


def todas_posicoes(numero):
    match numero:
        case 0:
            # py.click(x=537, y=346)
            py.click(x=813, y=351)
            print('digito 0')
            tm.sleep(tempo)
        case 1:
            py.click(x=845, y=352)
            # py.click(x=569, y=344)
            print('digito 1')
            tm.sleep(tempo)
        case 2:
            py.click(x=875, y=352)
            # py.click(x=599, y=345)
            print('digito 2')
            tm.sleep(tempo)
        case 3:
            py.click(x=905, y=352)
            # py.click(x=629, y=344)
            print('digito 3')
            tm.sleep(tempo)
        case 4:
            py.click(x=935, y=352)
            # py.click(x=661, y=345)
            print('digito 4')
            tm.sleep(tempo)
        case 5:
            py.click(x=811, y=386)
            # py.click(x=537, y=374)
            print('digito 5')
            tm.sleep(tempo)
        case 6:
            py.click(x=845, y=386)
            # py.click(x=568, y=376)
            print('digito 6')
            tm.sleep(tempo)
        case 7:
            py.click(x=875, y=386)
            # py.click(x=597, y=375)
            print('digito 7')
            tm.sleep(tempo)
        case 8:
            py.click(x=904, y=386)
            # py.click(x=630, y=375)
            print('digito 8')
            tm.sleep(tempo)
        case 9:
            py.click(x=936, y=381)
            # py.click(x=661, y=376)
            print('digito 9')
            tm.sleep(tempo)

