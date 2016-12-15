import json
import socket
import pygame
pygame.init()

with open('config.json') as jfile:
    config = json.load(jfile)
    cores = config['cores']
    IMG_NAMES = config['IMG_NAMES']

SCREEN      = pygame.display.set_mode((800,600))
IMAGES      = {
                name: pygame.image.load("SamurAI-Images/{}.png".format(name)).convert_alpha()
                for name in IMG_NAMES
              }


class Samurai(pygame.sprite.Sprite):
    def __init__(self, img_name):
        super(Samurai, self).__init__()
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
        self.screen.fill((255,255,255))

        self.Acoes = {
            'move_down': {'rect': pygame.Rect(700,90,20,20), 'num':1 },
            'move_left': {'rect': pygame.Rect(670,60,20,20), 'num':3 },
            'move_up': {'rect': pygame.Rect(700,30,20,20), 'num':4 },
            'move_right': {'rect': pygame.Rect(730,60,20,20), 'num':2 },
            'occupy_down': {'rect': pygame.Rect(550,90,20,20), 'num':5 },
            'occupy_left': {'rect': pygame.Rect(520,60,20,20), 'num':8 },
            'occupy_up': {'rect': pygame.Rect(550,30,20,20), 'num':7 },
            'occupy_right': {'rect': pygame.Rect(580,60,20,20), 'num':6 },
            'Hide': {'rect': pygame.Rect(550,150,20,20), 'num':9 },
            'Send': {'rect': pygame.Rect(300,500,20,20), 'num': 0},
            'Erase': {'rect': pygame.Rect(250,500,20,20), 'num': -1},

        }
        pygame.draw.rect(self.screen,(20,20,20),self.Acoes['move_down']['rect'])
        pygame.draw.rect(self.screen,(20,20,20),self.Acoes['move_left']['rect'])
        pygame.draw.rect(self.screen,(20,20,20),self.Acoes['move_up']['rect'])
        pygame.draw.rect(self.screen,(20,20,20),self.Acoes['move_right']['rect'])

        pygame.draw.rect(self.screen,(20,20,20),self.Acoes['occupy_down']['rect'])
        pygame.draw.rect(self.screen,(20,20,20),self.Acoes['occupy_left']['rect'])
        pygame.draw.rect(self.screen,(20,20,20),self.Acoes['occupy_up']['rect'])
        pygame.draw.rect(self.screen,(20,20,20),self.Acoes['occupy_right']['rect'])

        pygame.draw.rect(self.screen,(20,20,20),self.Acoes['Hide']['rect'])

        pygame.draw.rect(self.screen,(20,20,20),self.Acoes['Send']['rect'])
        pygame.draw.rect(self.screen,(20,20,20),self.Acoes['Erase']['rect'])


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with open('config.json') as jfile:
            config = json.load(jfile)
            self.sock.connect((config["ip"], config["port"]))
            self.num = int(str(self.sock.recv(1), 'ascii'))
            print('sou o player', self.num)



        self.samurais = {
            1: Samurai("Blue-battleaxe"),
            2: Samurai("Blue-spear"),
            3: Samurai("Blue-sword"),
            4: Samurai("Red-battleaxe"),
            5: Samurai("Red-spear"),
            6: Samurai("Red-sword"),
        }


    def run(self):
        
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
                    samurai.set_center(self.board.casas[(x,y)]['rect'].center)
                    samurai.draw(self.screen)
                samurai.treatment = int(treatment)
                samurai.order_status = int(order_status)

            pygame.display.update()

            print(self.turno_atual%2+1,self.num)
            if self.turno_atual%2+1 == self.num:
                while self.estado != 'enviar_comandos':
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
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

    def request_turn(self):
        print('Aguardando envio de informações de turno por parte do Game Manager...')
        turno = str(self.sock.recv(1024), "ascii").split('\n')
        print('Dados recebidos')
        print(turno)
        return turno

Cliente().run()

