##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################


from SamurAI.gamemanager import *
from SamurAI.ai import AI
import sys
import time

def main(num_jogos, numPartidas=1, graphical=False):

    game = Game()

    KARDAMEL = AI(model='KARDAMEL', armazenar_dados=True)
    IA_ENEMY = AI(model='randomIA')

    t = time.time()

    for i in range (num_jogos):
        #print("Jogo: {}".format(i))
        
        score0 = 0
        score1 = 0

        for partida in range(numPartidas):
            #print("Partida: {}".format(partida))
            # manda o DB acrescentar um jogo aos seus registros
            #KARDAMEL.jogosDB.addJogo()

            game.__init__()

            while game.turn < MAX_TURN:

                if partida == 0:
                    turno_player = game.turn%2 + 1
                elif partida == 1:
                    turno_player = 2-game.turn%2

                if turno_player == 1:
                    IA = KARDAMEL
                else:
                    IA = IA_ENEMY

                if TOTALMENTE_OBSERVAVEL:
                    IA.set_turn(game.view(-turno_player), graphical=False)
                else:
                    IA.set_turn(game.view(turno_player), graphical=False)

                comando = IA.get_comandos()

                if turno_player == 1:
                    game.p1.order(comando)
                else:
                    game.p2.order(comando)

                game.turn += 1
                if game.turn%6 == 0:
                    game.clearOrderStat()

                game.heal()

            score0 += game.score(1)
            score1 += game.score(2)

        #print('Score: player0', score0)
        #print('SCore: player1', score1, '\n')

        KARDAMEL.set_scores(score0, score1)
        IA_ENEMY.set_scores(score0, score1)

    print('{}s em {}jogos'.format(time.time()-t,num_jogos))
    KARDAMEL.jogosDB.close()


if __name__ == '__main__':
    argumento = int(sys.argv[1])
    main(argumento)

