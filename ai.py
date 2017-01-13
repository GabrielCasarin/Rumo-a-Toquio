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
		self.Q.add(Activation("sigmoid"))
		# self.Q.add(Dense(output_dim=40))
		# self.Q.add(Activation("sigmoid"))
		self.Q.add(Dense(output_dim=30))
		self.Q.compile(loss='mean_squared_error', optimizer='SGD')

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

		print('turno:', turno)
		print('samurais:', samurais)
		print('tabuleiro:', tabuleiro)

		budget = MAX_BUDGET

		self.estado = Estado(turno, samurais, tabuleiro, budget, self.player)

		print(self.estado.toVect())

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

		vect = np.ndarray(tam)
		k = 0

		vect[0] = self.turno
		k+= 1

		for i in range (len(self.samurais)):
			for j in range (5):
				vect[k] = self.samurais[i][j]
				k += 1

		for i in range (len(self.tabuleiro)):
			for j in range (len(self.tabuleiro)):
				vect[k] = self.tabuleiro[i][j]
				k += 1

		vect[k] = self.budget
		k += 1

		vect[k] = self.player

		return vect
