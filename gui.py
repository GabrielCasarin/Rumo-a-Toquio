import json
import socket
import pygame
pygame.init()

MODO_OFFLINE = True

with open('config/config.json') as jfile:
    config = json.load(jfile)
    cores = config['cores']
    IMG_NAMES = config['IMG_SamurAI-Images']
    IMG_NAMES_BUTTONS = config['IMG_buttons-Images']
    IMG_NAMES_INFO = config['IMG_info-Images']

SCREEN      = pygame.display.set_mode((800,600))

### COLOCAR TODOS OS DICIONARIOS DE IMAGENS JUNTO EM IMAGES

IMAGES      = {
                name: pygame.image.load("images/SamurAI-Images/{}.png".format(name)).convert_alpha()
                for name in IMG_NAMES
                }

IMAGES_BUTTONS = {
                name: pygame.image.load("images/buttons-Images/{}.png".format(name)).convert_alpha()
                for name in IMG_NAMES_BUTTONS
                }

IMAGES_INFO = {
                name: pygame.image.load("images/info-Images/{}.png".format(name)).convert_alpha()
                for name in IMG_NAMES_INFO
                }

# bg = pygame.image.load("images/background.png")
# bgrect = bg.get_rect()
# SCREEN.blit(bg,bgrect)

SCREEN.fill([220,220,220])

