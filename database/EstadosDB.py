##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

import os

import hashlib

import numpy as np

from BTrees.OOBTree import OOBTree
from BTrees.IOBTree import IOBTree
import ZODB
import ZODB.FileStorage as FS
import transaction
import persistent


class EstadosDB:
    def __init__(self, arq='estados.fs'):
        self.storage = FS.FileStorage(os.path.join('database','tmp', arq))  # armazena os dados fisicamente no arquivo .fs
        self.db = ZODB.DB(self.storage)  # encapsula o objeto de armazenamento (storage), além de prover o comportamento do DB
        self.conn = self.db.open()  # começa uma conexão com o DB a fim de podermos realizar transações
        self.dbroot = self.conn.root()  # o objeto root funciona como um namespace para todos os outros contêineres do DB
        if 'estados' not in self.dbroot.keys():
            self.dbroot['estados'] = OOBTree()
        self.estados = self.dbroot['estados']

    def get_estado(self, turno, samurais, tabuleiro, budget, player):
        # calcula o hash
        string = str(turno)
        for i in range(len(samurais)):
            for j in range(5):
                string += str(samurais[i][j])
        for i in range(len(tabuleiro)):
            for j in range(len(tabuleiro)):
                string += str(tabuleiro[i][j])
        string += str(budget)
        string += str(player)

        h = hashlib.sha256(string.encode()).hexdigest()

        if h in self.estados.keys():
            return self.estados[h]
        else:
            novo_estado = Estado(turno, samurais, tabuleiro, budget, player)
            self.estados[h] = novo_estado
            transaction.commit()
            return novo_estado

    def encerrar(self):
        self.conn.close()
        self.db.close()
        self.storage.close()


class Estado(persistent.Persistent):
    def __init__(self, turno, samurais, tabuleiro, budget, player):
        self.turno = turno          # int 0 95
        self.samurais = samurais    # int de lista de lista (6x5)
        self.tabuleiro = tabuleiro  # int de lista de lista (size x size)
        self.budget = budget        # int 0 7
        self.player = player        # int 0 1
        self.qtd_visitas = 0        # para futuras implementacoes

    # GETTERS E SETTERS

    # Samurais
    @property
    def samurais(self):
        return self.__samurais

    @samurais.setter
    def samurais(self, s):
        self.__samurais = []
        for el in s:
            self.__samurais.append(list(el))
        self._p_changed = True

    # Tabuleiro
    @property
    def tabuleiro(self):
        return self.__tabuleiro

    @tabuleiro.setter
    def tabuleiro(self, s):
        self.__tabuleiro = []
        for el in s:
            self.__tabuleiro.append(list(el))
        self._p_changed = True

    # FIM GETTERS E SETTERS

    def to_hash(self):
        string = str(self.turno)
        for i in range(len(self.samurais)):
            for j in range(5):
                string += str(self.samurais[i][j])
        for i in range(len(self.tabuleiro)):
            for j in range(len(self.tabuleiro)):
                string += str(self.tabuleiro[i][j])
        string += str(self.budget)
        string += str(self.player)

        return hashlib.sha256(string.encode()).hexdigest()

    def to_vect(self):
        tam = 33 + len(self.tabuleiro)**2

        vect = np.ndarray((1, tam))
        k = 0

        vect[0][k] = self.turno
        k += 1

        for i in range(len(self.samurais)):
            for j in range(5):
                vect[0][k] = self.samurais[i][j]
                k += 1

        for i in range(len(self.tabuleiro)):
            for j in range(len(self.tabuleiro)):
                vect[0][k] = self.tabuleiro[i][j]
                k += 1

        vect[0][k] = self.budget
        k += 1

        vect[0][k] = self.player

        return vect

    def copy(self):
        novo_estado = Estado(
            turno=self.turno,
            samurais=self.samurais,
            tabuleiro=self.tabuleiro,
            budget=self.budget,
            player=self.player
        )
        return novo_estado

