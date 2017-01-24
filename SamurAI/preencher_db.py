
from SamurAI.gamemanager import *
from SamurAI.ai import AI


def main_ia():

    game = Game()

    IA_0 = AI(player=0)
    IA_1 = AI(player=1)

    score0 = 0
    score1 = 0

    for partida in range(1):

        game.__init__()

        while game.turn < MAX_TURN:

            print('~~~~TURNO:  ', game.turn)

            if partida == 0:
                turno_player = game.turn%2 + 1
            elif partida == 1:
                turno_player = 2-game.turn%2

            if turno_player == 1: #IA_1
                IA = IA_0
            else:
                IA = IA_1

            if TOTALMENTE_OBSERVAVEL:
                IA.set_turn(game.view(-turno_player))
            else:
                IA.set_turn(game.view(turno_player))

            comando = IA.get_comandos()

            if turno_player == 1:
                game.p1.order(comando)
            else:
                game.p2.order(comando)

            print('\n' + game.view(-1) + '\n')

            game.turn += 1
            if game.turn%6 == 0:
                game.clearOrderStat()

            game.heal()

        score0 += game.score(1)
        score1 += game.score(2)

    print('\nSCORES:')
    print('Player0', score0)
    print('Player1', score1)

    IA_0.set_scores(score0, score1)
    IA_1.set_scores(score0, score1)

