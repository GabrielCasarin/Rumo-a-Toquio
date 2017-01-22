from gamemanager import *


def main_human():

    #FUNCAO A IMPLEMENTAR:
    #PASSAR msg PARA O CLIENT PARA ELE IMPRIMIR NA TELA DO JOGADOR
    #usar o final do protocolo

    score1 = 0
    score2 = 0
    msg1 = 'Bom Jogo!'
    msg2 = 'Bom Jogo!'

    server = Server()
    server.aguardar_jogadores()

    game = Game()

    for partida in range (2):

        game.__init__()

        while game.turn < MAX_TURN:


            if partida == 0:
                turno_player = game.turn%2 + 1
            elif partida == 1:
                turno_player = 2-game.turn%2

            if TOTALMENTE_OBSERVAVEL:
                if COMENTARIO:
                    server.send_turn(1, game.view(-1)+'\n'+msg1)
                    server.send_turn(2, game.view(-2)+'\n'+msg2)
                else:
                    server.send_turn(1, game.view(-1))
                    server.send_turn(2, game.view(-2))
            else:
                if COMENTARIO:
                    server.send_turn(1, game.view(1)+'\n'+msg1)
                    server.send_turn(2, game.view(2)+'\n'+msg2)
                else:
                    server.send_turn(1, game.view(1))
                    server.send_turn(2, game.view(2))

            print('Turno {}: player {}'.format(game.turn, turno_player))



            comando = server.recv_comandos(turno_player)

            if turno_player == 1:
                game.p1.order(comando)
            else:
                game.p2.order(comando)

            game.turn += 1
            if game.turn%6 == 0:
                game.clearOrderStat()

            game.heal()

        score1 += game.score(1)
        score2 += game.score(2)

        server.send_scores(score1, score2)

def main_ia():
    from ai import AI

    game = Game()

    IA_1 = AI(player=0)
    IA_2 = AI(player=1)

    score1 = 0
    score2 = 0

    for partida in range(1):

        game.__init__()

        while game.turn < MAX_TURN:

            print('~~~~TURNO:  ', game.turn)

            if partida == 0:
                turno_player = game.turn%2 + 1
            elif partida == 1:
                turno_player = 2-game.turn%2

            if turno_player == 1: #IA_1
                IA = IA_1
            else:
                IA = IA_2

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

        score1 += game.score(1)
        score2 += game.score(2)

    print('\nSCORES:')
    print('Player1', score1)
    print('Player2', score2)


    IA_1.set_scores(score1, score2)


def main(modo = 'IH', numPartidas = 2): #substituir todos os outros mains

    
    from human import Human
    from ai import AI
    
    if modo == 'HH':
        main_human()
        return
    elif modo == 'HI':
        player0 = Human(player=0)
        player1 = AI(player=1)
        pass
    elif modo == 'IH':
        from ai import AI
        from human import Human
        player0 = AI(player=1)
        player1 = Human(player=1)
        pass
    elif modo == 'II':
        from ai import AI
        main_human()
    else:
        print ('Modo ERROR')

    score0 = 0
    score1 = 0

    game = Game()

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
    print('Player1', score1)
    print('Player2', score2)


    IA_1.set_scores(score1, score2)

main('II')