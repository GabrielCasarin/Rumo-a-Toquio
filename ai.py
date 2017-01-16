##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################


import hashlib

import numpy as np
from keras.models import Sequential
from keras.layers import Input, Dense, Activation

from BTrees.OOBTree import OOBTree
import ZODB
import ZODB.FileStorage as FS
import transaction
import persistent

from config import *


class AI:
	def __init__(self, player, treinar, camadas=[82, 40, 30]):
		super(AI, self).__init__()
		self.player = player
		self.treinar = treinar

		# Rede Neural
		self.Q = Sequential()

		self.Q.add(Dense(output_dim=camadas[1], input_dim=camadas[0]))

		for i in range (1,len(camadas)-1):
			self.Q.add(Activation("sigmoid"))
			self.Q.add(Dense(output_dim=camadas[i+1]))

		self.Q.compile(loss='mean_squared_error', optimizer='SGD')

		self.Q.save('model{}.h5'.format(self.player))

		self.epsilon = 0.2
		self.batch_size = 16

	def set_turn(self, msg):
		msg = msg.split('\n')

		turno = int(msg[0])

		samurais = [x.split() for x in msg[1:7]]

		for i in range(len(samurais)):
			for j in range(5):
				samurais[i][j] = int(samurais[i][j])

		tabuleiro = [x.split() for x in msg[7:]]
		for i in range(len(tabuleiro)):
			for j in range(len(tabuleiro)):
				tabuleiro[i][j] = int(tabuleiro[i][j])

		budget = MAX_BUDGET

		self.estado = Estado(turno, samurais, tabuleiro, budget, self.player)

	def armazena(self):
		# estado = self.estado
		# listaAcao = self.listaAcao

		#if estourou o espaço de armazenamento
			#treinar


		pass

	def reward(self,estado, estadoLinha, acao):
		#punicao:
		#nao terminar a jogada com 0
		#jogada invalida
		#punicao leve por acao para ele nao fazer jogadas e desfazer em seguida


		pass

	def jogar(self):

		listaAcao = []
		acao = -1
		budget = self.estado.budget
		sam = -1


		estado = self.estado
		#estado = self.estado.copy()  #TODO IMPORTANTE

		while budget > 0 and acao != 0:
			vectQ = self.Q.predict(estado.to_vect())[0]

			if not listaAcao:
				#V = np.max(vectQ)
				i = np.argmax(vectQ)
				sam = i//10
				listaAcao.append(str(sam))
			else:
				vectQ = vectQ[10*sam:10*sam+10]
				#V = np.max(vectQ)
				i = np.argmax(vectQ)
			acao = i%10
			listaAcao.append(str(acao))
			if 1 <= acao <= 4:
				budget -= 4
			elif 5 <= acao <= 8:
				budget -= 2
			elif acao == 9:
				budget -= 1

			# estado.simulate(sam, acao)

		# armazenar o estado e as acoes

		if self.estado.turno%2 == 0:
			print(i)
			print(listaAcao)
		self.listaAcao = listaAcao
		#self.armazenar()

	def get_comandos(self):
		self.jogar()
		return ' '.join(self.listaAcao)

	def armazenar(self):
		pass


def search(game):
	pass

def simulate(state):
	pass

def rollout(state):
	pass

def select(node):
	pass

def update(node, action, payoff):
	pass


class Estado(persistent.Persistent):

	def __init__(self, turno, samurais, tabuleiro, budget, player):
		self.turno = turno			#int 0 95
		self.samurais = samurais	#int de lista de lista (6x5)
		self.tabuleiro = tabuleiro  #int de lista de lista (size x size)
		self.budget = budget		#int 0 7
		self.player = player		#int 0 1
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
		for i in range (len(self.samurais)):
			for j in range (5):
				string += str(self.samurais[i][j])
		for i in range (len(self.tabuleiro)):
			for j in range (len(self.tabuleiro)):
				string += str(self.tabuleiro[i][j])
		string += str(self.budget)
		string += str(self.player)

		return hashlib.sha256(string.encode()).hexdigest()

	def to_vect(self):
		tam = 33 + len(self.tabuleiro)**2

		vect = np.ndarray((1,tam))
		k = 0

		vect[0][k] = self.turno
		k += 1

		for i in range (len(self.samurais)):
			for j in range (5):
				vect[0][k] = self.samurais[i][j]
				k += 1

		for i in range (len(self.tabuleiro)):
			for j in range (len(self.tabuleiro)):
				vect[0][k] = self.tabuleiro[i][j]
				k += 1

		vect[0][k] = self.budget
		k += 1

		vect[0][k] = self.player

		return vect

	#TODO
	def copy(self):
		novo_estado = Estado(
			turno=self.turno,
			samurais=self.samurais,
			tabuleiro=self.tabuleiro,
			budget=self.budget,
			player=self.player
		)
		return novo_estado

class EstadosDB:
	def __init__(self, arq='estados.fs'):
		self.storage = ZODB.FileStorage.FileStorage(arq)  # armazena os dados fisicamente no arquivo .fs
		self.db = ZODB.DB(storage)  # encapsula o objeto de armazenamento (storage), além de prover o comportamento do DB
		self.conn = db.open()  # começa uma conexão com o DB a fim de podermos realizar transações
		self.dbroot = conn.root()  # o objeto root funciona como um namespace para todos os outros contêineres do DB
		if 'estados' not in self.dbroot.keys():
			self.dbroot['estados'] = OOBTree()
		self.estados = self.dbroot['estados']

	def get_estado(self, turno, samurais, tabuleiro, budget, player):
		# calcula o hash
		string = str(turno)
		for i in range (len(samurais)):
			for j in range (5):
				string += str(samurais[i][j])
		for i in range (len(tabuleiro)):
			for j in range (len(tabuleiro)):
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

	def close():
		self.conn.close()
		self.db.close()
		self.storage.close()
