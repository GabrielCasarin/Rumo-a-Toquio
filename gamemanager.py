##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

from server import Server
from util import distancia
from config import *


class Game:
    #criar tabuleiro:
    def __init__(self):

        #definindo o Turno
        self.turn = 0

        #definindo o Tabuleiro
        row = SIZE*[8]
        tabuleiro = []
        for i in range(SIZE):
            tabuleiro.append(row[:])
        self.tab = tabuleiro

        #definindo os Jogadores

        self.p1 = Jogador(1, self)
        self.p2 = Jogador(2, self)
        self.jogadores = [self.p1, self.p2]


        #Definindo e preenchenco as Homes Positions
        homes = []#player, pos
        for i in range(len(self.p1.samurais)):
            self.tab[self.p1.samurais[i].pos[1]][self.p1.samurais[i].pos[0]] = i
            homes.append(self.p1.samurais[i].pos[:])
        for i in range(len(self.p2.samurais)):
            self.tab[self.p2.samurais[i].pos[1]][self.p2.samurais[i].pos[0]] = i + 3
            homes.append(self.p2.samurais[i].pos[:])
        self.homes = homes

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
                sS += str(samurai1.treat)  #treatmentturns
            for samurai2 in self.p2.samurais:

                vendo = False
                for samurai1 in self.p1.samurais:
                    if distancia(samurai1.pos[0],samurai2.pos[0],samurai1.pos[1],samurai2.pos[1])<=DIST_VISAO and samurai2.hideStat == 0:
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
                    if distancia(samurai1.pos[0],samurai2.pos[0],samurai1.pos[1],samurai2.pos[1])<=DIST_VISAO and samurai1.hideStat == 0:
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

        elif player == -1:
            for samurai1 in self.p1.samurais:
                sS += '\n'
                sS += str(samurai1.pos[0]) + ' '#x
                sS += str(samurai1.pos[1]) + ' '#y
                sS += str(samurai1.orderStat) + ' '#orderstatus
                sS += str(samurai1.hideStat) + ' '#showingstatus
                sS += str(samurai1.treat) #treatmentturns
            for samurai2 in self.p2.samurais:
                vendo = True
                sS += '\n'
                sS += str(samurai2.pos[0]) + ' '#x
                sS += str(samurai2.pos[1]) + ' '#y
                sS += str(samurai2.orderStat) + ' '#orderstatus
                sS += str(samurai2.hideStat) + ' '#showingstatus
                sS += str(samurai2.treat)#treatmentturns

        elif player == -2:
            for samurai2 in self.p2.samurais:
                sS += '\n'
                sS += str(samurai2.pos[0]) + ' '#x
                sS += str(samurai2.pos[1]) + ' '#y
                sS += str(samurai2.orderStat) + ' '#orderstatus
                sS += str(samurai2.hideStat) + ' '#showingstatus
                sS += str(samurai2.treat) #treatmentturns
            for samurai1 in self.p1.samurais:
                vendo = True
                sS += '\n'
                sS += str(samurai1.pos[0]) + ' '#x
                sS += str(samurai1.pos[1]) + ' '#y
                sS += str(samurai1.orderStat) + ' '#orderstatus
                sS += str(samurai1.hideStat) + ' '#showingstatus
                sS += str(samurai1.treat)#treatmentturns

        row = SIZE*[9]
        newTab = []
        for i in range(SIZE):
            newTab.append(row[:])

        if player == 1:
            for y1 in range (SIZE):
                for x1 in range (SIZE):
                    for i in range(len(self.p1.samurais)):
                        x2 = self.p1.samurais[i].pos[0]
                        y2 = self.p1.samurais[i].pos[1]
                        if distancia(x1,x2,y1,y2) <= DIST_VISAO:
                            newTab[y1][x1] = self.tab[y1][x1]

        if player == 2:
            for y1 in range (SIZE):
                for x1 in range (SIZE):
                    for i in range(len(self.p2.samurais)):
                        x2 = self.p2.samurais[i].pos[0]
                        y2 = self.p2.samurais[i].pos[1]
                        if distancia(x1,x2,y1,y2) <= DIST_VISAO:

                            #Invertendo os samurais para o player2 (0>3,1>4,2>5,3>0,4>1,5>2)
                            if self.tab[y1][x1] < 3: #0>3,1>4,2>5
                                newTab[y1][x1] = self.tab[y1][x1]+3
                            elif self.tab[y1][x1] < 6: #3>0,4>1,5>2
                                newTab[y1][x1] = self.tab[y1][x1]-3
                            else:
                                newTab[y1][x1] = self.tab[y1][x1]
        if player == -1:
            for y1 in range (SIZE):
                for x1 in range (SIZE):
                    newTab[y1][x1] = self.tab[y1][x1]

        if player == -2:
            for y1 in range (SIZE):
                for x1 in range (SIZE):
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
            sM += str(newTab[y][SIZE-1])

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
    def __init__(self, player, game):

        if player == 1:
            self.samurais = [Samurai(i, game) for i in range(0,3)]
        elif player == 2:
            self.samurais = [Samurai(i, game) for i in range(3,6)]

        self.game = game

    def order(self, comando):
        budget = MAX_BUDGET
        cont = True

        comando = comando.split(' ')

        msg = "Jogava valida"

        ID = int(comando.pop(0))
        if ID in [0,1,2]:
            samurai = self.samurais[ID]
        else:
            msg = 'Id do samurai invalido, perdeu a vez'

        if samurai.treat > 0: #se esta machucado nao joga
            msg = 'Samurai machucado nao joga'
            cont = False

        if samurai.orderStat == 1: #se ja jogou, nao joga
            msg = 'Samurai ja jogou nesse periodo'
            cont = False
        else:
            samurai.orderStat = 1

        while comando and cont:
            acao = int(comando.pop(0))
            if acao in range(10):
                cont, custo, msg = samurai.action(acao, budget)
                budget -= custo
            else:
                cont = False
                msg = 'Codigo de acao invalido'

        print(msg)

        return msg


