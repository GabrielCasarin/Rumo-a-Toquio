##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

import json
import socket
import pygame
pygame.init()

PRINT_DADOS = False

with open('config/config.json') as jfile:
    config = json.load(jfile)
    cores = config['cores']
    IMG_NAMES = config['IMG_SamurAI-Images']
    IMG_NAMES_BUTTONS = config['IMG_buttons-Images']
    IMG_NAMES_INFO = config['IMG_info-Images']
    MODO_OFFLINE = config['modo_offline']
    MAX_TURN = config['max_turn']
    SPLASH_SCREEN = config['splash_screen']

SCREEN      = pygame.display.set_mode((800,600))

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


bg = pygame.image.load("images/background.png")
bgrect = bg.get_rect()
SCREEN.blit(bg,bgrect)

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
        if self.treatment>0:
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


class ButtonSamurai(pygame.sprite.Sprite):
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

    # def draw(self,enable,update=True):
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


class Acao(pygame.sprite.Sprite):
    def __init__(self,num,update=False):

        cmx = 550   #centerMoveX
        cmy = 200   #centerMoveY

        cox = 670   #centerOcuppyX 
        coy = 140   #centerOcuppyY

        dPad = 43  #distancia do center do Pad

        if num == 0:
            self.imgName, self.center = "Send"         , (450,        500      )  
        elif num == 1:
            self.imgName, self.center = "occupy_down"  , (cox,        coy+dPad)  
        elif num == 2:
            self.imgName, self.center = "occupy_right" , (cox+dPad,  coy      )  
        elif num == 3:
            self.imgName, self.center = "occupy_up"    , (cox,        coy-dPad)  
        elif num == 4:
            self.imgName, self.center = "occupy_left"  , (cox-dPad,  coy      )  
        elif num == 5:
            self.imgName, self.center = "move_down"    , (cmx,        cmy+dPad)  
        elif num == 6:
            self.imgName, self.center = "move_right"   , (cmx+dPad,  cmy      )  
        elif num == 7:
            self.imgName, self.center = "move_up"      , (cmx,        cmy-dPad)  
        elif num == 8:
            self.imgName, self.center = "move_left"    , (cmx-dPad,  cmy      )  
        elif num == 9:
            self.imgName, self.center = "Hide"         , (670,        240      )  
        elif num == 10:
            self.imgName, self.center = "Erase"        , (400,        500      )  

        self.img = IMAGES_BUTTONS[self.imgName]
        self.rect = self.img.get_rect(center=self.center)
        SCREEN.blit(self.img,self.rect)

        #textos:
        occImg = IMAGES_BUTTONS['Occupy']
        occRect = occImg.get_rect(center=(cox,coy))
        SCREEN.blit(occImg, occRect)
        movImg = IMAGES_BUTTONS['Move']
        movRect = movImg.get_rect(center=(cmx,cmy))
        SCREEN.blit(movImg, movRect)
        
        if update:
            pygame.display.update()


