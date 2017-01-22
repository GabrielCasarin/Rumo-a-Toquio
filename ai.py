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

randomizar = True


class AI:
    def __init__(self, player, em_treinamento=False, camadas=[82, 40, 30]):
        super(AI, self).__init__()
        self.player = player    # 0 ou 1 ~~ para indicar quem voce eh
        self.em_treinamento = em_treinamento  # boolean

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

        self.epsilon = 0.2

        if self.player == 0:
            self.jogosDB = JogadasDB()
            if not self.em_treinamento:
                self.jogosDB.addJogo()

        self.simulador = Simulador()

        self.estado_anterior = None
        self.estado = None

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

        #s -> a
        #s, a -> s'
        #s, a, s' -> R

        listaAcao = []
        acao = -1
        sam = -1

        self.simulador.estado = self.estado

        while self.estado.budget >= 0 and acao != 0:
            if self.player == 0: # se é a IA sendo treinada
                self.jogosDB.addState(self.estado)
                if self.estado_anterior is not None:
                    r = self.reward(self.estado, self.jogosDB.ultima_acao(), self.estado_anterior)
                    self.jogosDB.addReward(r)
                print('armazenamento budget: ', self.estado.budget)

            vectQ = self.Q.predict(self.estado.to_vect())[0]

            if not listaAcao:
                i = np.argmax(vectQ)
                sam = i // 10
                listaAcao.append(str(sam))
            else:
                vectQ = vectQ[10 * sam:10 * sam + 10]
                i = np.argmax(vectQ)
            acao = i % 10

            if self.player == 0:
                self.jogosDB.addAcao(i)

            listaAcao.append(str(acao))

            self.simulador.atuar(sam, acao)
            self.estado_anterior = self.estado
            self.estado = self.simulador.estado

        print(listaAcao)

        return ' '.join(listaAcao)

    def reward(self, s, a, sL):

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

        return self.i

    def set_scores(self, scoreEu, scoreInim):
        self.jogosDB.estagioAtual = 'aceitaReward' # xD
        self.jogosDB.addReward(10*(scoreEu - scoreInim))
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