class Samurai:
    def __init__(self, num, game):

        #Home position
        delta = SIZE//2

        if num == 0:
            self.home = [ 0, 0]
        elif num == 1:
            self.home = [ 0, delta]
        elif num == 2:
            self.home = [ delta, 0]
        elif num == 3:
            self.home = [SIZE-1,SIZE-1]
        elif num == 4:
            self.home = [SIZE-1, SIZE-1-delta]
        elif num == 5:
            self.home = [SIZE-1-delta, SIZE-1]

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

        self.game = game

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

    def action(self, acao, budget):

        cont = False
        custo = 0
        msg = 'Sem budget suficiente'

        if acao == 0:
            msg = 'Jogada valida'
            pass
        elif 1 <= acao <= 4:
            if budget >= 4:
                cont, msg = self.occupy(acao)
            custo = 4
        elif 5 <= acao <= 8:
            if budget >= 2:
                cont, msg = self.move(acao)
            custo = 2
        elif acao == 9:
            if budget >= 1:
                cont, msg = self.hide()
            custo = 1

        return cont, custo, msg

    def occupy(self, acao):
        #Occupies neighboring sections

        #CONDICOES:
        #   - Nao pode ocupar se estiver escondido

        #   - Home positions não podem ser ocupadas

        if self.hideStat == 1: #Se esta escondido, nao pode ocupar
            return False, 'Samurai escondido nao pode atacar'

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
            if (atkArea[i][0]>=0 and atkArea[i][0]<=SIZE-1 and atkArea[i][1]>=0 and atkArea[i][1]<=SIZE-1): #casa a ser ocupada dentro do tabuleiro
                if (atkArea[i] not in self.game.homes): #home position
                    self.game.tab[atkArea[i][1]][atkArea[i][0]] = self.id +3*self.player-3

                    #Se tiver samurai inimigo, deixar injuried
                    if self.player == 1:
                        for samurai2 in self.game.p2.samurais:
                            if samurai2.pos == atkArea[i]:
                                print('Samurai machucado')
                                samurai2.injury()
                    if self.player == 2:
                        for samurai1 in self.game.p1.samurais:
                            if samurai1.pos == atkArea[i]:
                                print('Samurai machucado')
                                samurai1.injury()
        return True, 'Jogada válida'

    def move(self, acao):

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
        if (x < 0 or x >= SIZE or y < 0 or y >= SIZE): #fora do tabuleiro
            return False, 'Samurai nao pode sair tabuleiro'

        #(1) Colisão de dois samurais aparecendo:
        elif (self.hideStat == 0):
            for samurai in self.game.p1.samurais + self.game.p2.samurais:
                if samurai.hideStat == 0 and samurai.pos == [x,y]:
                    return False, 'Samurai nao pode entrar em casa ocupada'

        #(2) Samurai scondido só pode ir para casa aliada
        elif (self.hideStat==1):
            if (self.player == 1) and (self.game.tab[y][x] not in [0,1,2]):
                    return False, 'Samurai escondido nao pode sair de area amiga'
            elif (self.player == 2) and (self.game.tab[y][x] not in [3,4,5]):
                    return False, 'Samurai escondido nao pode sair de area amiga'

        #(3) Não pode entrar em home positions que não é a sua prória
        elif ([x,y] in self.game.homes) and ([x,y] != self.home): #home position
            return False, 'Samurai nao pode entrar em home positions que nao seja a sua propria'

        #Moving
        self.pos[0] = x
        self.pos[1] = y
        return True, 'Jogada valida'

    def hide(self):
        #Switches its showing state

        #Concicoes
        #(1) Hiding is only possible when the samurai is in a friendly territory section.
        #(2) Showing is not possible if there is another non-hiding samurai, either friendly or enemy, in the same section.

        #(1) Verifica se está escondendo em território não amigo
        if self.hideStat == 0:
            if self.player == 1:
                if self.game.tab[self.pos[1]][self.pos[0]] not in [0,1,2]:
                    return False, 'Samurai nao pode se esconder em territorio nao amigo'
            else:
                if self.game.tab[self.pos[1]][self.pos[0]] not in [3,4,5]:
                    return False, 'Samurai nao pode se esconder em territorio nao amigo'

        #(2) Verifica se está tentando aparecer onde já tem algum samurai aparecendo
        if (self.hideStat == 1):
            for samurai in self.game.p1.samurais + self.game.p2.samurais:
                if samurai.hideStat == 0 and samurai.pos == self.pos:
                    return False, 'Samurai nao pode aparecer onde ja tem um samurai aparecendo'

        #Switching state
        self.hideStat = 1 - self.hideStat
        return True, 'Jogada valida'


