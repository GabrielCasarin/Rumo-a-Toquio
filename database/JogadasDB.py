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

        linha = {'turno':'', 'acao':'', 'estado':'', 'reward':''}
        self.estagioAtual = 'aceitaAcao'
        # 'aceitaAcao', 'aceitaState', 'aceitaReward', 'Error'

        # proxima tuple
        acao = None
        # state = state
        reward = None

    def addJogo(self):
        self.idJogo = len(self.dbroot['jogos'])
        self.jogos[self.idJogo] = IOBTree()
        self.jogoAtual = self.jogos[self.idJogo]
        transaction.commit()

    def addAcao(self, acao):
        if self.estagioAtual == 'aceitaAcao':
            # proxima tuple
            # colocar acao
            self.estagioAtual = 'aceitaState'
            self.jogadaAtual['acao'] = acao
            transaction.commit()
        else:
            self.estagioAtual = 'Error'

    def addState(self, state):
        if self.estagioAtual == 'aceitaState':
            # colocar estado
            self.estagioAtual = 'aceitaReward'
            numJogada = len(self.jogoAtual)
            self.jogoAtual[numJogada] = OOBTree()
            self.jogadaAtual = self.jogoAtual[numJogada]
            self.jogadaAtual['estado'] = state
            self.jogadaAtual['acao'] = None
            self.jogadaAtual['reward'] = None
            transaction.commit()
        else:
            self.estagioAtual = 'Error'

    def addReward(self, reward):
        if self.estagioAtual == 'aceitaReward':
            # colocar reward(estado, estado da linha de cima)
            self.estagioAtual = 'aceitaAcao'
            self.jogadaAtual['reward'] = reward
            transaction.commit()
        else:
            self.estagioAtual = 'Error'
