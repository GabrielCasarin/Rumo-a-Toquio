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


Q = Sequential()
Q.add(Dense(output_dim=40, input_dim=80))
Q.add(Activation("sigmoid"))
Q.add(Dense(output_dim=40))
Q.add(Activation("sigmoid"))
Q.add(Dense(output_dim=30))
Q.compile(loss='mean_squared_error', optimizer='SGD')

epsilon = 0.2
batch_size = 16
gamma = 0.9


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
