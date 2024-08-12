import pygame
import sys
from face_tracker import FaceTracker

#Interpola linearmente entre dois pontos baseado em t.
def interpolate(t, ponto1, ponto2):
    return ponto1[0] + t * (ponto2[0] - ponto1[0]), ponto1[1] + t * (ponto2[1] - ponto1[1])
#Calcula um ponto numa curva de Bezier para um dado t.
def bezier(t, pontos):
    while len(pontos) > 1:
        pontos = [interpolate(t, pontos[i], pontos[i+1]) for i in range(len(pontos)-1)]
    return pontos[0]
#Desenha uma curva de Bezier na superfície dada, baseada nos pontos de controlo.
def desenha_bezier(superficie, cor, pontos_ctrl, segmentos=20):
    # Executa a funcao bezier 
    pontos = [bezier(t/segmentos, pontos_ctrl[:]) for t in range(segmentos + 1)]
    for i in range(len(pontos) - 1):
        pygame.draw.line(superficie, cor, pontos[i], pontos[i+1], 10)

pygame.init()
tracker = FaceTracker()

altura_quadro, largura_quadro = 720, 1280
quadro = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

preto = (0, 0, 0)
branco = (255, 255, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    quadro.fill(preto)

    pos_cara = tracker.track_landmark()
    if pos_cara is not None:
        pos_x_cara, pos_y_cara = pos_cara
        # (x,y)
    else:
        # se nao encontra face coloca a posicao no meio do quadro
        pos_x_cara = largura_quadro // 2
        pos_y_cara = altura_quadro // 2
    # Adiciona um ponto de controlo baseado na posição do rosto
    ponto_ctrl_meio = (pos_x_cara, pos_y_cara)
    '''3 pontos de controlo (pontos_ctrl):
        P1: centro-esquerdo do quadro,
        P2: posicao do ponto que deu o facetracker
        P3: centro-direito do quadro
    '''
    pontos_ctrl = [(0, altura_quadro // 2), ponto_ctrl_meio, (largura_quadro, altura_quadro // 2)]
    # Desenha a curva com a cor branca com 20 segmentos
    desenha_bezier(quadro, branco, pontos_ctrl)
    pygame.display.flip()
tracker.release()
pygame.quit()
sys.exit()
