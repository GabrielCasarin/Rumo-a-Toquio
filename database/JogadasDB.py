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
        self.idJogo = len(self.jogos)
        self.jogos[self.idJogo] = IOBTree()
        self.jogoAtual = self.jogos[self.idJogo]

    def addState(self, state):
        # cria uma nova linha e colocar estado nela
        if len(self.jogoAtual) > 0:
            self.jogadaAnterior = self.jogadaAtual
        numJogada = len(self.jogoAtual)
        self.jogoAtual[numJogada] = OOBTree()
        self.jogadaAtual = self.jogoAtual[numJogada]
        # colocar estado
        self.jogadaAtual['estado'] = state.copy()

    def addAcao(self, acao):
        # colocar acao na linha atual
        self.jogadaAtual['acao'] = acao

    def addReward(self, reward):
        # colocar reward na linha anterior
        self.jogadaAnterior['reward'] = reward

    def ultima_acao(self):
        return self.jogadaAnterior['acao']

    def ultimo_estado(self):
        return self.jogadaAnterior['estado']

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
