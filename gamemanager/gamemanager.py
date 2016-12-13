##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################


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
        self.p1 = Jogador(0)
        self.p2 = Jogador(1)

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
        if player <> 1:
            for i in range (3):
                sS += '\n'
                sS += str(self.p1.samurais[i].x) + ' '#x
                sS += str(self.p1.samurais[i].y) + ' '#y
                sS += str(self.p1.samurais[i].order) + ' '#orderstatus
                sS += str(self.p1.samurais[i].hide) + ' '#showingstatus
                sS += str(self.p1.samurais[i].treat)#treatmentturns

            for i in range (3):
                sS += '\n'
                sS += str(self.p2.samurais[i].x) + ' '#x
                sS += str(self.p2.samurais[i].y) + ' '#y
                sS += str(self.p2.samurais[i].order) + ' '#orderstatus
                sS += str(self.p2.samurais[i].hide) + ' '#showingstatus
                sS += str(self.p2.samurais[i].treat)#treatmentturns

        else:
            
            for i in range (3):
                sS += str(self.p2.samurais[i].x) + ' '#x
                sS += str(self.p2.samurais[i].y) + ' '#y
                sS += str(self.p2.samurais[i].order) + ' '#orderstatus
                sS += str(self.p2.samurais[i].hide) + ' '#showingstatus
                sS += str(self.p2.samurais[i].treat) +'\n'#treatmentturns
                
            for i in range (3):
                sS += str(self.p1.samurais[i].x) + ' '#x
                sS += str(self.p1.samurais[i].y) + ' '#y
                sS += str(self.p1.samurais[i].order) + ' '#orderstatus
                sS += str(self.p1.samurais[i].hide) + ' '#showingstatus
                sS += str(self.p1.samurais[i].treat) +'\n'#treatmentturns


        if player == -1:
            newTab = self.tab


        else:
                
            size = self.size
            row = size*[9]
            newTab = []
            for i in range(size):
                newTab.append(row[:])

            if player == 0:
                for y1 in range (size):
                    for x1 in range (size):
                        for i in range(len(self.p1.samurais)):
                            x2 = self.p1.samurais[i].x
                            y2 = self.p1.samurais[i].y
                            if self.distancia(x1,x2,y1,y2)<=5:
                                newTab[y1][x1] = self.tab[y1][x1]

            if player == 1:
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

                                    
            #transformar newTab em str
            #print(newTab)
            sM =''
            for y in range(len(newTab)):
                sM += '\n'
                for x in range(len(newTab)-1):
                    sM += str(newTab[y][x]) + ' '
                sM += str(newTab[y][x])
        s = sT + sS + sM
        
        print(s)
        return(s)
            
    def score(self,player):

        size = self.size

        count = 0
        if player == 0:
            for y in range (size):
                for x in range (size):
                    for i in range(len(self.p1.samurais)):
                        if self.p1.samurais[i].ID == self.tab[y][x]:
                            count += 1
        elif player == 1:
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

        self.p1 = player
        
        samurais = []
        if player == 0:
            samurais.append(Samurai(0,0,0))
            samurais.append(Samurai(1,0,7))
            samurais.append(Samurai(2,7,0))
        elif player == 1:
            samurais.append(Samurai(0,14,14))
            samurais.append(Samurai(1,14,7))
            samurais.append(Samurai(2,7,14))                
        self.samurais = samurais

    def view(self,game):
        #recebe todos os dados (turno, samurais, tabuleiro visivel)
        pass

    def order(self, order):
        #verifica se eh valido
        #order = order.split(' ')
        
        ID = order[0]
        
        for i in range(1,len(order)):
            self.samurais[ID].action(order)
            
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

    def action(self,acao,game):

        #validar tretment status e order status
      
        if acao == 0:
            cont = self.stop(self)
        elif acao < 5:
            cont = self.occupy(self,acao,game)
        elif acao < 9:
            cont = self.move(self,acao,game)
        elif acao == 9:
            cont = self.hide(self,game)


    def stop(self):
        return False

    def move(self,direcao):
        if direcao == 5: #south
            #verificar se possivel
            self.y += 1
        elif direcao == 6: #east
            #verificar se possivel
            self.x += 1
        elif direcao == 7: #north
            #verificar se possivel
            self.y -= 1
        elif direcao == 8: #west
            #verificar se possivel
            self.x -= 1

        return True

    def occupy(self,direcao):

        if direcao == 1: #south
            #aplicar mascara no tabuleiro
            pass
        elif direcao == 2: #east
            #aplicar mascara no tabuleiro
            pass
        elif direcao == 3: #north
            #aplicar mascara no tabuleiro
            pass
        elif direcao == 4: #west
            #aplicar mascara no tabuleiro
            pass

        return True

    def hide(self):
        #verificar se possivel
        self.hide = 1-self.hide

        return True

def main():
    score1 = 0
    score2 = 0
    game = Game()
    

g = Game()
    