def main():

    #FUNCAO A IMPLEMENTAR:
    #PASSAR msg PARA O CLIENT PARA ELE IMPRIMIR NA TELA DO JOGADOR
    #usar o final do protocolo

    score1 = 0
    score2 = 0
    msg1 = 'Bom Jogo!'
    msg2 = 'Bom Jogo!'

    server = Server()
    server.aguardar_jogadores()

    game = Game()

    for partida in range (2):

        game.__init__()

        while game.turn < MAX_TURN:


            if partida == 0:
                turno_player = game.turn%2 + 1
            elif partida == 1:
                turno_player = 2-game.turn%2

            if TOTALMENTE_OBSERVAVEL:
                if COMENTARIO:
                    server.send_turn(1, game.view(-1)+'\n'+msg1)
                    server.send_turn(2, game.view(-2)+'\n'+msg2)
                else:
                    server.send_turn(1, game.view(-1))
                    server.send_turn(2, game.view(-2))
            else:
                if COMENTARIO:
                    server.send_turn(1, game.view(1)+'\n'+msg1)
                    server.send_turn(2, game.view(2)+'\n'+msg2)
                else:
                    server.send_turn(1, game.view(1))
                    server.send_turn(2, game.view(2))

            print('Turno {}: player {}'.format(game.turn, turno_player))



            comando = server.recv_comandos(turno_player)

            if turno_player == 1:
                msg1 = game.p1.order(comando)
            else:
                msg2 = game.p2.order(comando)

            game.turn += 1
            if game.turn%6 == 0:
                game.clearOrderStat()

            game.heal()

        score1 += game.score(1)
        score2 += game.score(2)

        server.send_scores(score1, score2)

# main()

def main_ia():
    from ai import AI, EstadosDB

    game = Game()

    estadosdb = EstadosDB()

    IA_1 = AI(player=0, treinar=True,  estadosdb=estadosdb)
    IA_2 = AI(player=1, treinar=False, estadosdb=estadosdb)

    score1 = 0
    score2 = 0

    for partida in range(1):

        game.__init__()

        while game.turn < MAX_TURN:

            print('OOOOOI EU SOU O tuRNO', game.turn)

            if partida == 0:
                turno_player = game.turn%2 + 1
            elif partida == 1:
                turno_player = 2-game.turn%2

            if turno_player == 1: #IA_1
                IA = IA_1
            else:
                IA = IA_2

            if TOTALMENTE_OBSERVAVEL:
                IA.set_turn(game.view(-turno_player))
            else:
                IA.set_turn(game.view(turno_player))

            comando = IA.get_comandos()

            if turno_player == 1:
                msg1 = game.p1.order(comando, game)
            else:
                msg2 = game.p2.order(comando, game)

            game.turn += 1
            if game.turn%6 == 0:
                game.clearOrderStat()

            game.heal()

        score1 += game.score(1)
        score2 += game.score(2)

    print(score1)
    print(score2)


    #IA_1.set_scores(score1, score2)
    #IA_2.set_scores(score1, score2)

    estadosdb.encerrar()

main_ia()
