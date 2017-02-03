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
#import persistent


class JogadasDB:

    def __init__(self, arq='historico_jogos.fs'):
        # TRADUCAO DAS VARIAVEIS PQ EU TO CONFUSO:

        # Todos os dados se referem a um unico jogador
        # 'historico_jogos' possui todas as partidas
        # 'partida' possui todas as rodadas
        # 'partida[self.numRodada]' é um dicionário da ultima jogada que possui (estado, acao, reward) de um unico jogador

        # id se refere ao numero da partida no historico_jogos
        # numRodada se refere ao numedo da partida[self.numRodada] da partida

        self.storage = FS.FileStorage(os.path.join('SamurAI', 'database','tmp', arq))  # armazena os dados fisicamente no arquivo .fs
        self.db = ZODB.DB(self.storage)  # encapsula o objeto de armazenamento (storage), além de prover o comportamento do DB
        self.conn = self.db.open()  # começa uma conexão com o DB a fim de podermos realizar transações
        self.dbroot = self.conn.root()  # o objeto root funciona como um namespace para todos os outros contêineres do DB

        if 'historico_jogos' not in self.dbroot.keys():
            self.dbroot['historico_jogos'] = IOBTree()
            transaction.commit()

        self.historico_jogos = self.dbroot['historico_jogos']

        self.JogoAberto = False

    def addJogo(self):
        # grava o estado inicial, inicialmente
        # cria um registro para o novo jogo
        self.id = len(self.historico_jogos)
        self.historico_jogos[self.id] = IOBTree()
        self.partida = self.historico_jogos[self.id]
        self.numRodada = 0

        self.JogoAberto = True

    def addState(self, state):
        # cria uma nova linha e colocar estado nela
        self.partida[self.numRodada] = OOBTree()
        # colocar estado
        self.partida[self.numRodada]['estado'] = state.copy()
        # print('    rodada', self.numRodada, ': adicionado', state.to_hash()[:8])

    def addAcao(self, acao):
        # colocar acao na linha atual
        self.partida[self.numRodada]['acao'] = acao
        # print('             : acao', acao)
        #adiciona-se 1 ao numRodada
        self.numRodada += 1

    def addReward(self, reward):
        # colocar reward na linha anterior
        self.partida[self.numRodada-1]['reward'] = reward

    def addRewardScore(self, reward):
        # colocar reward na linha atual
        self.partida[self.numRodada - 1]['reward'] = reward
        self.JogoAberto = False
        transaction.commit()

    def ultima_acao(self):
        return self.partida[self.numRodada-1]['acao']

    def ultimo_estado(self):
        if not self.JogoAberto:
            self.addJogo()

        if self.numRodada == 0:
            return None
        else:
            return self.partida[self.numRodada - 1]['estado']

    def close(self):
        self.conn.close()
        self.db.close()
        self.storage.close()

    def commit(self):
        transaction.commit()
