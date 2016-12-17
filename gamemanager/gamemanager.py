##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

from server import Server

from util import distancia

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

    def reset_orderStats(self):
        for samurai1 in self.p1.samurais:
            samurai1.orderStat = 0
        for samurai2 in self.p2.samurais:
            samurai2.orderStat = 0

    def countdown_treat(self):
        for samurai1 in self.p1.samurais:
            if samurai1.treat > 0:
                samurai1.treat -= 1
        for samurai2 in self.p2.samurais:
            if samurai2.treat > 0:
                samurai2.treat -= 1

    def view(self,player):
        #recebe todos os dados (turno, samurais, tabuleiro)

        sT = str(self.turn)

        sS = ''
        if player != 2:
            for samurai1 in self.p1.samurais:
                sS += '\n'
                sS += str(samurai1.x) + ' '#x
                sS += str(samurai1.y) + ' '#y
                sS += str(samurai1.orderStat) + ' '#orderstatus
                sS += str(samurai1.hideStat) + ' '#showingstatus
                sS += str(samurai1.treat)#treatmentturns
            for samurai2 in self.p2.samurais:
                
                vendo = False
                for samurai1 in self.p1.samurais:
                    if distancia(samurai1.x,samurai2.x,samurai1.y,samurai2.y)<=5:
                        vendo = True
                if vendo:
                    sS += '\n'
                    sS += str(samurai2.x) + ' '#x
                    sS += str(samurai2.y) + ' '#y
                    sS += str(samurai2.orderStat) + ' '#orderstatus
                    sS += str(samurai2.hideStat) + ' '#showingstatus
                    sS += str(samurai2.treat)#treatmentturns
                else:
                    sS += '\n'
                    sS += "-1 "
                    sS += "-1 "
                    sS += str(samurai2.orderStat) + ' '#orderstatus
                    sS += "-1 "
                    sS += str(samurai2.treat)#treatmentturns

        else:
            for samurai2 in self.p2.samurais:
                sS += '\n'
                sS += str(samurai2.x) + ' '#x
                sS += str(samurai2.y) + ' '#y
                sS += str(samurai2.orderStat) + ' '#orderstatus
                sS += str(samurai2.hideStat) + ' '#showingstatus
                sS += str(samurai2.treat) #treatmentturns             
            for samurai1 in self.p1.samurais:
                vendo = False
                for samurai2 in self.p2.samurais:
                    if distancia(samurai1.x,samurai2.x,samurai1.y,samurai2.y)<=5:
                        vendo = True
                if vendo:
                    sS += '\n'
                    sS += str(samurai1.x) + ' '#x
                    sS += str(samurai1.y) + ' '#y
                    sS += str(samurai1.orderStat) + ' '#orderstatus
                    sS += str(samurai1.hideStat) + ' '#showingstatus
                    sS += str(samurai1.treat)#treatmentturns
                else:
                    sS += '\n'
                    sS += "-1 "
                    sS += "-1 "
                    sS += str(samurai1.orderStat) + ' '#orderstatus
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
                        if distancia(x1,x2,y1,y2)<=5:
                            newTab[y1][x1] = self.tab[y1][x1]

        if player == 2:
            for y1 in range (size):
                for x1 in range (size):
                    for i in range(len(self.p1.samurais)):
                        x2 = self.p2.samurais[i].x
                        y2 = self.p2.samurais[i].y
                        if distancia(x1,x2,y1,y2)<=5:
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
            sM += str(newTab[y][len(newTab)-1])

        s = sT + sS + sM
        
        return(s)

    def score(self,player):

        count = 0
        if player == 1:
            for linha in self.tab:
                for casa in linha:
                    for samurai in self.p1.samurais:
                        if samurai.id == casa:
                            count += 1
        elif player == 2:
            for linha in self.tab:
                for casa in linha:
                    for samurai in self.p2.samurais:
                        if samurai.id == casa:
                            count += 1
        return count
                       
 

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

    def order(self, comando, game):
        game.turn += 1
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

        samurai.orderStat

        while comando and cont:
            acao = int(comando.pop(0))
            if acao in [0,1,2,3,4,5,6,7,8,9]:
                cont, custo = samurai.action(game,acao,budget)
                budget -= custo
            else: 
                cont = False
                print('Order invalida')

