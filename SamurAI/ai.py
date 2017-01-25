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

from .database.JogadasDB import JogadasDB
from .database.EstadosDB import Estado
from .simulador import Simulador
from .config import *
from .interface import gui_ia as gui


randomizar = True


class AI:
    def __init__(self, player, em_treinamento=False, camadas=[82, 40, 30], **kwargs):

        # inicializa a AI:

        # possui os atributos:

        #   player (0 ou 1)
        #   em_treinamento (True or False)

        #   Q   (rede neural s->Q)
        #   epsilon (parametro para a politica epsilon greed)

        #   jogosDB (ponteiro para o BD de jogosDB)
        #   simulador (ponteiro para o simulador)

        #   estado_anterior
        #   estado

        super(AI, self).__init__()
        self.player = player    # 0 ou 1 ~~ para indicar quem voce eh
        # self.em_treinamento = em_treinamento  # boolean

        # Rede Neural
        if 'model' in kwargs:
            nome_arq = kwargs['model']
        else:
            nome_arq = 'model%d.h5'%player

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

        self.epsilon = 0.2

        if self.player == 0:
            self.jogosDB = JogadasDB()
            # if not self.em_treinamento:
                # self.jogosDB.addJogo()

        self.simulador = Simulador()

        self.estado = None
        self.estadoLinha = None

    def set_turn(self, msg):
        # recebe um turno no protocolo oficial de texto
        # mostra o turno numa gui
        # atualiza estado

        gui.cliente(msg)

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
        #inicializa as variaveis a serem usadas
        listaAcao = []
        acao = -1
        sam = -1

        s = None
        if self.player == 0:
            s = self.jogosDB.ultimo_estado()
        sLinha = self.estado
        print('s:', s)

        while acao != 0 and sLinha.budget >= 0:

            #se está no loop, é porque está em um estado jogável
            #logo:
            #hora de armazenar estado
            if self.player == 0:
                self.jogosDB.addState(sLinha)

            #s, acao, s' -> R
            if s != None:
                print('ooooooi')
                print(s)
                r = self.reward(s,acao,sLinha)
                
                #com exceção do loop da primeira rodada, deve-se armazenar todos os rewards
                #hora de armazenar reward
                if self.player == 0:
                    self.jogosDB.addReward(r)
                        
            s = sLinha.copy()
            #s -> acao
            
            vectQ = self.Q.predict(self.estado.to_vect())[0]
            if not listaAcao:
                i = np.argmax(vectQ)
                sam = i // 10
                listaAcao.append(str(sam))
            else:
                vectQ = vectQ[10 * sam:10 * sam + 10]
                i = np.argmax(vectQ)
            acao = i % 10
            listaAcao.append(str(acao))

            #toda acao decidida deve ser armazenada
            #logo:
            #hora de armazenar acao
            if self.player == 0:
                self.jogosDB.addAcao(i)


            #s, acao -> sSim

            self.simulador.estado = s.copy()
            self.simulador.atuar(sam,acao)
            sSim = self.simulador.estado

            sLinha = sSim


        print(listaAcao)

        return ' '.join(listaAcao)

    def reward(self, s, a, sL):
        #depende da acao  TODO
        rAcao = -0.1    # (1) reward Acao
        #rAcaoInv = -5   # (2) reward Acao Invalida
        rAcao0 = +0.8   #(tmp2) reward por finalizar acao com 0

        #depende do estado
        rEuCqN  = +1    # (3) reward Eu         Conquistar  Neutro
        rEuCqI  = +2    # (4) reward Eu         Conquistar  Inimigo
        rICqN   = -1    # (5) reward Inimigo    Conquistar  Neutro
        rICqEu  = -2    # (6) reward Inimigo    Conquistar  Eu
        rTII    = +3    # (7) reward turnos     Inimigo     Injuried
        rTEuI   = -3    # (8) reward turnos     Eu          Injuried

        
        reward = rAcao #(1)
        
        # if False: # (2)
        #     reward += rAcaoInv

        if False: # (tmp2)
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

        for i in range(len(sL.samurais)):
            for j in range(3):
                reward += rTII  #(7)
            for j in range(3,5):
                reward += rTEuI #(8)

        return reward

    def set_scores(self, scoreEu, scoreInim):
        if self.player == 0:
            self.jogosDB.estagioAtual = 'aceitaReward' # xD
            self.jogosDB.addRewardScore(10*(scoreEu - scoreInim))
            self.jogosDB.commit()
            self.jogosDB.close()


    def treinar(self):
        batch_size = 16
        gamma = 1


        indices_jogos = np.random.randint(len(self.jogosDB.jogos), size=batch_size)
        print(indices_jogos)
        print()
                
        inputs = np.zeros((batch_size, self.Q.input_shape[1]))
        targets = np.zeros((batch_size, self.Q.output_shape[1]))

        for i in range(batch_size):
            iJogo = int(indices_jogos[i])
            iJogada = np.random.randint(1, len(self.jogosDB.jogos[iJogo]))
            # print('iJogo', iJogo)
            # print('iJogada', iJogada)
            # print()

            s = self.jogosDB.jogos[iJogo][iJogada - 1]['estado']
            s_next = self.jogosDB.jogos[iJogo][iJogada]['estado']
            acao = self.jogosDB.jogos[iJogo][iJogada]['acao']
            r = self.jogosDB.jogos[iJogo][iJogada]['reward']

            budget = s.budget
            s = s.to_vect()
            inputs[i] = s
            targets[i] = self.Q.predict(s)
            # print(targets)

            if s_next is not None:
                targets[i][acao] = r + gamma*imax(self.Q.predict(s_next.to_vect()), budget)
            else:
                targets[i][acao] = r

        # treina o batch
        self.Q.train_on_batch(inputs, targets)

        self.jogosDB.close()


# if __name__ == '__main__':
#     a = AI(player=0, em_treinamento=True)
#     a.treinar()
