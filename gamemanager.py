##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

import json
from server import Server
from util import distancia


with open('config/config.json') as jfile:
    config = json.load(jfile)
    MAX_TURN = config['max_turn']


class Game:
    #criar tabuleiro:
    def __init__(self):

        #definindo o Turno
        self.turn = 0

        #definindo o Tabuleiro
        size = 15
        self.size = size
        row = size*[8]
        tabuleiro = []
        for i in range(size):
            tabuleiro.append(row[:])
        self.tab = tabuleiro

        #definindo os Jogadores

        self.p1 = Jogador(1)
        self.p2 = Jogador(2)


        #Definindo e preenchenco as Homes Positions
        homes = []#player, pos
        for i in range(len(self.p1.samurais)):
            self.tab[self.p1.samurais[i].pos[1]][self.p1.samurais[i].pos[0]] = i
            homes.append(self.p1.samurais[i].pos[:])
        for i in range(len(self.p2.samurais)):
            self.tab[self.p2.samurais[i].pos[1]][self.p2.samurais[i].pos[0]] = i + 3
            homes.append(self.p2.samurais[i].pos[:])
        self.homes = homes

    def update(self):
        pass

    def view(self, player):

        '''Fornece todas as informações do jogo de um determinado turno para o player
        
        player = 1: Jogador 1
        player = 2: Jogador 2

        exemplo:
        T                       (Turno)
        X Y O H T               (Samurai)
        X Y O H T
        X Y O H T
        X Y O H T
        X Y O H T
        X Y O H T
        A A A A A A A A...      (Tabuleiro)
        A A A A A A A A...
        A A A A A A A A...
        A A A A A A A A...
        A A A A A A A A...
        A A A A A A A A...
        . . . . . . . . (15x15)

        '''      

        #string do turno
        sT = str(self.turn)

        #string dos samurais
        sS = ''
        if player == 1:
            for samurai1 in self.p1.samurais:
                sS += '\n'
                sS += str(samurai1.pos[0]) + ' '#x
                sS += str(samurai1.pos[1]) + ' '#y
                sS += str(samurai1.orderStat) + ' '#orderstatus
                sS += str(samurai1.hideStat) + ' '#showingstatus
                sS += str(samurai1.treat)#treatmentturns
            for samurai2 in self.p2.samurais:
                
                vendo = False
                for samurai1 in self.p1.samurais:
                    if distancia(samurai1.pos[0],samurai2.pos[0],samurai1.pos[1],samurai2.pos[1])<=5 and samurai2.hideStat == 0:
                        vendo = True
                if vendo:
                    sS += '\n'
                    sS += str(samurai2.pos[0]) + ' '#x
                    sS += str(samurai2.pos[1]) + ' '#y
                    sS += str(samurai2.orderStat) + ' '#orderstatus
                    sS += str(samurai2.hideStat) + ' '#showingstatus
                    sS += str(samurai2.treat)#treatmentturns
                else:
                    sS += '\n'
                    sS += "-1 "
                    sS += "-1 "
                    sS += str(samurai2.orderStat) + ' '#orderstatus
                    sS += "1 "
                    sS += str(samurai2.treat)#treatmentturns

        elif player == 2:
            for samurai2 in self.p2.samurais:
                sS += '\n'
                sS += str(samurai2.pos[0]) + ' '#x
                sS += str(samurai2.pos[1]) + ' '#y
                sS += str(samurai2.orderStat) + ' '#orderstatus
                sS += str(samurai2.hideStat) + ' '#showingstatus
                sS += str(samurai2.treat) #treatmentturns             
            for samurai1 in self.p1.samurais:
                vendo = False
                for samurai2 in self.p2.samurais:
                    if distancia(samurai1.pos[0],samurai2.pos[0],samurai1.pos[1],samurai2.pos[1])<=5 and samurai1.hideStat == 0:
                        vendo = True
                if vendo:
                    sS += '\n'
                    sS += str(samurai1.pos[0]) + ' '#x
                    sS += str(samurai1.pos[1]) + ' '#y
                    sS += str(samurai1.orderStat) + ' '#orderstatus
                    sS += str(samurai1.hideStat) + ' '#showingstatus
                    sS += str(samurai1.treat)#treatmentturns
                else:
                    sS += '\n'
                    sS += "-1 "
                    sS += "-1 "
                    sS += str(samurai1.orderStat) + ' '#orderstatus
                    sS += "1 "
                    sS += str(samurai1.treat)#treatmentturns

        size = self.size
        row = size*[9]
        newTab = []
        for i in range(size):
            newTab.append(row[:])

        if player == 1:
            for y1 in range (size):
                for x1 in range (size):
                    for i in range(len(self.p1.samurais)):
                        x2 = self.p1.samurais[i].pos[0]
                        y2 = self.p1.samurais[i].pos[1]
                        if distancia(x1,x2,y1,y2) <= 5:
                            newTab[y1][x1] = self.tab[y1][x1]

        if player == 2:
            for y1 in range (size):
                for x1 in range (size):
                    for i in range(len(self.p2.samurais)):
                        x2 = self.p2.samurais[i].pos[0]
                        y2 = self.p2.samurais[i].pos[1]
                        if distancia(x1,x2,y1,y2) <= 5:

                            #Invertendo os samurais para o player2 (0>3,1>4,2>5,3>0,4>1,5>2)
                            if self.tab[y1][x1] < 3: #0>3,1>4,2>5
                                newTab[y1][x1] = self.tab[y1][x1]+3
                            elif self.tab[y1][x1] < 6: #3>0,4>1,5>2
                                newTab[y1][x1] = self.tab[y1][x1]-3
                            else:
                                newTab[y1][x1] = self.tab[y1][x1]
        
        #string do tabuleiro(Mapa)                    
        sM =''
        for y in range(len(newTab)):
            sM += '\n'
            for x in range(len(newTab)-1):
                sM += str(newTab[y][x]) + ' '
            sM += str(newTab[y][size-1])

        s = sT + sS + sM
        
        return s

    def clearOrderStat(self):
        for samurai in self.p1.samurais + self.p2.samurais:
            samurai.orderStat = 0

    def heal(self):
        for samurai in self.p1.samurais + self.p2.samurais:
            if samurai.treat > 0:
                samurai.treat -= 1

    def score(self, player):
        count = 0
        if player == 1:
            for linha in self.tab:
                for casa in linha:
                    if casa in [0, 1, 2]:
                        count += 1
        elif player == 2:
            for linha in self.tab:
                for casa in linha:
                    if casa in [3, 4, 5]:
                        count += 1
        return count
                       

