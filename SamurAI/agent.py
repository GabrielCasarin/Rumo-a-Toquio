##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

import os.path

import numpy as np
import random
import keras.models
from keras.models import Sequential
from keras.layers import Dense, Activation

from .database.JogadasDB import JogadasDB
from .database.EstadosDB import Estado
from .simulador import Simulador
from .config import *


class AI:
    def __init__(self, em_treinamento=False, camadas=[82, 40, 30], **kwargs):
        # inicializa a AI:

        # possui os atributos:

        #   armazenar_dados (True or False)
        #   em_treinamento (True or False)

        #   Q   (rede neural s->Q)
        #   epsilon (parametro para a politica epsilon greed)

        #   jogosDB (ponteiro para o BD de jogosDB)
        #   simulador (ponteiro para o simulador)

        #   estado_anterior
        #   estado

        super(AI, self).__init__()

        if 'armazenar_dados' in kwargs:
            self.armazenar_dados = kwargs['armazenar_dados']
        else:
            self.armazenar_dados = False

        # Rede Neural
        if 'model' in kwargs:
            nome_arq = kwargs['model']+'.h5'
        else:
            nome_arq = 'newRandom.h5'

        DIR = os.path.join('.', 'SamurAI', 'database', 'IAs')

        if nome_arq == 'randomIA.h5':
            numModels = len([name for name in os.listdir(DIR) if (
                os.path.isfile(os.path.join(DIR, name)) and 'model' in name)])
            if numModels > 0:
                nome_arq = 'model_' + str(np.random.randint(numModels)) + '.h5'
            else:
                nome_arq = 'model_0.h5'
            print('Oponente: IA', nome_arq)

        # if nome_arq == 'newRandom.h5':
        #     #CRIANDO UMA REDE NOVA QUE NAO SERÁ SALVA:
        #     self.Q = Sequential()
        #     self.Q.add(Dense(output_dim=camadas[1], input_dim=camadas[0]))
        #     for i in range(1, len(camadas) - 1):
        #         self.Q.add(Activation("sigmoid"))
        #         self.Q.add(Dense(output_dim=camadas[i + 1]))
        #     self.Q.compile(loss='mean_squared_error', optimizer='SGD')


        if os.path.isfile(os.path.join(DIR, nome_arq)) and nome_arq != 'newRandom.h5':
            self.Q = keras.models.load_model(os.path.join(DIR, nome_arq))
        else:
            #CRIANDO UMA REDE NOVA:
            self.Q = Sequential()
            self.Q.add(Dense(output_dim=camadas[1], input_dim=camadas[0]))
            for i in range(1, len(camadas) - 1):
                self.Q.add(Activation("sigmoid"))
                self.Q.add(Dense(output_dim=camadas[i + 1]))
            self.Q.compile(loss='mean_squared_error', optimizer='SGD')

            # SALVANDO O MODELO COM NOME DEFINIDO
            self.Q.save(os.path.join(DIR, nome_arq))

        if kwargs['model'] == 'KARDAMEL':
            self.epsilon = 0.2
        else:
            self.epsilon = 0

        if self.armazenar_dados:
            self.jogosDB = JogadasDB()

        self.simulador = Simulador()

        self.estado = None
        self.estadoLinha = None

    def set_turn(self, msg, graphical=True):
        # recebe um turno no protocolo oficial de texto
        # mostra o turno numa gui
        # atualiza estado

        # if graphical:
        #     gui.cliente(msg)

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

        player = turno%2

        self.estado = Estado(turno, samurais, tabuleiro, MAX_BUDGET, player)

    def get_comandos(self):\
        #inicializa as variaveis a serem usadas
        listaAcao = []
        acao = -1
        sam = -1

        sAntes = None
        if self.armazenar_dados:
            sAntes = self.jogosDB.ultimo_estado()
        sAgora = self.estado

        while acao != 0 and sAgora.budget >= 0:
            #se está no loop, é porque está em um estado jogável
            #logo:
            #hora de armazenar estado
            if self.armazenar_dados:
                self.jogosDB.addState(sAgora)

                #s, acao, s' -> R
                if sAntes is not None:
                    #com exceção do loop da primeira rodada, deve-se armazenar todos os rewards
                    #hora de armazenar reward
                    if self.armazenar_dados:
                        r = self.reward(sAntes, self.jogosDB.ultima_acao(), sAgora)
                        self.jogosDB.addReward(r)

            sAntes = sAgora.copy()
            #s -> acao

            vectQ = self.Q.predict(self.estado.to_vect())[0]
            e = np.random.uniform()
            # e = 0

            if not listaAcao:
                if e < self.epsilon:
                    i = np.random.randint(30)
                else:
                    i = np.argmax(vectQ)
                sam = i // 10
                listaAcao.append(str(sam))
                acao = i % 10
            else:
                if e < self.epsilon:
                    acao = np.random.randint(10)
                else:
                    low_action_limit = 10*sam
                    high_action_limit = low_action_limit + 10
                    vectQ = vectQ[low_action_limit:high_action_limit]
                    acao = np.argmax(vectQ)

            listaAcao.append(str(acao))

            #toda acao decidida deve ser armazenada
            #logo:
            #hora de armazenar acao
            if self.armazenar_dados:
                self.jogosDB.addAcao(10*sam + acao)


            #s, acao -> sSim
            self.simulador.estado = sAgora.copy()
            self.simulador.atuar(sam, acao)
            sSim = self.simulador.estado

            sAgora = sSim

        #print(listaAcao)
        # if self.armazenar_dados:
        #     print()

        return ' '.join(listaAcao)

    def reward(self, s, a, sL):
        #depende da acao
        rAcao = 0       # (1) reward Acao
        rAcaoInv = -5   # (2) reward Acao Invalida
        rAcao0 = +0.8   # (2 tmp) reward Acao 0

        #depende do estado
        rEuCqN  = +1    # (3) reward Eu         Conquistar  Neutro
        rEuCqI  = +2    # (4) reward Eu         Conquistar  Inimigo
        rICqN   = -1    # (5) reward Inimigo    Conquistar  Neutro
        rICqEu  = -2    # (6) reward Inimigo    Conquistar  Eu
        rTII    = +30   # (7) reward turnos     Inimigo     Injuried
        rTEuI   = -30   # (8) reward turnos     Eu          Injuried


        reward = rAcao #(1)

        if (a%10 == 10): # (2 tmp)
            reward += rAcao0

        for x in range(SIZE):
            for y in range(SIZE):
                if s.tabuleiro[y][x] in [8] and sL.tabuleiro[y][x] in [0,1,2]: #(3)
                    reward += rEuCqN
                if s.tabuleiro[y][x] in [3,4,5] and sL.tabuleiro[y][x] in [0,1,2]: #(4)
                    reward += rEuCqI
                if s.tabuleiro[y][x] in [8] and sL.tabuleiro[y][x] in [3,4,5]: #(5)
                    reward += rICqN
                if s.tabuleiro[y][x] in [0,1,2] and sL.tabuleiro[y][x] in [3,4,5]: #(6)
                    reward += rICqEu

        for sam in range(0,3):
            if sL.samurais[sam][4]>16:
                reward += rTII  #(7)
        for sam in range(3,6):
            if sL.samurais[sam][4]>16:
                reward += rTEuI #(8)

        return 0

    def set_scores(self, scoreEu, scoreInim):
        if self.armazenar_dados:
            self.jogosDB.addRewardScore(scoreEu)
