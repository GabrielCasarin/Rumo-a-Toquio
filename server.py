##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

import socket
import json

class Server:
    def __init__(self):
        super(Server, self).__init__()
        
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        with open('config/config.json') as jfile:
            config = json.load(jfile)
            self.serversocket.bind((config['ip'], config['port']))

        self.serversocket.listen(2)

    def aguardar_jogadores(self):
        #Regras do jogo:
        #manda 0 para o player 1
        #manda 1 para o player 2
        print('servidor iniciado')
        print('aguardando conexoes...')
        self.sock_player1, addr = self.serversocket.accept()
        print('player 1 conectou-se')
        print('endereco:', addr, '')
        self.sock_player1.send(bytes('0', 'ascii'))
        self.sock_player2, addr = self.serversocket.accept()
        print('player 2 conectou-se')
        print('endereco:', addr, '')
        self.sock_player2.send(bytes('1', 'ascii'))

    def send_turn(self, player, turn_msg):
        if player == 1:
            self.sock_player1.send(bytes(turn_msg, 'ascii'))
            print('enviei1\n'+turn_msg)
        elif player == 2:
            self.sock_player2.send(bytes(turn_msg, 'ascii'))
            print('enviei2\n'+turn_msg)
        else:
            print('player', player, 'não existe')

    def recv_comandos(self, player):
        comandos = None
        if player == 1:
            print('aguardando envio de comandos por parte do player %d...'%player)
            comandos = str(self.sock_player1.recv(1024), 'ascii')
            print('comandos recebidos')
        elif player == 2:
            print('aguardando envio de comandos por parte do player %d...'%player)
            comandos = str(self.sock_player2.recv(1024), 'ascii')
            print('comandos recebidos')
        else:
            print('player', player, 'não existe')
        return comandos

    def send_scores(self, score_p1, score_p2):
        msg = '{} {}'.format(score_p1, score_p2)
        print('Placar enviado:', msg)
        self.sock_player1.send(bytes(msg, 'ascii'))
        self.sock_player2.send(bytes(msg, 'ascii'))
        r1 = str(self.sock_player1.recv(1024), 'ascii')
        print('Player 1 respondeu:', r1)
        r2 = str(self.sock_player2.recv(1024), 'ascii')
        print('Player 2 respondeu:', r2)
        if (r1 == 'ok'
            and r2 == 'ok'):
                print('ambos receberam placar')
        else:
            print('algo deu errado na transmissão do placar')

    def fechar_conexoes(self):
        self.sock_player1.close()
        self.sock_player2.close()
        self.serversocket.shutdown(socket.SHUT_RDWR)
        self.serversocket.close()
