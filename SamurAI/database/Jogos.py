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
import transaction
import persistent
from .Estados import EstadosManager


''' Todos os dados se referem a um unico jogador
    'historico_jogos' possui todas as partidas
    'partida' possui todas as rodadas
    'partida[self.numRodada]' é um dicionário da ultima jogada que possui (estado, acao, reward) de um unico jogador
    numRodada se refere ao numedo da partida[self.numRodada] da partida'''

class JogosManager:
    def __init__(self, historico_jogos):
        self.historico_jogos = historico_jogos

    def create(self):
        # cria um registro para o novo jogo
        new_pk = len(self.historico_jogos)
        nova_partida = Partida()
        self.historico_jogos[new_pk] = partida
        return partida
    
    def get(self, index):
        return self.historico_jogos[index]


class Partida(persistent.Persistent):
    objects = None # Manager
    def __init__(self):
        self.rodadas = IOBTree()
    
    @property
    def numRodadas(self):
        return len(self.rodadas)
    
    def save(self):
        transaction.commit()

    def addRodada(self):
        # cria uma nova linha
        self.rodadas[self.numRodadas] = OOBTree()

    def addState(self, numRodada, state):
        # colocar estado
        self.rodadas[numRodada]['estado'] = EstadosManager.get_or_create(s=state)
        # print('    rodada', self.numRodada, ': adicionado', state.to_hash()[:8])

    def addAcao(self, numRodada, acao):
        # colocar acao na linha atual
        self.rodadas[numRodada]['acao'] = acao
        # print('             : acao', acao)

    def addReward(self, numRodada, reward):
        # colocar reward na linha anterior
        self.rodadas[numRodada]['reward'] = reward

    def ultimaAcao(self):
        return self.rodadas[self.numRodadas - 1]['acao']

    def ultimoEstado(self):
        if self.numRodada == 0:
            return None
        else:
            return self.rodadas[self.numRodadas - 1]['estado']
