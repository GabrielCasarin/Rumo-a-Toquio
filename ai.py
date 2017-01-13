##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################


import numpy as np
from keras.models import Sequential
from keras.layers import Input, Dense, Activation

from config import *


class AI:
	def __init__(self, G, player, treinar, camadas=[82, 40, 30]):
		super(AI, self).__init__()
		self.G = G
		self.player = player
		self.treinar = treinar

		# Rede Neural
		self.Q = Sequential()

		self.Q.add(Dense(output_dim=camadas[1], input_dim=camadas[0]))

		for i in range (1,len(camadas)-1):
			self.Q.add(Activation("sigmoid"))
			self.Q.add(Dense(output_dim=camadas[i+1]))

		self.Q.compile(loss='mean_squared_error', optimizer='SGD')

		self.Q.save('blablabla.h5')

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

		# print('turno:', turno)
		# print('samurais:', samurais)
		# print('tabuleiro:', tabuleiro)

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
			vectQ = self.Q.predict(estado.toVect())[0]

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

class Estado:
	def __init__(self, turno, samurais, tabuleiro, budget, player):
		self.turno = turno			#int 0 95
		self.samurais = samurais	#int de lista de lista (6x5)
		self.tabuleiro = tabuleiro  #int de lista de lista (sizexsize)
		self.budget = budget		#int 0 7
		self.player = player		#int 0 1

	def toVect(self):
		tam =  33 + len(self.tabuleiro)**2

		vect = np.ndarray((1,tam))
		k = 0

		vect[0][0] = self.turno
		k+= 1

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
	def copy(self, arg):
		pass
