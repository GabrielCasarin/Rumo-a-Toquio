##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

import os.path

import numpy as np
import keras.models
from keras.models import Sequential
from keras.layers import Dense, Activation

from database.JogadasDB import JogadasDB
from database.EstadosDB import Estado
from simulador import Simulador

from config import *

randomizar = False

class AI:
    def __init__(self, player, treinar, camadas=[82, 40, 30]):
        super(AI, self).__init__()
        self.player = player    # 0 ou 1 ~~ para indicar quem voce eh
        self.treinar = treinar  # boolean

        # Rede Neural
        nome_arq = 'model{}.h5'.format(self.player)

        if os.path.isfile(nome_arq) and not randomizar:
            self.Q = keras.models.load_model(nome_arq)
        else:
            self.Q = Sequential()
            self.Q.add(Dense(output_dim=camadas[1], input_dim=camadas[0]))
            for i in range(1, len(camadas) - 1):
                self.Q.add(Activation("sigmoid"))
                self.Q.add(Dense(output_dim=camadas[i + 1]))
            self.Q.compile(loss='mean_squared_error', optimizer='SGD')
            # salva o modelo para próximas partidas
            self.Q.save(nome_arq)

        # self.epsilon = 0.2
        # self.batch_size = 16

        if self.treinar:
            self.jogosDB = JogadasDB()
            self.jogosDB.addJogo()

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

        self.estado = Estado(
            turno, samurais, tabuleiro, MAX_BUDGET, self.player)

    def get_comandos(self):

        listaAcao = []
        acao = -1
        sam = -1
        estado = self.estado
        self.simulador.estado = estado

        while estado.budget >= 0 and acao != 0:

            if self.treinar:
                sAntes = self.jogosDB.ultimoState()
                self.jogosDB.addState(estado)
                print('armazenamento budget: ', estado.budget)
                #r = self.reward() # R(s')
                r = 1 # temp
                #print(estado)
                #print('r:', r)
                self.jogosDB.addReward(r)

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
                self.jogosDB.addAcao(i)

            listaAcao.append(str(acao))

            self.simulador.atuar(sam, acao)
            estado = self.simulador.estado

        print(listaAcao)

        return ' '.join(listaAcao)

    def reward(self):
        s = self.estado

        #depende da acao  TODO
        rAcao = -0.1    # (1) reward Acao
        rAcaoInv = -5   # (2) reward Acao Invalida

        #depende do estado
        rEuCqN  = +1    # (3) reward Eu         Conquistar  Neutro
        rEuCqI  = +2    # (4) reward Eu         Conquistar  Inimigo
        rICqN   = -1    # (5) reward Inimigo    Conquistar  Neutro
        rICqEu  = -2    # (6) reward Inimigo    Conquistar  Eu
        rEuKI = +10     # (7) reward Eu         kill        Inimigo
        rIKEu = -10     # (8) reward Inimigo    kill        Eu

        reward = 0
        # if False: # (1)
        #     reward += rAcao
        # if False: # (2)
        #     reward += rAcaoInv
        # if False: # (3)
        #     #for area eu conquista neutra
        #     reward += rEuCqN
        # if False: # (4)
        #     #for area eu conquista inimigo
        #     reward += rEuCqI
        # if False: # (5)
        #     #for area ininigo conquista neutro
        #     reward += rICqN
        # if False: # (6)
        #     #for area inimigo conquista eu
        #     reward += rICqEu
        # if False: # (7)
        # # if is enemy.sam in sNovo.samurais injuried and sVelho.samurai not injuried
        #     reward += rIKEu
        # if False: # (8)
        # # if is meu.sam in sNovo.samurais injuried and sVelho.samurai not injuried
        #     reward += rEuKI

        return 1

    def set_scores(self, scoreEu, scoreInim):
        self.jogosDB.estagioAtual = 'aceitaReward' # xD
        self.jogosDB.addReward(10*(scoreEu - scoreInim))
        import transaction
        transaction.commit()
