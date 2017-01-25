##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################


from SamurAI.gamemanager import *
from SamurAI.ai import AI


def main(num_jogos):
    # instancia a IA principal
    ai_principal = AI(player=0, model='model0.h5')

    # instancia a IA que servirá como oponente
    ai_openente = AI(player=1, model='model1.h5')

    # instancia um game manager
    game = Game()

    numPartidas = 1

    score0 = 0
    score1 = 0

    for _ in range(500):
        # manda o DB acrescentar um jogo aos seus registros
        ai_principal.jogosDB.addJogo()

        for partida in range (numPartidas):

            game.__init__()

            while game.turn < MAX_TURN:

                if partida == 0:
                    turno_player = game.turn%2 + 1
                elif partida == 1:
                    turno_player = 2-game.turn%2

                if turno_player == 1: #player_0
                    player = player0
                else:
                    player = player1

                if TOTALMENTE_OBSERVAVEL:
                    player.set_turn(game.view(-turno_player))
                else:
                    player.set_turn(game.view(turno_player))

                comando = player.get_comandos()

                if turno_player == 1:
                    msg1 = game.p1.order(comando)
                else:
                    msg2 = game.p2.order(comando)

                game.turn += 1
                if game.turn%6 == 0:
                    game.clearOrderStat()

                game.heal()

            score0 += game.score(1)
            score1 += game.score(2)

        print('\nSCORES:')
        print('Player1', score0)
        print('Player2', score1)

        player0.set_scores(score0, score1)


if __name__ == '__main__':
    argumento = sys.argv[1]
    main(argumento)
