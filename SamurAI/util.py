import numpy as np
from .config import *

def distancia(x1,x2,y1,y2):
    d = abs(x1-x2)+abs(y1-y2)
    return d


def imax (npVect, budget, i):
	# Recebe vetor Q(s) (tamanho (1,30), budget(s) e 
	# Retorna max(a) de Q(s,a) considerando apenas os Q possiveis

	#Para isso basta considerar se o budget é maximo (logo, todos os Q sao possiveis)
	#ou budget nao é maximo e só 10 Qs sao possiveis

	mBudget = MAX_BUDGET

	#Verificando se o estado permite que escolham os 3 samurais

	if mBudget == budget:
		return np.max(npVect[0])
	else:
		#Verificando qual samurai pode jogar
		samurai = i//10
		return np.max(npVect[0][samurai*10 : 10 + samurai*10])