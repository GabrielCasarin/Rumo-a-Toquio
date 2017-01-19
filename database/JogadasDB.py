##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################


import hashlib

from BTrees.OOBTree import OOBTree
from BTrees.IOBTree import IOBTree
import ZODB
import ZODB.FileStorage as FS
import transaction
import persistent


class JogadasDB:

    def __init__(self, arq='Jogos.fs'):
        self.storage = FS.FileStorage(arq)  # armazena os dados fisicamente no arquivo .fs
        self.db = ZODB.DB(self.storage)  # encapsula o objeto de armazenamento (storage), além de prover o comportamento do DB
        self.conn = self.db.open()  # começa uma conexão com o DB a fim de podermos realizar transações
        self.dbroot = self.conn.root()  # o objeto root funciona como um namespace para todos os outros contêineres do DB
        if 'jogadas' not in self.dbroot.keys():
            self.dbroot['jogadas'] = IOBTree()
        self.jogadas = self.dbroot['jogadas']

        linha = {'turno':'', 'acao':'', 'estado':'', 'reward':''}
        self.estagioAtual = 'aceitaAcao'
        # 'aceitaAcao', 'aceitaState', 'aceitaReward', 'Error'

        # proxima tuple
        acao = None
        # state = state
        reward = None

    def addAcao(self,acao):
        if self.estagioAtual == 'aceitaAcao':
            # proxima tuple
            # colocar acao
            self.estagioAtual = 'aceitaState'
        else:
            self.estagioAtual = 'Error'
    def addState(self,state):
        if self.estagioAtual == 'aceitaState':
            # colocar estado
            self.estagioAtual = 'aceitaReward'
        else:
            self.estagioAtual = 'Error'

    def addReward(self,reward):
        if self.estagioAtual == 'aceitaReward':
            # colocar reward(estado, estado da linha de cima)
            self.estagioAtual = 'aceitaAcao'
        else:
            self.estagioAtual = 'Error'