class OrderList(pygame.sprite.Sprite):

    def __init__(self):

        self.order = ['0']

        self.centers = [
            ( 40,500),
            (125,500),
            (175,500),
            (225,500),
            (275,500),
            (325,500)
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
            "Hide"
        ]

        for i in range(6):
            boxImg = IMAGES_BUTTONS['Empty']
            boxRect = boxImg.get_rect(center=self.centers[i])
            SCREEN.blit(boxImg,boxRect)
        pygame.display.update()

    def __str__(self):
        s = 'Order:'
        for i in range(len(self.order)):
            s += ' {}'.format(self.order[i])
        return s

    def setSamurai(self,num):
        self.order[0] = num #str = '0', '1', ou '2'
        self.draw()

    def appendO(self,newOrder):
        self.order.append(newOrder)
        self.draw()

    def popO(self):
        if len(self.order)>1:
            self.order.pop()
            self.draw()

    def clear(self):
        self.order = self.order[:1] 
        self.draw(False)

    def draw(self,update=True):

        order = self.order
        #limpando
        for i in range(6):
            boxImg = IMAGES_BUTTONS['Empty']
            boxRect = boxImg.get_rect(center=self.centers[i])
            SCREEN.blit(boxImg,boxRect)
       
        #order1:
        xImg = IMAGES[self.imgs_sam[int(order[0])]]
        xRect = xImg.get_rect(center=self.centers[0])
        SCREEN.blit(xImg,xRect)

        for i in range(1,5):
            if i<len(order):
                xImg = IMAGES_BUTTONS[self.imgs_butt[int(order[i])]]
                xRect = xImg.get_rect(center=self.centers[i])
                SCREEN.blit(xImg,xRect)

        if len(order) == 6:
                xImg = IMAGES_BUTTONS[self.imgs_butt[int(order[5])]]
                xRect = xImg.get_rect(center=self.centers[5])
                SCREEN.blit(xImg,xRect)

        elif len(order) >6:
                xImg = IMAGES_BUTTONS["More"]
                xRect = xImg.get_rect(center=self.centers[5])
                SCREEN.blit(xImg,xRect)

        if update:
            #print(self)
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

    def minhaVez(self):
        return (False == (self.turn%2 + self.player%2 +self.partida%2)%2)

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
    def __init__(self, splash_screen):

        #fazendo a conexão com o servidor
        if not MODO_OFFLINE:
            #definindo o caminho pro servidor
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            with open('config/config.json') as jfile:
                config = json.load(jfile)
                self.sock.connect((config["ip"], config["port"]))

                #definindo se o player é o Player 1 ou o Player 2
                #Apesar de receber 0 ou 1, se converte para 1 ou 2 para ficar mais intuitivo            
                self.num = int(str(self.sock.recv(1), 'ascii'))+1
        else:
            #definindo se o player é o Player 1 ou o Player 2
            self.num = 1

        print('\nSou o player {}\n'.format(self.num))

        if splash_screen:
            pygame.time.delay(2000)

        SCREEN.fill([220,220,220])

        #definindo a surface
        self.screen = SCREEN
        
        #definindo o tabuleiro
        self.board = Board(15)

        #definindo o turno e seu display
        self.turn = Turno(self.num)

        #definindo os 6 samurais
        self.samurais = [Samurai(i) for i in range(6)]

        #definindo as acoes
        self.acoes = [Acao(i) for i in range(11)]
 
        #definindo a lista de ordens
        self.orderList = OrderList()

        #definindo o botão que escolhe o samurai
        self.buttonSamurai = ButtonSamurai()

        #atualizando o botao que escolhe o samurai com indicador se ele pode jogar
        #samurai = self.samurais[self.buttonSamurai.num]
        #self.buttonSamurai.draw(samurai)

 
    def run(self):
        self.estado = 'inicial'

        #loop principal do Player
        while (self.estado != 'terminal'
               and self.estado != 'quitou'):

            #dados recebidos do servidor
            turno = self.request_turn()

            #atualizando o turno atual
            self.turn.setTurn(int(turno[0]))

            #atualizando a lista de acoes
            self.orderList.clear()
            self.orderList.setSamurai(str(self.buttonSamurai.num))
         
            #atualizando o tabuleiro
            tabuleiro = turno[7:25]
            for j in range(len(tabuleiro)):
                tabuleiro[j] = tabuleiro[j].split()
                for i in range(len(tabuleiro[j])):
                    self.board[i, j]['cor'] = cores[tabuleiro[j][i]]
            self.board.draw(self.screen)

            #atualizando os samurais e colocando eles no tabuleiro
            for samurai in self.samurais:
                x, y, order_status, hidden, treatment = turno[samurai.num + 1].split()
                samurai.update(self.board, x, y, order_status, hidden, treatment)

            #atualizando o botao que escolhe o samurai com indicador se ele pode jogar
            samurai = self.samurais[self.buttonSamurai.num]
            self.buttonSamurai.draw(samurai)

            pygame.display.update()

            #decisão se é minha vez de jogar ou esperar
            if self.turn.minhaVez():
                print('Minha vez\n')
                #enquanto não tiver jogado, repetir o loop
                while (self.estado != 'enviar_comandos'
                       and self.estado != 'quitou'):
                    for event in pygame.event.get():
                        #cada cada clique do mouse:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            #verifica se foi clicado no escolhedor de samurai
                            if self.buttonSamurai.boxRect.collidepoint(event.pos):
                                self.buttonSamurai.num = (self.buttonSamurai.num+1)%3
                                self.orderList.setSamurai(str(self.buttonSamurai.num))

                                samurai = self.samurais[self.buttonSamurai.num]
                                self.buttonSamurai.draw(samurai)

                            #verifica se foi clicado em alguma das acoes   
                            for i in range(len(self.acoes)):
                                if self.acoes[i].rect.collidepoint(event.pos):
                                    #se foi clicado em cancel, apagar ultima ação
                                    if i == 10:
                                        self.orderList.popO()

                                    #se foi clicado em outra ação, adicionar ação
                                    else:
                                        self.orderList.appendO(str(i))
                                        #condicao para finalizar jogada
                                        if i == 0:
                                            self.estado = 'enviar_comandos'
                                            if PRINT_DADOS:
                                                print ('Comandos enviados:\n{}\n'.format(' '.join(self.orderList.order)))

                        #condicao de parada forçada
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            if not MODO_OFFLINE:
                                self.sock.close()
                            self.estado = 'quitou'

                #envia os comandos para o server se não estiver no MODO_OFFLINE
                if self.estado == 'enviar_comandos':
                    if not MODO_OFFLINE:
                        self.sock.send(bytes(' '.join(self.orderList.order), 'ascii'))

                    #condicao para esperar sua jogada
                    self.estado = 'aguardo'

            if self.turn.final():
                # verifica se é final de partida
                # caso positivo, espera o placar
                score_p1, score_p2 = str(self.sock.recv(1024), 'ascii').split()
                print('Scores:')
                print('Player 1:', score_p1)
                print('Player 2:', score_p2)
                print()
                self.sock.send(bytes('ok', 'ascii'))
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

Cliente(splash_screen=SPLASH_SCREEN).run()
