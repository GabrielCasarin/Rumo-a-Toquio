##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################


import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation

from database.JogadasDB import JogadasDB
from database.EstadosDB import Estado

from config import *

from simulador import Simulador

class AI:
    def __init__(self, player, treinar, estadosdb, camadas=[82, 40, 30]):
        super(AI, self).__init__()
        self.player = player    # 0 ou 1 ~~ para indicar quem voce eh
        self.treinar = treinar  # boolean

        # Rede Neural
        self.Q = Sequential()

        self.Q.add(Dense(output_dim=camadas[1], input_dim=camadas[0]))

        for i in range(1, len(camadas) - 1):
            self.Q.add(Activation("sigmoid"))
            self.Q.add(Dense(output_dim=camadas[i + 1]))

        self.Q.compile(loss='mean_squared_error', optimizer='SGD')

        self.Q.save('model{}.h5'.format(self.player))

        # self.epsilon = 0.2
        # self.batch_size = 16

        if self.treinar:
            self.jogosDB = JogadasDB()

        self.bd = estadosdb

        self.simulador = Simulador()

    def set_turn(self, msg):
        msg = msg.split('\n')

        turno = int(msg[0])

        samurais = [x.split() for x in msg[1:7]]

        for i in range(len(samurais)):
            for j in range(5):
                samurais[i][j] = int(samurais[i][j])

        tabuleiro = [x.split() for x in msg[7:]]
        for i in range(len(tabuleiro)):
            for j in range(len(tabuleiro)):
                tabuleiro[i][j] = int(tabuleiro[i][j])

        budget = MAX_BUDGET

        self.estado = self.bd.get_estado(
            turno, samurais, tabuleiro, budget, self.player)

     def reward(self, sAntes, sDepois):

        rAcao = -0.1    # (1) reward Acao
        rAcaoInv = -5   # (2) reward Acao Invalida
        rEuCqN  = +1    # (3) reward Eu         Conquistar  Neutro
        rEuCqI  = +2    # (4) reward Eu         Conquistar  Inimigo
        rICqN   = -1    # (5) reward Inimigo    Conquistar  Neutro
        rICqEu  = -2    # (6) reward Inimigo    Conquistar  Eu
        rEuKI = +10     # (7) reward Eu         kill        Inimigo
        rIKEu = -10     # (8) reward Inimigo    kill        Eu

        sAntes = sAntes
        sDepois = self.estado

        reward = 0
        if True: # (1)
            reward += rAcao
        if True: # (2)
            reward += rAcaoInv
        if True: # (3)
            #for area eu conquista neutra
            reward += rEuCqN
        if True: # (4)
            #for area eu conquista inimigo
            reward += rEuCqI
        if True: # (5)
            #for area ininigo conquista neutro
            reward += rICqN
        if True: # (6)
            #for area inimigo conquista eu
            reward += rICqEu
        if True: # (7)
        # if is enemy.sam in sNovo.samurais injuried and sVelho.samurai not injuried
            reward += rIKEu
        if True: # (8)
        # if is meu.sam in sNovo.samurais injuried and sVelho.samurai not injuried
            reward += rEuKI

        # TODO
        # return reward ?


    def jogar(self):

        listaAcao = []
        acao = -1
        sam = -1
        estado = self.estado
        self.simulador.estado = estado

        while estado.budget > 0 and acao != 0:

            if self.treinar:
                self.jogosDB.addState(estado)

            vectQ = self.Q.predict(estado.to_vect())[0]

            if not listaAcao:
                i = np.argmax(vectQ)
                sam = i // 10
                listaAcao.append(str(sam))
            else:
                vectQ = vectQ[10 * sam:10 * sam + 10]
                i = np.argmax(vectQ)
            acao = i % 10

            if self.treinar:
                self.jogosDB.addAcao(acao)

            listaAcao.append(str(acao))

            self.simulador.atuar(sam, acao)
            estado = self.simulador.estado

            #atualizarEstado simulando

            # self.armazenarAcao() #armazenar o estado atual e a acao

            # simulador.atuar(sam, acao)

        # armazenar o estado e as acoes

        self.listaAcao = listaAcao

    def get_comandos(self):
        self.jogar()
        return ' '.join(self.listaAcao)


