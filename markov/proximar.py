import pygame
import random
import time
import os
import sys
from datetime import datetime

def ler_texto(caminho_do_arquivo):
    with open(caminho_do_arquivo, 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

def construir_cadeia_de_markov(texto, tamanho_do_prefixo=2):
    markov_chain = {}
    palavras = texto.split()

    for i in range(len(palavras) - tamanho_do_prefixo):
        prefixo = tuple(palavras[i:i + tamanho_do_prefixo])
        sufixo = palavras[i + tamanho_do_prefixo]
        if prefixo not in markov_chain:
            markov_chain[prefixo] = []
        markov_chain[prefixo].append(sufixo)
    
    return markov_chain

def gerar_texto(markov_chain, tamanho=50, lista_substantivos=None, lista_conectores=None):
    tamanho_do_prefixo = 2
    prefixo = random.choice(list(markov_chain.keys()))
    resultado = list(prefixo)

    for _ in range(tamanho - len(prefixo)):
        sufixos = markov_chain.get(prefixo, None)
        if not sufixos:
            break
        proxima_palavra = random.choice(sufixos)
        resultado.append(proxima_palavra)
        prefixo = tuple(resultado[tamanho_do_prefixo:])
    
    texto_gerado = ' '.join(resultado)

    # Verificar se a última palavra gerada é um conector
    palavras_geradas = texto_gerado.split()
    if lista_conectores and lista_substantivos and palavras_geradas and palavras_geradas[-1] in lista_conectores:
        # Adicionar um substantivo aleatório ao final do texto
        substantivo_aleatorio = random.choice(lista_substantivos)
        texto_gerado += " " + substantivo_aleatorio

    return texto_gerado.capitalize()  # Capitalizar a primeira letra do texto gerado

# Inicializar Pygame
pygame.init()

# Configurações da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Proximar")

# Fonte para o texto
font = pygame.font.SysFont("courier new", 25)

# Ler o texto do trabalho teórico e construir a cadeia de Markov
texto_original = ler_texto("proximacao_texto.txt")
cadeia_markov = construir_cadeia_de_markov(texto_original)

# Ler a lista de substantivos e conectores
lista_substantivos = ler_texto("substantivos.txt").splitlines()
lista_conectores = ler_texto("conectores.txt").splitlines()

# Loop principal do programa
running = True

# Abrir o arquivo de texto para escrita no início do programa
arquivo_frases_geradas = open("frases_criadas.txt", "w", encoding="utf-8")

data_atual = datetime.now().strftime("%d/%m/%Y")
arquivo_frases_geradas.write("Data: "+ data_atual+ "\n\n")

# Loop principal do programa
while True:  # Loop infinito
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False  # Encerrar o loop quando clica esc

    # Gerar novo texto usando a cadeia de Markov
    tamanho_texto = 1
    texto_gerado = gerar_texto(cadeia_markov, tamanho=tamanho_texto, lista_substantivos=lista_substantivos, lista_conectores=lista_conectores)
    termina = random.choice(["...", ":", ".", ""])

    # Adicionar uma nova palavra aleatória ao final do texto
    nova_palavra_aleatoria = random.choice(lista_substantivos)
    texto_gerado += " " + nova_palavra_aleatoria

    # Escrever a frase gerada no arquivo de texto
    arquivo_frases_geradas.write(texto_gerado + termina + "\n")
    
    # Renderizar o texto gerado
    screen.fill((0, 0, 0))  # Limpar janela
    text_surface = font.render(texto_gerado + termina, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(4)

    if not running:
        break  


arquivo_frases_geradas.close()


pygame.quit()
sys.exit()
