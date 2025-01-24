from pynput.keyboard import Listener, Key
import pyautogui
import pyperclip
import random
import time
import sys
import os

bomb_x = ""
bomb_y = ""
delays = [0.00, 0.00, 0.00, 0.00, 0.00]
long_words = True  #usar palavras longas
instant_typing = False  #digitar instantaneamente
pyautogui.PAUSE = 0  #Sem pausa entre as acoes do pyautogui
used_words = set()  

#le a lista de palavras do arquivo
with open('wordlist portugues.txt') as word_file:
    valid_words = word_file.read().split()  #Le e separa as palavras do arquivo

def release(key):
    global bomb_x, bomb_y, used_words
    #armazena posicao
    if key == Key.f8:
        try:
            bomb_x, bomb_y = pyautogui.position()  #pega a posicao atual do mouse
        except Exception as err:
            print(f"erro do mouse {err}")
            #roda o codigo em base de sua posicao
    if key == Key.f4:
        try:
            #simula um duplo clique
            pyautogui.click(x=bomb_x, y=bomb_y, clicks=2)
            #copia o texto
            with pyautogui.hold('ctrl'):
                pyautogui.press('c')
            #clica um pouco pra esquerda
            pyautogui.click(x=bomb_x - 100, y=bomb_y)
            time.sleep(0.1)
            #pega o texto copiado da area de transferencia e remove espacos extras
            syllable = pyperclip.paste().lower().strip()
            pyperclip.copy('')  #limpa
            found_words = [word for word in valid_words if syllable in word]
            if not found_words:
                print("nao achei")
                return
            if long_words:
                found_words.sort(key=len, reverse=True)  #ordena por palavras mais longas
            #escolhe uma palavra aleatoriamente que ainda nao foi usada
            final_word = random.choice(found_words)
            while final_word in used_words:
                if len(used_words) == len(found_words):
                    print("tudo usado ja")
                    return
                final_word = random.choice(found_words)
            used_words.add(final_word)  #adiciona a palavra ao conjunto de palavras usadas
            if instant_typing:
                pyperclip.copy(final_word)
                with pyautogui.hold('ctrl'):
                    pyautogui.press('v')  #cola a palavra copiada
            else:
                for char in final_word:
                    delay = random.choice(delays)  #escolhe um atraso aleatorio
                    pyautogui.write(char, delay)  #digita cada letra
            time.sleep(0.1)
            pyautogui.press('enter')  #pressiona Enter
        except Exception as e:
            print(f"Error: {e}")

#Escuta as teclas pressionadas
with Listener(on_release=release) as listener:
    listener.join()
