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
        # cria um registro para o novo jogo
        self.id = len(self.jogos)
        self.jogos[self.id] = IOBTree()
        self.match = self.jogos[self.id]

    def addState(self, state):
        # cria uma nova linha e colocar estado nela
        print('ADICIONANDO UM ESTADO')
        if len(self.match) > 0:
            self.rodadaAnterior = self.rodadaAtual
        numJogada = len(self.match)
        self.match[numJogada] = OOBTree()
        self.rodadaAtual = self.match[numJogada]

        # colocar estado
        self.rodadaAtual['estado'] = state.copy()

        #transaction.commit()

    def addAcao(self, acao):
        # colocar acao na linha atual
        self.rodadaAtual['acao'] = acao
        #transaction.commit()

    def addReward(self, reward):
        # colocar reward na linha anterior
        self.rodadaAnterior['reward'] = reward
        #transaction.commit()

    def addRewardScore(self, reward):
        # colocar reward na linha atual
        self.rodadaAtual['reward'] = reward
        transaction.commit()

    def ultima_acao(self):
        return self.rodadaAnterior['acao']

    def ultimo_estado(self):
        if len(self.match) == 0:
            return None
        else:
            return self.rodadaAnterior['estado']

    def imprimir_jogo(self, id):
        for i in range(len(self.jogos[id])):
            rodada = self.jogos[id][i]
            print('Rodada', i)
            print('Acao:', rodada['acao'])
            print('Estado:')
            print(rodada['estado'])
            print('Reward:', rodada['reward'])
            print('\n\n')

    def close(self):
        self.conn.close()
        self.db.close()
        self.storage.close()

    def commit(self):
        transaction.commit()
