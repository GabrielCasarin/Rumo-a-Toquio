import itertools
import os.path

import numpy as np
import random
import keras.models
from keras.models import Sequential
from keras.layers import Dense, Activation

from SamurAI.database.JogadasDB import JogadasDB
from SamurAI.database.IAs.RN_Manager import RN_Manager
from SamurAI.config import *
from SamurAI.util import imax


nb_epochs = 50
batch_size = 16
gamma = 0.9


def main(model='KARDAMEL'):
    #Recebe uma rede neural e o file_db
    #treina essa rede com os dados do file_db
    #guarda a rede antiga na pasta IAs
    #chama essa ia nova de "KARDAMEL"
    DIR = os.path.join('.', 'SamurAI', 'database', 'IAs')
    Q = keras.models.load_model(os.path.join(DIR, model + '.h5'))

    j = JogadasDB()

    #salvar Q em outro lugar
    # numModels = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and 'model' in name])
    indice = RN_Manager.proximo_indice()
    rn_nome = 'model_{}.h5'.format(indice)
    Q.save(os.path.join(DIR, rn_nome))
    RN_Manager.registrar(rn_nome)
    
    #treinar rede Q
    inputs = np.zeros((batch_size, Q.input_shape[1]))
    targets = np.zeros((batch_size, Q.output_shape[1]))

    for _ in range(nb_epochs):
        # montar minibatch
        tuplas_random = []
        for i in range(len(j.historico_jogos)):
            tuplas_random += list(itertools.product([i], range(len(j.historico_jogos[i]))))
        np.random.shuffle(tuplas_random)

        tuplas_random = tuplas_random[0:batch_size*(len(tuplas_random)//batch_size)]

        while tuplas_random:
            minibatch = tuplas_random[0:batch_size]
            tuplas_random = tuplas_random[batch_size:]

            for i in range(batch_size):
                iJogo, iJogada = minibatch[i]

                # print(iJogo, iJogada)

                s = j.historico_jogos[iJogo][iJogada]['estado']
                if iJogada == len(j.historico_jogos[iJogo][iJogada]) - 1:
                    sLinha = j.historico_jogos[iJogo][iJogada + 1]['estado']
                else:
                    sLinha = None
                acao = j.historico_jogos[iJogo][iJogada]['acao']
                r = j.historico_jogos[iJogo][iJogada]['reward']

                budget = s.budget
                s = s.to_vect()
                inputs[i] = s
                targets[i] = Q.predict(s)

                if sLinha is not None:
                    targets[i][acao] = r + gamma*imax(Q.predict(sLinha.to_vect()), budget, acao)
                else:
                    targets[i][acao] = r


            Q.train_on_batch(inputs, targets)

    
    #salvar Q no KARDAMEL.h5
    Q.save(os.path.join(DIR, 'KARDAMEL.h5'))
    j.close()
    
if __name__ == '__main__':
    main()