class Samurai:
    def __init__(self,weaponID,x,y):
        self.id = weaponID      
        self.homeX = x
        self.homeY = y
        self.x = x
        self.y = y
        self.orderStat = 0
        self.hideStat = 0
        self.treat = 0

        if self.id == 0:
            mask = [[0,1],[0,2],[0,3],[0,4]]
        elif self.id == 1:
            mask = [[0,2],[0,1],[1,1],[1,0],[2,0]]
        elif self.id == 2:
            mask = [[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]

        self.mask = mask

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

    def move(self, game, acao):
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

        if (self.hideStat==1): #samurai escondido e saindo de area conquistada pelo time
            #SE JOGADOR 1
            if [self.homeX,self.homeY] in game.homes[:len(game.p1.samurais)]:
                if(game.tab[y][x] in [0,1,2]):
                    print('Samurai escondido não pode ir pra area inimiga')
                    return False
            elif [self.homeX,self.homeY] in game.homes[len(game.p2.samurais):]:#se jogador 2
                if(game.tab[y][x] in [3,4,5]):
                    print('Samurai escondido não pode ir pra area inimiga')
                    return False

        if (self.hideStat == 0): #dois samurais aparecendo na mesma posicao
            for i in range (3):
                if (game.p1.samurais[i].hideStat == 0):
                    if ([x,y] == [game.p1.samurais[i].x, game.p1.samurais[i].y]):
                        print('Samurai não pode entrar em casa ocupada')
                        return False
                if (game.p2.samurais[i].hideStat == 0):
                    if ([x,y] == [game.p2.samurais[i].x, game.p2.samurais[i].y]):
                        print('Samurai não pode entrar em casa ocupada')
                        return False

        self.x = x
        self.y = y
        return True

    def occupy(self, game, acao):
        
        if self.hideStat == 1: #Se esta escondido, nao pode ocupar
            print('Samurai escondido não pode atacar')
            return False

        newMask = []
        for casa in self.mask:
            newMask.append([casa[0],casa[1]])

        #Rotacoes
        if acao == 1:
            pass
        elif acao == 2:
            for casa in newMask:
                casa[0],casa[1]=casa[1],-casa[0]
        elif acao == 3:
            for casa in newMask:
                casa[0],casa[1]=-casa[0],-casa[1]
        elif acao == 4:
            for casa in newMask:
                casa[0],casa[1]=-casa[1],casa[0]

        for casa in newMask:
            casa[0] += self.x
            casa[1] += self.y


        for casa in newMask:
            if (casa[0]>=0 and casa[0]<game.size and casa[1]>=0 and casa[1]<game.size): #casa a ser ocupada dentro do tabuleiro
                if ([casa[0], casa[1]] not in game.homes): #home position
                    if [self.homeX,self.homeY] in game.homes[:len(game.p1.samurais)]:
                        game.tab[casa[1]][casa[0]] = self.id
                    else:
                        game.tab[casa[1]][casa[0]] = self.id+3

                    '''Se tiver samurai inimigo, manda ele pra home dele e atualiza treat status dele
                    turno par p1, impar p2 (pra saber se eh aliado ou inimigo'''
                    #SE JOGADOR 1
                    if [self.homeX,self.homeY] in game.homes[:len(game.p1.samurais)]:
                        for samurai2 in game.p2.samurais:
                            if samurai2.x == casa[0] and samurai2.y == casa[1]:
                                samurai2.x = samurai2.homeX
                                samurai2.y = samurai2.homeY
                                samurai2.treat = 18

                    else:
                        for samurai1 in game.p1.samurais:
                            if samurai1.x == casa[0] and samurai1.y == casa[1]:
                                samurai1.x = samurai1.homeX
                                samurai1.y = samurai1.homeY
                                samurai1.treat = 18            

        return True    

    def hide(self, game):
      

        #verificando se está tentando esconder em território inimigo
        if self.hideStat == 0:      
            if [self.homeX,self.homeY] in game.homes[:len(game.p1.samurais)]: #verifica se é player1
                if game.tab[self.y][self.x] in [3,4,5]:
                    print ('Samurai não pode se esconder em território inimigo')
                    return False
            else:
                if game.tab[self.y][self.x] in [0,1,2]:
                    print ('Samurai não pode se esconder em território inimigo')
                    return False
       
        #verificando se está tentando aparecer onde já tem algum samurai aparecendo
        if (self.hideStat == 1):
            for i in range (3):
                if (game.p1.samurais[i].hideStat == 0) and ([self.x,self.y] == [game.p1.samurais[i].x, game.p1.samurais[i].y]):
                    print ('Samurai não pode aparecer onde já tem um samurai aparecendo')
                    return False
                if (game.p2.samurais[i].hideStat == 0) and ([self.x,self.y] == [game.p2.samurais[i].x, game.p2.samurais[i].y]):
                    print ('Samurai não pode aparecer onde já tem um samurai aparecendo')
                    return False

        self.hideStat = 1-self.hideStat
        return True

def main():

    score1 = 0
    score2 = 0

    server = Server()
    server.aguardar_jogadores()

    #partida1:
    game = Game()

    while game.turn < 96:

        game.countdown_treat()

        if game.turn%6 == 0:
            game.reset_orderStats()

        server.send_turn(1,game.view(1))
        server.send_turn(2,game.view(2))

        turno_player = game.turn%2+1
        print(turno_player)

        comando = server.recv_comandos(turno_player)

        if turno_player == 1:
            game.p1.order(comando,game)
        else:
            game.p2.order(comando,game)

    score1 += game.score(1)
    score2 += game.score(2)


    #partida2:
    game = Game()

    while game.turn < 96:

        #inverte-se os indices de player1 e player2

        game.countdown_treat()

        if game.turn%6 == 0:
            game.reset_orderStats()


        turno_player = 2-game.turn%2

        comando = server.recv_comandos(turno_player)

        if turno_player == 1:
            game.p2.order(comando,game)
        else:
            game.p1.order(comando,game)

    score1 += game.score(1)
    score2 += game.score(2)

main()


