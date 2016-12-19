import json
import socket
import pygame
pygame.init()

MODO_OFFLINE = True

with open('config/config.json') as jfile:
    config = json.load(jfile)
    cores = config['cores']
    IMG_NAMES = config['IMG_NAMES']
    IMG_NAMES_BUTTONS = config['IMG_NAMES_BUTTONS']

SCREEN      = pygame.display.set_mode((800,600))

### COLOCAR TODOS OS DICIONARIOS DE IMAGENS JUNTO EM IMAGES

IMAGES      = {
                name: pygame.image.load("images/SamurAI-Images/{}.png".format(name)).convert_alpha()
                for name in IMG_NAMES
                }
IMAGES_BUTTONS  = {
                name: pygame.image.load("images/buttons-Images/{}.png".format(name)).convert_alpha()
                for name in IMG_NAMES_BUTTONS
              }

bg = pygame.image.load("images/background.png")
bgrect = bg.get_rect()
SCREEN.blit(bg,bgrect)
pygame.display.update()



class Samurai(pygame.sprite.Sprite):
    def __init__(self, img_name):
        super(Samurai, self).__init__()
        self.img_name = img_name
        self.image = IMAGES[img_name]
        self.rect = self.image.get_rect(center=(-100,-100))
        self.hidden = 1
        self.treatment = 0
        self.order_status = 0

    def set_center(self, center):
        self.rect = self.image.get_rect(center=center)

    def update(self):
        pass

    def draw(self, surface):
        if self.rect.centerx >= 0 and self.rect.centery >= 0:
            surface.blit(self.image, self.rect)


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

