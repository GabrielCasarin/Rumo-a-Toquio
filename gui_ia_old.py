
##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

import json
import select
import pygame
pygame.init()

from config import *

PRINT_DADOS = True

with open('config/config.json') as jfile:
    config = json.load(jfile)
    cores = config['cores']
    IMG_NAMES = config['IMG_SamurAI-Images']
    IMG_NAMES_INFO = config['IMG_info-Images']

pygame.display.set_icon(pygame.image.load("images/SamurAI-Images/Icon.png"))
pygame.display.set_caption('Samurai3x3 AI Battle')

SCREEN      = pygame.display.set_mode((800,600))

IMAGES      = {
                name: pygame.image.load("images/SamurAI-Images/{}.png".format(name)).convert_alpha()
                for name in IMG_NAMES
                }

IMAGES_INFO = {
                name: pygame.image.load("images/info-Images/{}.png".format(name)).convert_alpha()
                for name in IMG_NAMES_INFO
                }


myfont = pygame.font.SysFont("arial", 15)

bg = pygame.image.load("images/background.png")
bgrect = bg.get_rect()
SCREEN.blit(bg,bgrect)

pygame.display.update()


class Samurai(pygame.sprite.Sprite):
    def __init__(self, num):

        self.num = num

        if num == 0:
            self.img_name = "Blue-spear"
            self.image = IMAGES[self.img_name]

        elif num == 1:
            self.img_name = "Blue-sword"
            self.image = IMAGES[self.img_name]

        elif num == 2:
            self.img_name = "Blue-battleaxe"
            self.image = IMAGES[self.img_name]

        elif num == 3:
            self.img_name = "Red-spear"
            self.image = IMAGES[self.img_name]

        elif num == 4:
            self.img_name = "Red-sword"
            self.image = IMAGES[self.img_name]

        elif num == 5:
            self.img_name = "Red-battleaxe"
            self.image = IMAGES[self.img_name]

        else:
            print('deu ruim')

        super(Samurai, self).__init__()
        self.rect = self.image.get_rect(center=(-100,-100))

        self.x = -1
        self.y = -1
        self.hidden = 0
        self.treatment = 0
        self.order_status = 0

    def set_center(self, center):
        self.rect = self.image.get_rect(center=center)

    def update(self, board, x, y, order_status, hidden, treatment):
        self.x, self.y, self.order_status, self.hidden, self.treatment = int(x), int(y), int(order_status), int(hidden), int(treatment)

        if (self.x,self.y) != (-1, -1):
            self.set_center(board.casas[(self.x,self.y)]['rect'].center)
            self.drawBoard(SCREEN)

        self.drawStatus()

    def drawBoard(self, surface):
        if self.rect.centerx >= 0 and self.rect.centery >= 0:
            surface.blit(self.image, self.rect)

    def drawStatus(self):

        #Posicao de referencia
        centerStat = (520+140*(self.num//3),320+(self.num%3)*45)
        #centerStat = (520,300+(self.num)*45)

        #Box
        boxImg = IMAGES_BUTTONS['Empty']
        boxRect = boxImg.get_rect(center=centerStat)
        SCREEN.blit(boxImg,boxRect)

        #Weapon
        statusRect = self.image.get_rect(center=centerStat)
        SCREEN.blit(self.image,statusRect)

        #redBar
        redBar = pygame.Rect(centerStat[0]+25,centerStat[1]+5,5*18,10)
        pygame.draw.rect(SCREEN, (255,0,0), redBar)

        #greenBar
        greenBar = pygame.Rect(centerStat[0]+25,centerStat[1]+5,5*(18-self.treatment),10)
        pygame.draw.rect(SCREEN, (0,215,0), greenBar)

        #blackBord
        pygame.draw.rect(SCREEN, (0,0,0), redBar,1)

        #text
        whiteBg = pygame.Rect(centerStat[0]+80,centerStat[1]-19,30,20)
        pygame.draw.rect(SCREEN, (255,255,255), whiteBg)

        texto = myfont.render('{:>2}'.format(str(self.treatment)), 1, (0,0,0))
        SCREEN.blit(texto, (centerStat[0]+80,centerStat[1]-19))

        #status: verde = pode jogar, azul = ja jogou, vermelho = machucado (vermelho tem preferencia em azul)
        if self.treatment > 0:
            infoImg = IMAGES_INFO['Red']
        elif self.order_status == 1:
            infoImg = IMAGES_INFO['Blue']
        else:
            infoImg = IMAGES_INFO['Green']
        infoRect = infoImg.get_rect(center=(centerStat[0]-11,centerStat[1]+11))
        SCREEN.blit(infoImg,infoRect)

        #statusHidden:

        if self.hidden == 1:
            hImg = IMAGES_INFO['Hidden']
            hRect = hImg.get_rect(center=(centerStat[0]+11,centerStat[1]-11))
            SCREEN.blit(hImg,hRect)

class Board:
    def __init__(self, n):
        super(Board, self).__init__()
        delta_x = 20
        delta_y = 20
        self.casas = {
            (i, j): {
                "rect": pygame.Rect(30*i + delta_x, 30*j + delta_y, 30, 30),
                "cor": (255,255,255),
            } for i in range(n) for j in range(n)
        }

    def __getitem__(self, key):
        return self.casas[key]

    def draw(self, surface):
        for casa in self.casas.values():
            pygame.draw.rect(surface, casa["cor"], casa["rect"])
            pygame.draw.rect(surface, (0,0,0), casa["rect"].copy(), 1)

    def draw(self,samurai,update=True):

        #box
        SCREEN.blit(IMAGES_BUTTONS[self.boxImg],self.boxRect)

        #samurai
        if self.num == 0:
            SCREEN.blit(IMAGES[self.img0],self.samRect)
        elif self.num == 1:
            SCREEN.blit(IMAGES[self.img1],self.samRect)
        elif self.num == 2:
            SCREEN.blit(IMAGES[self.img2],self.samRect)

        #info
        infoCenter = [self.center[0]-11,self.center[1]+11]

        if samurai.treatment > 0:
            infoImg = IMAGES_INFO['Red']
        elif samurai.order_status == 1:
            infoImg = IMAGES_INFO['Blue']
        else:
            infoImg = IMAGES_INFO['Green']

        infoRect = infoImg.get_rect(center=[self.center[0]-11,self.center[1]+11])
        SCREEN.blit(infoImg,infoRect)

        if samurai.hidden == 1:
            hImg = IMAGES_INFO['Hidden']
            hRect = hImg.get_rect(center=[self.center[0]+11,self.center[1]-11])
            SCREEN.blit(hImg,hRect)

        if update:
            pygame.display.update()

class Turno(pygame.sprite.Sprite):

    def __init__(self,player):

        self.turn = 0
        self.player = player #1 ou 2

        self.center = [550,40]
        self.boxImg = 'Turno'
        self.boxRect = IMAGES_INFO[self.boxImg].get_rect(center=self.center)

        self.enable = True
        self.infoCenter = [self.center[0]+31,self.center[1]+10]
        self.enableImg = 'Green'
        self.disableImg = 'Red'
        self.enabRect = IMAGES_INFO[self.enableImg].get_rect(center=self.infoCenter)

        self.partida = 0 #inicia com 0, assume o valor 1 durante a primeira partida e o valor 2 durante a segunda

        self.draw()

    def setTurn(self,turno):
        self.turn = turno
        if self.turn == 0 and not(MODO_OFFLINE):
            self.partida += 1
        elif MODO_OFFLINE:
            self.partida = 1
        self.draw()

    def final(self):
        return self.turn == MAX_TURN - 1

    def draw(self, update=False):

        SCREEN.blit(IMAGES_INFO[self.boxImg],self.boxRect)

        texto = myfont.render('{:>2}'.format(str(self.turn)), 1, (0,0,0))
        SCREEN.blit(texto, (self.center[0]+20,self.center[1]-15))

        if self.minhaVez():
            SCREEN.blit(IMAGES_INFO[self.enableImg],self.enabRect)
        else:
            SCREEN.blit(IMAGES_INFO[self.disableImg],self.enabRect)

        if update:
            pygame.display.update()


class Cliente:
    def __init__(self, num_ia):
     
        # definindo se o player é o Player 1 ou o Player 2
        self.num_ia = num_ia

        print('\nSou o player {}\n'.format(self.num_ia))
        if SPLASH_SCREEN:
            pygame.time.delay(2000)

        SCREEN.fill([220,220,220])

        #definindo a surface
        self.screen = SCREEN

        #definindo o tabuleiro
        self.board = Board(SIZE)

        #definindo o turno e seu display
        self.turn = Turno(self.num)

        #definindo os 6 samurais
        self.samurais = [Samurai(i) for i in range(6)]

    def run(self):

        self.estado = ''

        if MODO_OFFLINE:
            readable = ['', '']

        #loop principal do Player
        while (self.estado != 'terminal'
        	and self.estado != 'quitou'):
            if readable:
                #atualizando o turno atual
                self.turn.setTurn(int(turno[0]))

                #atualizando o tabuleiro
                tabuleiro = turno[7:22]
                for j in range(len(tabuleiro)):
                    tabuleiro[j] = tabuleiro[j].split()
                    for i in range(len(tabuleiro[j])):
                        self.board[i, j]['cor'] = cores[tabuleiro[j][i]]
                self.board.draw(self.screen)

                #atualizando os samurais e colocando eles no tabuleiro
                for samurai in self.samurais:
                    x, y, order_status, hidden, treatment = turno[samurai.num + 1].split()
                    samurai.update(self.board, x, y, order_status, hidden, treatment)

                if COMENTARIO:
                    coment = turno[22]
                    print(coment)

                pygame.display.update()

                if self.turn.minhaVez():
                    print('Minha vez\n')
                    self.estado = 'meu turno'
                else:
                    self.estado = 'turno adversario'


            for event in pygame.event.get():
                #cada cada clique do mouse:
                #condicao de parada forçada
                if event.type == pygame.QUIT:
                    pygame.quit()

            if (self.turn.final() and self.estado == 'jogada concluida') or (self.turn.final() and self.estado == 'turno adversario'):
                # verifica se é final de partida
                # caso positivo, espera o placar
                score_p1, score_p2 = str(self.sock.recv(1024), 'ascii').split()
                print('Scores:')
                print('Player 1:', score_p1)
                print('Player 2:', score_p2)
                print()
                self.sock.send(bytes('ok', 'ascii'))
                self.estado = ''
                if self.turn.partida == 2:
                    self.estado = 'terminal'

    def request_turn(self):
        print('Aguardando envio de informações de turno por parte do Game Manager...\n')
        if not MODO_OFFLINE:
            turno = str(self.sock.recv(1024), "ascii").split('\n')
        else:
            turno = open('info.txt').read().split('\n')

        if PRINT_DADOS:
            print('Dados recebidos:\n {}\n'.format(turno))
        else:
            print('Dados Recebidos\n')

        return turno

Cliente(1).run()
