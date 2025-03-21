import pyautogui as py
import time as tm

tm.sleep(2)
pagina_atual = 2

if pagina_atual > 1:
    valor = pagina_atual
    print('valor pagina atual valor', valor)
    while valor > 1:
        
        py.click(975,879) #-> prox pagina 990,886
        print('valor pagina atual valor aqui', valor)
        valor = valor - 1