class Jogador:
    def __init__(self, player):
        
        # samurais = []
        # if player == 1:
        #     # samurais.append(Samurai(0,0,0))
        #     # samurais.append(Samurai(1,0,7))
        #     # samurais.append(Samurai(2,7,0))
        # elif player == 2:
        #     # samurais.append(Samurai(0,14,14))
        #     # samurais.append(Samurai(1,14,7))
        #     # samurais.append(Samurai(2,7,14))

        
        if player == 1:
            self.samurais = [Samurai(i) for i in range(0,3)]
        elif player == 2:
            self.samurais = [Samurai(i) for i in range(3,6)]  

    def order(self, comando, game):
        budget = 7
        cont = True

        comando = comando.split(' ')

        ID = int(comando.pop(0))
        if ID in [0,1,2]:
            samurai = self.samurais[ID]
        else: 
            print('Id do samurai invalido, perdeu a vez')
            return False

        if samurai.treat > 0: #se esta machucado nao joga
            print('Samurai machucado não joga')
            cont = False
        if samurai.orderStat == 1: #se ja jogou, nao joga
            print('Samurai já jogou nesse período')
            cont = False
        else:
            samurai.orderStat = 1

        while comando and cont:
            acao = int(comando.pop(0))
            if acao in [i for i in range(10)]:
                cont, custo = samurai.action(game,acao,budget)
                budget -= custo
            else: 
                cont = False
                print('Order invalida')