class Cliente:
    def __init__(self):
        
        self.board = Board(15)

        self.screen = SCREEN

        cmx = 550#centerMoveX
        cmy = 100#centerMoveY

        cox = 710#centerOcuppyX 
        coy = 100#centerOcuppyY

        bSize = 40


        self.Acoes = {
            'move_down':    {'rect': '', 'center': [cmx,        cmy+bSize],  'num':1, 'img':"Down"   },
            'move_right':   {'rect': '', 'center': [cmx+bSize,  cmy      ],  'num':2, 'img':"Right"  },
            'move_up':      {'rect': '', 'center': [cmx,        cmy-bSize],  'num':3, 'img':"Up"     },
            'move_left':    {'rect': '', 'center': [cmx-bSize,  cmy      ],  'num':4, 'img':"Left"   },
            'occupy_down':  {'rect': '', 'center': [cox,        coy+bSize],  'num':5, 'img':"Down"   },
            'occupy_right': {'rect': '', 'center': [cox+bSize,  coy      ],  'num':6, 'img':"Right"  },
            'occupy_up':    {'rect': '', 'center': [cox,        coy-bSize],  'num':7, 'img':"Up"     },
            'occupy_left':  {'rect': '', 'center': [cox-bSize,  coy      ],  'num':8, 'img':"Left"   },
            'hide':         {'rect': '', 'center': [630,        165      ],  'num':9, 'img':"Hide"   },
            'Send':         {'rect': '', 'center': [320,        520      ],  'num':0, 'img':"Send"   },
            'Erase':        {'rect': '', 'center': [270,        520      ],  'num':-1,'img':"Erase"  }
        }

        self.choseSamurai = {
            'spear':        {'rect': '','center': [550,   200],  'num':0, 'imgEnable':"Blue-spear",     'imgDisable':"Blue-spearused" },
            'sword':        {'rect': '','center': [550,   240],  'num':1, 'imgEnable':"Blue-sword"    ,  'imgDisable':"Blue-swordused"     },
            'b-axe':        {'rect': '','center': [550,   280],  'num':2, 'imgEnable':"Blue-battleaxe",  'imgDisable':"Blue-battleaxeused"     }
        }

        for acao, argumento in self.Acoes.items():
            buttonImg = IMAGES_BUTTONS[self.Acoes[acao]['img']]
            buttonRect = buttonImg.get_rect(center=self.Acoes[acao]['center'])
            self.Acoes[acao]['rect']=buttonRect
            self.screen.blit(buttonImg,buttonRect)

        pygame.display.update()
   

        if not MODO_OFFLINE:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            with open('config/config.json') as jfile:
                config = json.load(jfile)
                self.sock.connect((config["ip"], config["port"]))
                self.num = int(str(self.sock.recv(1), 'ascii'))
        else:
            self.num = 1

        print('sou o player', self.num)


        self.samurais = {
            1: Samurai("Blue-spear"),
            2: Samurai("Blue-sword"),
            3: Samurai("Blue-battleaxe"),
            4: Samurai("Red-spear"),
            5: Samurai("Red-sword"),
            6: Samurai("Red-battleaxe"),
        }


    def run(self):
        if not MODO_OFFLINE:
            while True:
                self.estado = 'inicial'
                turno = self.request_turn()
                self.turno_atual = int(turno[0])

                self.order = []

                tabuleiro = turno[7:]
                for i in range(len(tabuleiro)):
                    tabuleiro[i] = tabuleiro[i].split()
                    for j in range(len(tabuleiro[i])):
                        self.board.casas[(i,j)]['cor'] = cores[tabuleiro[i][j]]
                self.board.draw(self.screen)

                for num_samurai, samurai in self.samurais.items():
                    x, y, order_status, hidden, treatment = turno[num_samurai].split()
                    x, y = int(x), int(y)
                    samurai.hidden = int(hidden)
                    if (x,y) != (-1, -1):
                        samurai.set_center(self.board.casas[(y,x)]['rect'].center)
                        samurai.draw(self.screen)
                    samurai.treatment = int(treatment)
                    samurai.order_status = int(order_status)

                    for choseSam, argumento in self.choseSamurai.items():
                        if self.choseSamurai[choseSam]['imgEnable'] == samurai.img_name:
                            if samurai.treatment == 0 and samurai.order_status == 0:
                                buttonImg = IMAGES[self.choseSamurai[choseSam]['imgEnable']]
                            else:
                                buttonImg = IMAGES[self.choseSamurai[choseSam]['imgDisable']]
                            buttonRect = buttonImg.get_rect(center=self.choseSamurai[choseSam]['center'])
                            self.choseSamurai[choseSam]['rect']=buttonRect
                            self.screen.blit(buttonImg,buttonRect)


                pygame.display.update()

                print(self.turno_atual%2+1,self.num)
                if self.turno_atual%2+1 == self.num:
                    while self.estado != 'enviar_comandos':
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                for nome, botao in self.choseSamurai.items():
                                    if botao['rect'].collidepoint(event.pos):
                                        self.order.append(str(botao['num']))
                                        print(self.order)
                                for nome, botao in self.Acoes.items():
                                    if botao['rect'].collidepoint(event.pos):
                                        if botao['num'] == -1:
                                            if self.order:
                                                self.order.pop()
                                        else:
                                            self.order.append(str(botao['num']))
                                            if botao['num'] == 0:
                                                self.estado = 'enviar_comandos'
                                        print(self.order)
                            elif event.type == pygame.QUIT:
                                pygame.quit()
                                self.sock.close()

                    #envia os comandos para o server aqui
                    self.sock.sendall(bytes(' '.join(self.order), 'ascii'))
        else:  # se MODO_OFFLINE
                self.estado = 'inicial'
                turno = self.request_turn()
                self.turno_atual = int(turno[0])

                self.order = []

                tabuleiro = turno[7:]
                for i in range(len(tabuleiro)):
                    tabuleiro[i] = tabuleiro[i].split()
                    for j in range(len(tabuleiro[i])):
                        self.board.casas[(i,j)]['cor'] = cores[tabuleiro[i][j]]
                self.board.draw(self.screen)

                for num_samurai, samurai in self.samurais.items():
                    x, y, order_status, hidden, treatment = turno[num_samurai].split()
                    x, y = int(x), int(y)
                    samurai.hidden = int(hidden)
                    if (x,y) != (-1, -1):
                        samurai.set_center(self.board.casas[(y,x)]['rect'].center)
                        samurai.draw(self.screen)
                    samurai.treatment = int(treatment)
                    samurai.order_status = int(order_status)

                    for choseSam, argumento in self.choseSamurai.items():
                        if self.choseSamurai[choseSam]['imgEnable'] == samurai.img_name:
                            if samurai.treatment == 0 and samurai.order_status == 0:
                                buttonImg = IMAGES[self.choseSamurai[choseSam]['imgEnable']]
                            else:
                                buttonImg = IMAGES[self.choseSamurai[choseSam]['imgDisable']]
                            buttonRect = buttonImg.get_rect(center=self.choseSamurai[choseSam]['center'])
                            self.choseSamurai[choseSam]['rect']=buttonRect
                            self.screen.blit(buttonImg,buttonRect)

                pygame.display.update()

                print(self.turno_atual%2+1,self.num)
                if self.turno_atual%2+1 == self.num:
                    while self.estado != 'enviar_comandos':
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if not(self.order):
                                    for nome, botao in self.choseSamurai.items():
                                        if botao['rect'].collidepoint(event.pos):
                                            self.order.append(str(botao['num']))
                                            print(self.order)
                                else:
                                    for nome, botao in self.Acoes.items():
                                        if botao['rect'].collidepoint(event.pos):
                                            if botao['num'] == -1:
                                                if self.order:
                                                    self.order.pop()
                                            else:
                                                self.order.append(str(botao['num']))
                                                if botao['num'] == 0:
                                                    self.estado = 'enviar_comandos'
                                            print(self.order)
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

