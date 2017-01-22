##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

from config import *
import gui_human_local as gui

class Human:
    def __init__(self, player):
        self.player = player

    def __str__(self):
        return ('Eu sou o Humano {}'.format(self.player))

    def set_turn(self, msg):
        self.estado = msg

    def get_comandos(self):
        listaAcao = gui.cliente(self.estado, self.player)
        print(listaAcao)
        return listaAcao

    def set_scores(self, scoreEu, scoreInim):
        pass