class Samurai:
    #def __init__(self,weaponID,x,y):
    def __init__(self,num):

        #Home position
        if num == 0:
            self.home = [ 0, 0]
        elif num == 1:
            self.home = [ 0, 7]
        elif num == 2:
            self.home = [ 7, 0]
        elif num == 3:
            self.home = [14,14]
        elif num == 4:
            self.home = [14, 7]
        elif num == 5:
            self.home = [ 7,14]

        #Weapon
        self.id = num%3
        
        #Player
        self.player = num//3 + 1

        #Posicao
        self.pos = self.home[:]

        self.orderStat = 0
        self.hideStat = 0
        self.treat = 0

        #definindo o padrao de ataque para baixo
        if self.id == 0:
            self.atkMask = [[0,1],[0,2],[0,3],[0,4]]
        elif self.id == 1:
            self.atkMask = [[0,2],[0,1],[1,1],[1,0],[2,0]]
        elif self.id == 2:
            self.atkMask = [[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]

    def __str__(self):

        s = '\nSamurai:'
        if self.id%3 == 0:
            s += '  - Spear' 
        if self.id%3 == 1:
            s += '  - Sword' 
        if self.id%3 == 2:
            s += '  - B.Axe'
        s += '\nid        = {}'.format(self.id)
        s += '\nhome      = {}'.format(self.home)    
        s += '\n\npos      = {}'.format(self.pos)
        s += '\norderStat = {}'.format(self.orderStat)
        s += '\nhideStat  = {}'.format(self.hideStat)
        s += '\ntreat     = {}'.format(self.treat)
        return s

    def injury(self):
        self.pos = self.home[:]
        self.orderStat = 0
        self.hideStat = 0
        self.treat = 18 + 1

    def action(self,game,acao,budget): 

        cont = False
        custo = 0
        if acao == 0:
            pass
        elif acao < 5:
            if budget >= 4:
                cont = self.occupy(game,acao)
                custo = 4
        elif acao < 9:
            if budget >= 2:
                cont = self.move(game,acao)
                custo = 2
        elif acao == 9:
            if budget >= 1:
                cont = self.hide(game)
                custo = 1
        return cont, custo

    def occupy(self, game, acao):
        #Occupies neighboring sections

        #CONDICOES:
        #   - Nao pode ocupar se estiver escondido

        #   - Home positions não podem ser ocupadas
        
        if self.hideStat == 1: #Se esta escondido, nao pode ocupar
            print('Samurai escondido não pode atacar')
            return False

        atkArea = []
        for occPos in self.atkMask:
            atkArea.append([occPos[0],occPos[1]])

        #Rotacoes
        if acao == 1:
            pass
        elif acao == 2:
            for occPos in atkArea:
                occPos[0],occPos[1]=occPos[1],-occPos[0]
        elif acao == 3:
            for occPos in atkArea:
                occPos[0],occPos[1]=-occPos[0],-occPos[1]
        elif acao == 4:
            for occPos in atkArea:
                occPos[0],occPos[1]=-occPos[1],occPos[0]

        for occPos in atkArea:
            occPos[0] += self.pos[0]
            occPos[1] += self.pos[1]


        for i in range (len(atkArea)):
            if (atkArea[i][0]>=0 and atkArea[i][0]<=14 and atkArea[i][1]>=0 and atkArea[i][1]<=14): #casa a ser ocupada dentro do tabuleiro
                if (atkArea[i] not in game.homes): #home position
                    game.tab[atkArea[i][1]][atkArea[i][0]] = self.id +3*self.player-3

                '''Se tiver samurai inimigo, manda ele pra home dele e atualiza trear status'''

                if self.player == 1:
                    for samurai2 in game.p2.samurais:
                        if samurai2.pos == atkArea[i]:
                            print('Samurai machucado')
                            samurai2.injury()
                if self.player == 2:
                    for samurai1 in game.p1.samurais:
                        if samurai1.pos == atkArea[i]:
                            print('Samurai machucado')
                            samurai1.injury()
        return True    

    def move(self, game, acao):

        #Moves to one of the adjacent sections.

        #Condições: 
        #   - (1) If the samurai is not hiding itself, it cannot move to a sections in which a non-hiding samurai is in.
        #   - (2) A samurai hiding itself can only move to a friendly territory section. 
        #   - (3) Whether showing or hiding itself, home positions of other samurai cannot be entered.

        #   - (4) Extra (Não falado no Rules): Não sair do tabuleiro
         
        #Intrucoes:
        #The move direction is specified as 5 for southward, 6
        # for eastward, 7 for northward, and 8 for westward

        #As condicoes dependem da casa que o samurai quer ir, assim sendo, (x,y) corresponde a casa que se deseja chegar.
        if acao == 5: #south
            x = self.pos[0]
            y = self.pos[1] + 1
        elif acao == 6: #east
            x = self.pos[0] + 1
            y = self.pos[1]
        elif acao == 7: #north
            x = self.pos[0]
            y = self.pos[1] - 1
        elif acao == 8: #west
            x = self.pos[0] - 1
            y = self.pos[1]


        #(4) Sair do Tabuleiro
        size = game.size
        if (x < 0 or x >= size or y < 0 or y >= size): #fora do tabuleiro
            print('Samurai não pode sair tabuleiro')
            return False

        #(1) Colisão de dois samurais aparecendo:
        elif (self.hideStat == 0):
            for samurai in game.p1.samurais + game.p2.samurais:
                if samurai.hideStat == 0 and samurai.pos == [x,y]:
                    print('Samurai não pode entrar em casa ocupada')
                    return False

        #(2) Samurai scondido só pode ir para casa aliada
        elif (self.hideStat==1):
            if (self.player == 1) and (game.tab[y][x] not in [0,1,2]):
                    print('Samurai escondido não pode sair de area amiga')
                    return False
            elif (self.player == 2) and (game.tab[y][x] not in [3,4,5]):
                    print('Samurai escondido não pode sair de area amiga')
                    return False

        #(3) Não pode entrar em home positions que não é a sua prória
        elif ([x,y] in game.homes) and ([x,y] != self.home): #home position
            print('Samurai não pode entrar em home positions que não seja a sua própria')
            return False

        #Moving
        self.pos[0] = x
        self.pos[1] = y
        return True

    def hide(self, game):
        #Switches its showing state

        #Concicoes
        #(1) Hiding is only possible when the samurai is in a friendly territory section.
        #(2) Showing is not possible if there is another non-hiding samurai, either friendly or enemy, in the same section.
      
        #(1) Verifica se está escondendo em território não amigo
        if self.hideStat == 0:      
            if self.player == 1:
                if game.tab[self.pos[1]][self.pos[0]] not in [0,1,2]:
                    print ('Samurai não pode se esconder em território não amigo')
                    return False
            else:
                if game.tab[self.pos[1]][self.pos[0]] not in [3,4,5]:
                    print ('Samurai não pode se esconder em território não amigo')
                    return False

        #(2) Verifica se está tentando aparecer onde já tem algum samurai aparecendo
        if (self.hideStat == 1):
            for samurai in game.p1.samurais + game.p2.samurais:
                if samurai.hideStat == 0 and samurai.pos == self.pos:
                    print ('Samurai não pode aparecer onde já tem um samurai aparecendo')
                    return False

        #Switching state
        self.hideStat = 1-self.hideStat
        return True


def main():

    score1 = 0
    score2 = 0

    server = Server()
    server.aguardar_jogadores()

    game = Game()

    for partida in range (2):

        game.__init__()

        while game.turn < MAX_TURN:

            server.send_turn(1, game.view(1))
            server.send_turn(2, game.view(2))

            if partida == 0:
                turno_player = game.turn%2 + 1
            elif partida == 1:
                turno_player = 2-game.turn%2

            print('Turno {}: player {}'.format(game.turn, turno_player))

            comando = server.recv_comandos(turno_player)

            if turno_player == 1:
                game.p1.order(comando,game)
            else:
                game.p2.order(comando,game)

            game.turn += 1
            if game.turn%6 == 0:
                game.clearOrderStat()

            game.heal()

        score1 += game.score(1)
        score2 += game.score(2)

        server.send_scores(score1, score2)

main()
