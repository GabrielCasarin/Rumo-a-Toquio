##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

from .gamemanager import Game, Jogador, Samurai


class Simulador:
    def __init__(self):
        self.game = Game()

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, s):
        self.__estado = s.copy()
        # atualizar tabuleiro
        self.game.tab = self.__estado.tabuleiro
        self.game.turn = self.__estado.turno
        # e samurais
        for i in range(3):
            self.game.p1.samurais[i].pos[:] = self.__estado.samurais[i][:2]
            self.game.p1.samurais[i].orderStat = self.__estado.samurais[i][2]
            self.game.p1.samurais[i].hideStat = self.__estado.samurais[i][3]
            self.game.p1.samurais[i].treat = self.__estado.samurais[i][4]
        for i in range(3, 6):
            self.game.p2.samurais[i - 3].pos[:] = self.__estado.samurais[i][:2]
            self.game.p2.samurais[i - 3].orderStat = self.__estado.samurais[i][2]
            self.game.p2.samurais[i - 3].hideStat = self.__estado.samurais[i][3]
            self.game.p2.samurais[i - 3].treat = self.__estado.samurais[i][4]

    def atuar(self, sam_id, acao):

        sAntes = self.estado.copy()

        jogador = self.game.jogadores[self.__estado.player]

        jogadaValida = True

        samurai = jogador.samurais[sam_id]

        if samurai.treat > 0:  # se esta machucado nao joga
            jogadaValida = False

        if samurai.orderStat == 1:  # se ja jogou, nao joga
            jogadaValida = False

        if jogadaValida:
                jogadaValida, custo, msg = samurai.action(acao, self.__estado.budget)
        
        if not jogadaValida:
            custo = 100     # deixar isso elegante depois
        self.estado.budget -= custo
        #print('custo:', custo, ' budget:', self.estado.budget)

        if self.estado.budget >= 0:
            # atualizar estado

            self.estado.samurais = []
            # atualizar samurais
            for sam1 in self.game.p1.samurais:
                listaSam1 = [sam1.pos[0], sam1.pos[1], sam1.orderStat, sam1.hideStat, sam1.treat]
                self.estado.samurais.append(listaSam1)

            for sam2 in self.game.p2.samurais:
                listaSam2 = [sam2.pos[0], sam2.pos[1], sam2.orderStat, sam2.hideStat, sam2.treat]
                self.estado.samurais.append(listaSam2)

            # atualizar tabuleiro
            self.estado.tabuleiro = []
            for el in self.game.tab:
                self.estado.tabuleiro.append(list(el))
            #armazenar(acao, self.estado)
