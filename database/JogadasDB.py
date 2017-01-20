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
        self.estagioAtual = 'aceitaState'
        self.idJogo = len(self.jogos)
        self.jogos[self.idJogo] = IOBTree()
        self.jogoAtual = self.jogos[self.idJogo]
        self.jogoAtual[0] = OOBTree()
        self.jogadaAtual = self.jogoAtual[0]
        # default
        self.jogadaAtual['estado'] = None
        self.jogadaAtual['acao'] = None
        self.jogadaAtual['reward'] = None

        transaction.commit()

    def addAcao(self, acao):
        if self.estagioAtual == 'aceitaAcao':
            # proxima tuple
            # colocar acao
            self.estagioAtual = 'aceitaState'
            numJogada = len(self.jogoAtual)
            self.jogoAtual[numJogada] = OOBTree()
            self.jogadaAtual = self.jogoAtual[numJogada]
            self.jogadaAtual['acao'] = acao
            self.jogadaAtual['estado'] = None
            self.jogadaAtual['reward'] = None
            transaction.commit()
        else:
            self.estagioAtual = 'Error'

    def addState(self, state):
        if self.estagioAtual == 'aceitaState':
            # colocar estado
            self.estagioAtual = 'aceitaReward'
            self.jogadaAtual['estado'] = state.copy()
            # transaction.commit()
        else:
            self.estagioAtual = 'Error'

    def addReward(self, reward):
        if self.estagioAtual == 'aceitaReward':
            # colocar reward(estado, estado da linha de cima)
            self.estagioAtual = 'aceitaAcao'
            self.jogadaAtual['reward'] = reward
            # transaction.commit()
        else:
            self.estagioAtual = 'Error'

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
