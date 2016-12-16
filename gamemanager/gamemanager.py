##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

from server import Server

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

        #Definindo as Homes Positions
        homes = []
        for i in range(len(self.p1.samurais)):
            self.tab[self.p1.samurais[i].y][self.p1.samurais[i].x] = i
            homes.append([(self.p1.samurais[i].y),(self.p1.samurais[i].x)])
        for i in range(len(self.p2.samurais)):
            self.tab[self.p2.samurais[i].y][self.p2.samurais[i].x] = i + 3
            homes.append([(self.p2.samurais[i].y),(self.p2.samurais[i].x)])
       
        self.homes = homes

    def view(self,player):
        #recebe todos os dados (turno, samurais, tabuleiro)

        sT = str(self.turn)

        sS = ''
        if player != 2:
            for samurai1 in self.p1.samurais:
                sS += '\n'
                sS += str(samurai1.x) + ' '#x
                sS += str(samurai1.y) + ' '#y
                sS += str(samurai1.order) + ' '#orderstatus
                sS += str(samurai1.hide) + ' '#showingstatus
                sS += str(samurai1.treat)#treatmentturns
            for samurai2 in self.p2.samurais:
                
                vendo = False
                for samurai1 in self.p1.samurais:
                    if self.distancia(samurai1.x,samurai2.x,samurai1.y,samurai2.y)<=5:
                        vendo = True
                if vendo:
                    sS += '\n'
                    sS += str(samurai2.x) + ' '#x
                    sS += str(samurai2.y) + ' '#y
                    sS += str(samurai2.order) + ' '#orderstatus
                    sS += str(samurai2.hide) + ' '#showingstatus
                    sS += str(samurai2.treat)#treatmentturns
                else:
                    sS += '\n'
                    sS += "-1 "
                    sS += "-1 "
                    sS += str(samurai2.order) + ' '#orderstatus
                    sS += "-1 "
                    sS += str(samurai2.treat)#treatmentturns

        else:
            for samurai2 in self.p2.samurais:
                sS += '\n'
                sS += str(samurai2.x) + ' '#x
                sS += str(samurai2.y) + ' '#y
                sS += str(samurai2.order) + ' '#orderstatus
                sS += str(samurai2.hide) + ' '#showingstatus
                sS += str(samurai2.treat) #treatmentturns             
            for samurai1 in self.p1.samurais:
                vendo = False
                for samurai2 in self.p2.samurais:
                    if self.distancia(samurai1.x,samurai2.x,samurai1.y,samurai2.y)<=5:
                        vendo = True
                if vendo:
                    sS += '\n'
                    sS += str(samurai1.x) + ' '#x
                    sS += str(samurai1.y) + ' '#y
                    sS += str(samurai1.order) + ' '#orderstatus
                    sS += str(samurai1.hide) + ' '#showingstatus
                    sS += str(samurai1.treat)#treatmentturns
                else:
                    sS += '\n'
                    sS += "-1 "
                    sS += "-1 "
                    sS += str(samurai1.order) + ' '#orderstatus
                    sS += "-1 "
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
                        x2 = self.p1.samurais[i].x
                        y2 = self.p1.samurais[i].y
                        if self.distancia(x1,x2,y1,y2)<=5:
                            newTab[y1][x1] = self.tab[y1][x1]

        if player == 2:
            for y1 in range (size):
                for x1 in range (size):
                    for i in range(len(self.p1.samurais)):
                        x2 = self.p2.samurais[i].x
                        y2 = self.p2.samurais[i].y
                        if self.distancia(x1,x2,y1,y2)<=5:
                            #Invertendo os samurais para o player2 (0>3,1>4,2>5,3>0,4>1,5>2)
    
                            if self.tab[y1][x1] < 3: #0>3,1>4,2>5
                                newTab[y1][x1] = self.tab[y1][x1]+3
                            elif self.tab[y1][x1] < 6: #3>0,4>1,5>2
                                newTab[y1][x1] = self.tab[y1][x1]-3
                            else:
                                newTab[y1][x1] = self.tab[y1][x1]

                                    
        sM =''
        for y in range(len(newTab)):
            sM += '\n'
            for x in range(len(newTab)-1):
                sM += str(newTab[y][x]) + ' '
            sM += str(newTab[y][x])

        s = sT + sS + sM
        
        return(s)

    def score(self,player):

        size = self.size

        count = 0
        if player == 1:
            for y in range (size):
                for x in range (size):
                    for i in range(len(self.p1.samurais)):
                        if self.p1.samurais[i].ID == self.tab[y][x]:
                            count += 1
        elif player == 2:
            for y in range (size):
                for x in range (size):
                    for i in range(len(self.p2.samurais)):
                        if self.p2.samurais[i].ID + 3 == self.tab[y][x]:
                            count += 1
        return count
                       
 
    def distancia(self,x1,x2,y1,y2):
        d = abs(x1-x2)+abs(y1-y2)
        return d


class Jogador:
    def __init__(self,player):
        
        samurais = []
        if player == 1:
            samurais.append(Samurai(0,0,0))
            samurais.append(Samurai(1,0,7))
            samurais.append(Samurai(2,7,0))
        elif player == 2:
            samurais.append(Samurai(0,14,14))
            samurais.append(Samurai(1,14,7))
            samurais.append(Samurai(2,7,14))                
        self.samurais = samurais

    def order(self, order,game):
        game.turn += 1
        budget = 7
        cont = True

        order = order.split(' ')

        if order[0] in [1,2,3]
            ID = int(order.pop(0))
        else: 
            print('Id do samurai invalido, perdeu a vez')
            return

        while order and cont:
            acao = order.pop(0)
            if acao in [0,1,2,3,4,5,6,7,8,9]:
                cont, custo = self.action(game,acao,budget)
                budget -= custo
            else: 
                cont = False
                print('Order invalida')

