##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

import os
import hashlib

from BTrees.OOBTree import OOBTree
from BTrees.IOBTree import IOBTree
import ZODB
import ZODB.FileStorage as FS
import transaction
import persistent


class JogadasDB:

    def __init__(self, arq='Jogos.fs'):
        self.storage = FS.FileStorage(os.path.join('database','tmp', arq))  # armazena os dados fisicamente no arquivo .fs
        self.db = ZODB.DB(self.storage)  # encapsula o objeto de armazenamento (storage), além de prover o comportamento do DB
        self.conn = self.db.open()  # começa uma conexão com o DB a fim de podermos realizar transações
        self.dbroot = self.conn.root()  # o objeto root funciona como um namespace para todos os outros contêineres do DB

        if 'jogos' not in self.dbroot.keys():
            self.dbroot['jogos'] = IOBTree()
            transaction.commit()

        self.jogos = self.dbroot['jogos']

    def addJogo(self):
        # grava o estado inicial, inicialmente
        # self.estagioAtual = 'q0'
        # cria um registro para o novo jogo
        self.idJogo = len(self.jogos)
        self.jogos[self.idJogo] = IOBTree()
        self.jogoAtual = self.jogos[self.idJogo]
        self.jogoAtual[0] = OOBTree()
        self.jogadaAtual = self.jogoAtual[0]
        # # default
        # self.jogadaAtual['estado'] = None
        # self.jogadaAtual['acao'] = None
        # self.jogadaAtual['reward'] = None

    def addAcao(self, acao):
        # if self.estagioAtual == 'q1':
            # colocar acao
            # self.estagioAtual = 'q2'
            numJogada = len(self.jogoAtual)
            self.jogadaAtual['acao'] = acao
            self.jogadaAnterior = self.jogadaAtual
            self.jogoAtual[numJogada] = OOBTree()
            self.jogadaAtual = self.jogoAtual[numJogada]
            self.jogadaAtual['estado'] = None
        # else:
            # self.estagioAtual = 'Error'

    def addState(self, state):
        # if self.estagioAtual == 'q0':
            # colocar estado
            # self.estagioAtual = 'q1'
            self.jogadaAtual['estado'] = state.copy()
        # elif self.estagioAtual == 'q2':
            # self.estagioAtual = 'q3'
            self.jogadaAtual['estado'] = state.copy()
        else:
            # self.estagioAtual = 'Error'

    def addReward(self, reward):
        # if self.estagioAtual == 'q3':
            # colocar reward(estado, estado da linha de cima)
            # self.estagioAtual = 'q1'
            self.jogadaAnterior['reward'] = reward
        # else:
            # self.estagioAtual = 'Error'

    def ultimoState(self):
        if len(self.jogoAtual) == 1:
            return None
        else:
            jogadaAnterior = len(self.jogoAtual) - 2
            self.jogoAtual[jogadaAnterior]['estado']

    def imprimir_jogo(self, idJogo):
        for i in range(len(self.jogos[idJogo])):
            jogada = self.jogos[idJogo][i]
            print('Jogada', i)
            print('Acao:', jogada['acao'])
            print('Estado:')
            print(jogada['estado'])
            print('Reward:', jogada['reward'])
            print()

    def close(self):
        self.conn.close()
        self.db.close()
        self.storage.close()

    def commit(self):
        transaction.commit()