myfont = pygame.font.SysFont("arial", 15)

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
        self.hidden = 1
        self.treatment = 0
        self.order_status = 0


    def set_center(self, center):
        self.rect = self.image.get_rect(center=center)

    def update(self):
        pass

    def drawBoard(self, surface):
        if self.rect.centerx >= 0 and self.rect.centery >= 0:
            surface.blit(self.image, self.rect)

    def drawStatus(self):

        #posicao de referencia
        centerStat = (520+140*(self.num//3),320+(self.num%3)*45)


        #Box
        boxImg = IMAGES_BUTTONS['Empty']
        boxRect = boxImg.get_rect(center=centerStat)      
        SCREEN.blit(boxImg,boxRect)
        
        #Weapon
        statusRect = self.image.get_rect(center=centerStat)
        SCREEN.blit(self.image,statusRect)

        #redBar        
        redBar = pygame.Rect(centerStat[0]+25,centerStat[1]+5,90,10)
        pygame.draw.rect(SCREEN, (255,0,0), redBar)

        #greenBar
        greenBar = pygame.Rect(centerStat[0]+25,centerStat[1]+5,(18-self.treatment)*5,10)
        pygame.draw.rect(SCREEN, (0,215,0), greenBar)

        #blackBord
        pygame.draw.rect(SCREEN, (0,0,0), redBar,1)

        #text
        whiteBg = pygame.Rect(centerStat[0]+80,centerStat[1]-19,30,20)
        pygame.draw.rect(SCREEN, (255,255,255), whiteBg)

        texto = myfont.render('{:>2}'.format(str(self.treatment)), 1, (0,0,0))
        SCREEN.blit(texto, (centerStat[0]+80,centerStat[1]-19))



class Board(pygame.sprite.Sprite):
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

    def update(self):
        pass

    def draw(self, surface):
        for casa in self.casas.values():
            pygame.draw.rect(surface, casa["cor"], casa["rect"])
            pygame.draw.rect(surface, (0,0,0), casa["rect"].copy(), 1)

class ButtonSamurai():
    def __init__(self):
   
        self.center = [550,100]
        
        self.boxRect = ''
        self.boxImg = 'Empty'
        self.boxRect = IMAGES_BUTTONS[self.boxImg].get_rect(center=self.center)

        self.num = 0
        self.img0 = "Blue-spear"
        self.img1 = "Blue-sword"
        self.img2 = 'Blue-battleaxe'
        self.samRect = IMAGES[self.img0].get_rect(center=self.center)

        self.enable = True
        self.infoCenter = [self.center[0]-12,self.center[1]+11]
        self.enableImg = 'Green'
        self.disableImg = 'Red'
        self.enabRect = IMAGES_INFO[self.enableImg].get_rect(center=self.infoCenter)

    def draw(self,enable,update=True):

        self.enable=enable

        #box
        SCREEN.blit(IMAGES_BUTTONS[self.boxImg],self.boxRect)

        #samurai
        if self.num == 0:
            SCREEN.blit(IMAGES[self.img0],self.samRect)
        elif self.num == 1:
            SCREEN.blit(IMAGES[self.img1],self.samRect)
        elif self.num == 2:
            SCREEN.blit(IMAGES[self.img2],self.samRect)

        #enable
        if self.enable:
            SCREEN.blit(IMAGES_INFO[self.enableImg],self.enabRect)
        else:
            SCREEN.blit(IMAGES_INFO[self.disableImg],self.enabRect)

        if update:
            pygame.display.update()

class OrderList():

    def __init__(self):
        self.centers = [
            (100,500),
            (150,500),
            (200,500),
            (250,500),
            (300,500)

        ]

        self.imgs_sam = [
            "Blue-spear",
            "Blue-sword",
            "Blue-battleaxe"
        ]

        self.imgs_butt = [
            "Send",
            "occupy_down",
            "occupy_right",
            "occupy_up",
            "occupy_left",
            "move_down",
            "move_right",
            "move_up",
            "move_left",
            "Hide2"
        ]

        for i in range(5):
            boxImg = IMAGES_BUTTONS['Empty']
            boxRect = boxImg.get_rect(center=self.centers[i])
            SCREEN.blit(boxImg,boxRect)
        pygame.display.update()


    def draw(self,order,update=True):

        #limpando
        for i in range(5):
            boxImg = IMAGES_BUTTONS['Empty']
            boxRect = boxImg.get_rect(center=self.centers[i])
            SCREEN.blit(boxImg,boxRect)
       
        #order1:
        xImg = IMAGES[self.imgs_sam[int(order[0])]]
        xRect = xImg.get_rect(center=self.centers[0])
        SCREEN.blit(xImg,xRect)

        for i in range(1,4):
            if i<len(order):
                xImg = IMAGES_BUTTONS[self.imgs_butt[int(order[i])]]
                xRect = xImg.get_rect(center=self.centers[i])
                SCREEN.blit(xImg,xRect)

        if len(order) == 5:
                xImg = IMAGES_BUTTONS[self.imgs_butt[int(order[4])]]
                xRect = xImg.get_rect(center=self.centers[4])
                SCREEN.blit(xImg,xRect)

        elif len(order) >5:
                xImg = IMAGES_BUTTONS["More"]
                xRect = xImg.get_rect(center=self.centers[4])
                SCREEN.blit(xImg,xRect)

        if update:
            pygame.display.update()



class Turno():

    def __init__(self):
        self.center = [550,40]
        self.boxImg = 'Turno'
        self.boxRect = IMAGES_INFO[self.boxImg].get_rect(center=self.center)

        self.enable = True
        self.infoCenter = [self.center[0]+31,self.center[1]+10]
        self.enableImg = 'Green'
        self.disableImg = 'Red'
        self.enabRect = IMAGES_INFO[self.enableImg].get_rect(center=self.infoCenter)


    def draw(self,turno,meuTurno,update=False):
        self.turn = turno
        SCREEN.blit(IMAGES_INFO[self.boxImg],self.boxRect)

        texto = myfont.render('{:>2}'.format(str(self.turn)), 1, (0,0,0))
        SCREEN.blit(texto, (self.center[0]+20,self.center[1]-15))

        if meuTurno:
            SCREEN.blit(IMAGES_INFO[self.enableImg],self.enabRect)
        else:
            SCREEN.blit(IMAGES_INFO[self.disableImg],self.enabRect)

        if update:
            pygame.display.update()


class Cliente:
    def __init__(self):
        
        self.board = Board(15)

        self.screen = SCREEN

        cmx = 550#centerMoveX
        cmy = 200#centerMoveY

        cox = 670#centerOcuppyX 
        coy = 140#centerOcuppyY

        bSize = 40

        self.Acoes = {
            'occupy_down':  {'rect': '', 'center': [cox,        coy+bSize],  'num':1, 'img':"occupy_down"   },
            'occupy_right': {'rect': '', 'center': [cox+bSize,  coy      ],  'num':2, 'img':"occupy_right"  },
            'occupy_up':    {'rect': '', 'center': [cox,        coy-bSize],  'num':3, 'img':"occupy_up"     },
            'occupy_left':  {'rect': '', 'center': [cox-bSize,  coy      ],  'num':4, 'img':"occupy_left"   },

            'move_down':    {'rect': '', 'center': [cmx,        cmy+bSize],  'num':5, 'img':"move_down"   },
            'move_right':   {'rect': '', 'center': [cmx+bSize,  cmy      ],  'num':6, 'img':"move_right"  },
            'move_up':      {'rect': '', 'center': [cmx,        cmy-bSize],  'num':7, 'img':"move_up"     },
            'move_left':    {'rect': '', 'center': [cmx-bSize,  cmy      ],  'num':8, 'img':"move_left"   },

            'hide':         {'rect': '', 'center': [670,        240      ],  'num':9, 'img':"Hide2"   },
            'Send':         {'rect': '', 'center': [450,        500      ],  'num':0, 'img':"Send"   },
            'Erase':        {'rect': '', 'center': [400,        500      ],  'num':-1,'img':"Erase"  }
        }

        for acao, argumento in self.Acoes.items():
            buttonImg = IMAGES_BUTTONS[self.Acoes[acao]['img']]
            buttonRect = buttonImg.get_rect(center=self.Acoes[acao]['center'])
            self.Acoes[acao]['rect']=buttonRect
            self.screen.blit(buttonImg,buttonRect)

        self.buttonSamurai = ButtonSamurai()

        self.turn = Turno()
        self.turn.draw(0,True) #temp

        self.samurais = [Samurai(i) for i in range(6)]
 
        self.orderList = OrderList()

        if not MODO_OFFLINE:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            with open('config/config.json') as jfile:
                config = json.load(jfile)
                self.sock.connect((config["ip"], config["port"]))
                self.num = int(str(self.sock.recv(1), 'ascii'))
        else:
            self.num = 1

        print('sou o player', self.num)

        
    def run(self):
        if not MODO_OFFLINE:
            while True:
                self.estado = 'inicial'
                turno = self.request_turn()
                self.turno_atual = int(turno[0])

                self.order = [str(self.buttonSamurai.num)]

                tabuleiro = turno[7:]
                for i in range(len(tabuleiro)):
                    tabuleiro[i] = tabuleiro[i].split()
                    for j in range(len(tabuleiro[i])):
                        self.board.casas[(i,j)]['cor'] = cores[tabuleiro[i][j]]
                self.board.draw(self.screen)

                for samurai in self.samurais:
                    x, y, order_status, hidden, treatment = turno[samurai.num+1].split()
                    x, y = int(x), int(y)
                    samurai.hidden = int(hidden)
                    if (x,y) != (-1, -1):
                        samurai.set_center(self.board.casas[(y,x)]['rect'].center)
                        samurai.drawBoard(self.screen)
                    samurai.treatment = int(treatment)
                    samurai.order_status = int(order_status)
                    samurai.drawStatus()
                samurai = self.samurais[self.buttonSamurai.num]
                enable = (samurai.order_status == 0 and samurai.treatment == 0)
                self.buttonSamurai.draw(enable)


                if self.turno_atual%2+1 == self.num:
                    while self.estado != 'enviar_comandos':
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if self.buttonSamurai.boxRect.collidepoint(event.pos):
                                    self.buttonSamurai.num = (self.buttonSamurai.num+1)%3
                                    self.order[0] = str(self.buttonSamurai.num)

                                    samurai = self.samurais[self.buttonSamurai.num]
                                    enable = (samurai.order_status == 0 and samurai.treatment == 0)
                                    self.buttonSamurai.draw(enable)

                                    print(self.order)
                                
                                for nome, botao in self.Acoes.items():
                                    if botao['rect'].collidepoint(event.pos):
                                        if botao['num'] == -1:
                                            if len(self.order)>1:
                                                self.order.pop()
                                        else:
                                            self.order.append(str(botao['num']))
                                            if botao['num'] == 0:
                                                self.estado = 'enviar_comandos'
                                        print(self.order)

                                self.orderList.draw(self.order)



                            elif event.type == pygame.QUIT:
                                pygame.quit()
                                self.sock.close()

                    #envia os comandos para o server aqui
                    self.sock.sendall(bytes(' '.join(self.order), 'ascii'))

        else:  # se MODO_OFFLINE
                self.estado = 'inicial'
                turno = self.request_turn()
                self.turno_atual = int(turno[0])

                self.order = [str(self.buttonSamurai.num)]

                tabuleiro = turno[7:]
                for i in range(len(tabuleiro)):
                    tabuleiro[i] = tabuleiro[i].split()
                    for j in range(len(tabuleiro[i])):
                        self.board.casas[(i,j)]['cor'] = cores[tabuleiro[i][j]]
                self.board.draw(self.screen)

                for samurai in self.samurais:
                    x, y, order_status, hidden, treatment = turno[samurai.num+1].split()
                    x, y = int(x), int(y)
                    samurai.hidden = int(hidden)
                    if (x,y) != (-1, -1):
                        samurai.set_center(self.board.casas[(y,x)]['rect'].center)
                        samurai.drawBoard(self.screen)
                    samurai.treatment = int(treatment)
                    samurai.order_status = int(order_status)
                    samurai.drawStatus()
                samurai = self.samurais[self.buttonSamurai.num]
                enable = (samurai.order_status == 0 and samurai.treatment == 0)
                self.buttonSamurai.draw(enable)


                if self.turno_atual%2+1 == self.num:
                    while self.estado != 'enviar_comandos':
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if self.buttonSamurai.boxRect.collidepoint(event.pos):
                                    self.buttonSamurai.num = (self.buttonSamurai.num+1)%3
                                    self.order[0] = str(self.buttonSamurai.num)

                                    samurai = self.samurais[self.buttonSamurai.num]
                                    enable = (samurai.order_status == 0 and samurai.treatment == 0)
                                    self.buttonSamurai.draw(enable)

                                    print(self.order)
                                
                                for nome, botao in self.Acoes.items():
                                    if botao['rect'].collidepoint(event.pos):
                                        if botao['num'] == -1:
                                            if len(self.order)>1:
                                                self.order.pop()
                                        else:
                                            self.order.append(str(botao['num']))
                                            if botao['num'] == 0:
                                                self.estado = 'enviar_comandos'
                                        print(self.order)

                                self.orderList.draw(self.order)



                            elif event.type == pygame.QUIT:
                                pygame.quit()
                                self.sock.close()

    def request_turn(self):
        print('Aguardando envio de informações de turno por parte do Game Manager...')
        if not MODO_OFFLINE:
            turno = str(self.sock.recv(1024), "ascii").split('\n')
        else:
            turno = open('info.txt').read().split('\n')
        print('Dados recebidos')
        print(turno)
        return turno

Cliente().run()

