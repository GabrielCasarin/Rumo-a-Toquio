##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################
import os.path
import json
import pygame
import SamurAI.config import as conf


with open(os.path.join(conf.ROOT_DIR, 'config', 'config.json') as jfile:
    config = json.load(jfile)
    cores = config['cores']
    IMG_NAMES = config['IMG_SamurAI-Images']
    IMG_NAMES_BUTTONS = config['IMG_buttons-Images']
    IMG_NAMES_INFO = config['IMG_info-Images']


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

    def draw(self, surface):
        for casa in self.casas.values():
            pygame.draw.rect(surface, casa["cor"], casa["rect"])
            pygame.draw.rect(surface, (0,0,0), casa["rect"].copy(), 1)

    def setBoard(self, tabuleiro_separado):
        for j in range(len(tabuleiro_separado)):
            tabuleiro_separado[j] = tabuleiro_separado[j].split()
            for i in range(len(tabuleiro_separado[j])):
                self.casas[i, j]['cor'] = cores[tabuleiro_separado[j][i]]


class Samurai(pygame.sprite.Sprite):
    def __init__(self, num, IMAGES, IMAGES_BUTTONS, IMAGES_INFO):
        super(Samurai, self).__init__()
    
        self.IMAGES = IMAGES
        self.IMAGES_BUTTONS = IMAGES_BUTTONS
        self.IMAGES_INFO = IMAGES_INFO

        self.num = num

        if num == 0:
            self.img_name = "Blue-spear"
            self.image = self.IMAGES[self.img_name]

        elif num == 1:
            self.img_name = "Blue-sword"
            self.image = self.IMAGES[self.img_name]

        elif num == 2:
            self.img_name = "Blue-battleaxe"
            self.image = self.IMAGES[self.img_name]

        elif num == 3:
            self.img_name = "Red-spear"
            self.image = self.IMAGES[self.img_name]

        elif num == 4:
            self.img_name = "Red-sword"
            self.image = self.IMAGES[self.img_name]

        elif num == 5:
            self.img_name = "Red-battleaxe"
            self.image = self.IMAGES[self.img_name]

        else:
            print('deu ruim')

        self.rect = self.image.get_rect(center=(-100,-100))

        self.x = -1
        self.y = -1
        self.hidden = 0
        self.treatment = 0
        self.order_status = 0

    def set_center(self, center):
        self.rect = self.image.get_rect(center=center)

    def update(self, SCREEN, board, x, y, order_status, hidden, treatment):
        self.x, self.y, self.order_status, self.hidden, self.treatment = int(x), int(y), int(order_status), int(hidden), int(treatment)

        if (self.x,self.y) != (-1, -1):
            self.set_center(board.casas[(self.x,self.y)]['rect'].center)
            self.drawBoard(SCREEN)

        self.drawStatus()

    def drawBoard(self, surface):
        if self.rect.centerx >= 0 and self.rect.centery >= 0:
            surface.blit(self.image, self.rect)

    def drawStatus(self, SCREEN):

        #Posicao de referencia
        centerStat = (520 + 140*(self.num//3), 320 + (self.num%3)*45)
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

        #statusHidden
        if self.hidden == 1:
            hImg = IMAGES_INFO['Hidden']
            hRect = hImg.get_rect(center=(centerStat[0]+11,centerStat[1]-11))
            SCREEN.blit(hImg,hRect)


class ClienteGUI:
    def __init__(self, fps=1):
        # configura a janela
        pygame.init()
        pygame.display.set_icon(pygame.image.load("./SamurAI/images/SamurAI-Images/Icon.png"))
        pygame.display.set_caption('Samurai3x3 AI Battle')
        # configura a tela
        self.screen = pygame.display.set_mode((800,600))
        self.screen.fill([220,220,220])

        IMAGES = {name: pygame.image.load(
            "./SamurAI/images/SamurAI-Images/{}.png".format(name)).convert_alpha() for name in IMG_NAMES}

        IMAGES_BUTTONS = {name: pygame.image.load(
            "./SamurAI/images/buttons-Images/{}.png".format(name)).convert_alpha() for name in IMG_NAMES_BUTTONS}

        IMAGES_INFO = {name: pygame.image.load(
            "./SamurAI/images/info-Images/{}.png".format(name)).convert_alpha() for name in IMG_NAMES_INFO}

        self.myfont = pygame.font.SysFont("arial", 15)

        # desenha
        pygame.display.update()

        self.clock = pygame.time.Clock()
        self.FPS = fps

        # cria um tabuleiro e seus samurais
        self.tab = Board(conf.SIZE)
        self.samurais = [Samurai(i, IMAGES, IMAGES_BUTTONS, IMAGES_INFO) for i in range(6)]

    def update(self, turn_info):
        separado = turn_info.split('\n')

        turno_separado = separado[0] #pegando apenas a parte do tabuleiro da string status
        samurais_separados = separado[1:7] #pegando apenas a parte do tabuleiro da string status
        tabuleiro_separado = separado[7:] #pegando apenas a parte do tabuleiro da string status

        self.tab.setBoard(tabuleiro_separado)
        self.tab.draw(self.screen)

        for i in range (6):
            dados_samurai = samurais_separados[i].split(' ')
            samurais[i].update(self.screen, self.tab, dados_samurai[0], dados_samurai[1], 
                dados_samurai[2], dados_samurai[3], dados_samurai[4])
        pygame.display.update()

    def tick(self):
        self.clock.tick(self.FPS)
