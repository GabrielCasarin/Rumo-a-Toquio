import os.path

import numpy as np
import random
import keras.models
from keras.models import Sequential
from keras.layers import Dense, Activation

from SamurAI.database.JogadasDB import JogadasDB
from SamurAI.config import *

def main(model='KARDAMEL'):
	#Recebe uma rede neural e o file_db
	#treina essa rede com os dados do file_db
	#guarda a rede antiga na pasta IAs
	#chama essa ia nova de "KARDAMEL"
	DIR = './Samurai/database/IAs/'
	Q = keras.models.load_model(DIR + model + '.h5')

	#salvar Q em outro lugar
	numModels = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and 'model' in name])
	Q.save(DIR+'model_'+str(numModels))
	
	#treinar rede Q
	# TODO
	
	#salvar Q no KARDAMEL.h5
	Q.save(DIR+'KARDAMEL.h5')
	
if __name__ == '__main__':
    main()
