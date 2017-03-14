##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################
import hashlib
import numpy as np
from BTrees.OOBTree import OOBTree
from BTrees.IOBTree import IOBTree
import transaction
import persistent


class EstadosManager:
    def __init__(self, estados):
        self.estados = estados

    def get_or_create(self, **kwargs):
        if 's' in kwargs:
            new_state = kwargs['s']
        else:
            turno = kwargs['turno']
            samurais = kwargs['samurais']
            tabuleiro = kwargs['tabuleiro']
            budget = kwargs['budget']
            player = kwargs['player']
            new_state = Estado(turno, samurais, tabuleiro, budget, player)
    
        # calcula o hash
        h = new_state.to_hash()

        # verifica se o estado já se encontra no DB
        if h in self.estados.keys():
            s = self.estados[h]
        else:
            self.estados[h] = new_state
            s = new_state
        return s


class Estado(persistent.Persistent):
    objects = None # manager
    def __init__(self, turno, samurais, tabuleiro, budget, player, qtd_visitas=0):
        self.turno = int(turno)     # int 0 95
        self.samurais = samurais    # int de lista de lista (6x5)
        self.tabuleiro = tabuleiro  # int de lista de lista (size x size)
        self.budget = int(budget)   # int 0 7
        self.player = int(player)       # int 0 1
        self.qtd_visitas = qtd_visitas  # para futuras implementacoes

    @property
    def samurais(self):
        return self.__samurais

    @samurais.setter
    def samurais(self, s):
        self.__samurais = []
        for el in s:
            self.__samurais.append(list(el))
        self._p_changed = True

    @property
    def tabuleiro(self):
        return self.__tabuleiro

    @tabuleiro.setter
    def tabuleiro(self, s):
        self.__tabuleiro = []
        for el in s:
            self.__tabuleiro.append(list(el))
        self._p_changed = True

    def save(self):
        s = Estado.objects.get_or_create(s=self)
        s.qtd_visitas = self.qtd_visitas
        transaction.commit()

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
        new_state = Estado(turno=self.turno,
                           samurais=self.samurais,
                           tabuleiro=self.tabuleiro,
                           budget=self.budget,
                           player=self.player)
        return new_state

    def __str__(self):
        #string do turno
        sT = str(self.turno)

        #strin dos samurais
        sS = ''

        for samurai in self.samurais:
            sS += '\n'
            sS += str(samurai[0]) + ' '#x
            sS += str(samurai[1]) + ' '#y
            sS += str(samurai[2]) + ' '#orderstatus
            sS += str(samurai[3]) + ' '#showingstatus
            sS += str(samurai[4])       #treatmentturn


        #string do tabuleiro(Mapa)
        sM =''
        for y in range(len(self.tabuleiro)):
            sM += '\n'
            for x in range(len(self.tabuleiro)-1):
                sM += str(self.tabuleiro[y][x]) + ' '
            sM += str(self.tabuleiro[y][len(self.tabuleiro)-1])

        s = sT + sS + sM

        return s