class Samurai:
    def __init__(self,weaponID,x,y):
        self.ID = weaponID      
        self.homeX = x
        self.homeY = y
        self.x = x
        self.y = y
        self.order = 0
        self.hide = 0
        self.treat = 0

        if self.ID == 0:
            mask = [[0,1],[0,2],[0,3],[0,4]]
        elif self.ID == 1:
            mask = [[0,2],[0,1],[1,1],[1,0],[2,0]]
        elif self.ID == 2:
            mask = [[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]

        self.mask = mask

    def action(self,game,acao,budget):

        if self.treat > 0: #se esta machucado nao joga
            print('Samurai machucado não joga')
            return False
        if self.order == 1: #se ja jogou, nao joga
            print('Samurai já jogou nesse período')
            return False

        cont = False
        custo = 0

        if acao == 0:
            pass
        elif acao < 5:
            if budget >= 4:
                cont = self.occupy(acao,game)
                custo = 4
        elif acao < 9:
            if budget >= 2:
                cont = self.move(acao,game)
                custo = 2
        elif acao == 9:
            if budget >= 1:
                cont = self.hide(game)
                custo = 1
        return cont, custo

    def move(self, acao, game):
        if acao == 5: #south
            x = self.x
            y = self.y + 1
        elif acao == 6: #east
            x = self.x + 1
            y = self.y
        elif acao == 7: #north
            x = self.x
            y = self.y - 1
        elif acao == 8: #west
            x = self.x - 1
            y = self.y

        '''verifica se o movimento eh valido'''
        
        size = game.size
        if (x < 0 or x >= size or y < 0 or y >= size): #fora do tabuleiro
            print('Samurai não pode sair tabuleiro')
            return False

        if ([x,y] in game.homes): #home position
            print('Samurai não pode entrar em home positions')
            return False

        if (self.hide==1): #samurai escondido e saindo de area conquistada pelo time 
            if(game.tabuleiro[y][x] != 0 and game.tabuleiro[y][x] != 1 and game.tabuleiro[y][x] != 3):
                return False

        if (self.hide == 0): #dois samurais aparecendo na mesma posicao
            for i in range (3):
                if (game.p1.samurais[i].hide == 0):
                    if ([x,y] == [game.p1.samurais[i].x, game.p1.samurais[i].y]):
                        return False
                if (game.p2.samurais[i].hide == 0):
                    if ([x,y] == [game.p2.samurais[i].x, game.p2.samurais[i].y]):
                        return False

        self.x = x
        self.y = y
        return True

    def occupy(self, acao, game):
        newMask = []
        for pos in self.mask:
            newMask.append([pos[0],pos[1]])

        # if self.hide == 1: #Se esta escondido, nao pode ocupar
        #     return False

        #Rotacoes
        if acao == 1:
            pass
        elif acao == 2:
            for pos in newMask:
                pos[0],pos[1]=pos[1],-pos[0]
        elif acao == 3:
            for pos in newMask:
                pos[0],pos[1]=-pos[0],-pos[1]
        elif acao == 4:
            for pos in newMask:
                pos[0],pos[1]=-pos[1],pos[0]

        for pos in newMask:
            pos[0] += self.x
            pos[1] += self.y


        for i in range (len(newMask)):
            if (newMask[i][0]>=0 and newMask[i][0]<=14 and newMask[i][1]>=0 and newMask[i][1]<=14): #casa a ser ocupada dentro do tabuleiro
                if ([newMask[i][0], newMask[i][1]] not in game.homes): #home position
                    game.tab[newMask[i][1]][newMask[i][0]] = self.ID
                    '''Se tiver samurai inimigo, manda ele pra home dele e atualiza trear status dele
                       turno par p1, impar p2 (pra saber se eh aliado ou inimigo'''

        return True    

    def hide(self, game):
        if (game.tabuleiro[self.y][self.x]<0 and game.tabuleiro[self.y][self.x]>3): #esconder em territorio amigo
            return False

        if (self.hide == 0): #dois samurais aparecendo na mesma posicao
            for i in range (3):
                if (game.p1.samurais[i].hide == 0):
                    if ([x,y] == [game.p1.samurais[i].x, game.p1.samurais[i].y]):
                        return False
                if (p2.game.p2.samurais[i].hide == 0):
                    if ([x,y] == [game.p2.samurais[i].x, game.p2.samurais[i].y]):
                        return False

        self.hide = 1-self.hide
        return True

def main():

    score1 = 0
    score2 = 0

    server = Server()
    server.aguardar_jogadores()

    #partida1:
    game = Game()

    while game.turn < 96:
        server.send_turn(1,game.view(1))
        server.send_turn(2,game.view(2))

        turno_player = game.turn%2+1
        print(turno_player)

        comando = server.recv_comandos(turno_player)

        if turno_player == 1:
            game.p1.order(comando,game)
        else:
            game.p2.order(comando,game)

        game.turn+=1#temporario

    score1 += game.score(1)
    score2 += game.score(2)


    #partida2:
    game = Game()

    while game.turn < 96:
        server.send_turn(1,game.view(1))
        server.send_turn(2,game.view(2))

        turno_player = 2-game.turn%2

        comando = server.recv_comandos(turno_player)

        if turno_player == 1:
            game.p1.order(comando,game)
        else:
            game.p2.order(comando,game)
            
        game.turn+=1#temporario

    score1 += game.score(1)
    score2 += game.score(2)

#main()

g = Game()
print(g.view(2))
g.__init__()