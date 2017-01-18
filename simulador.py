##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

from gamemanager import Game, Jogador, Samurai


class Simulador:
	def __init__(self, estadosdb):
		self.game = Game()
		self.estadosdb = estadosdb

	@property
	def estado(self):
		return self.__estado

	@estado.setter
	def estado(self, s):
		self.__estado = s.copy()
        # atualizar tabuleiro
		self.game.tab = self.__estado.tabuleiro
		self.game.turn = self.__estado.turno
		#TODO: e samurais
		for i in range(3):
			self.game.p1.samurais[i] = ...
		for i in range(3, 6):
			self.game.p2.samurais[i] = ...

	def atuar(self, sam_id, acao):
		budget = self.__estado.budget
		jogador = self.game.jogadores[self.__estado.player]

		cont = True

        msg = "Jogava valida"

		if sam_id in [0,1,2]:
			samurai = jogador.samurais[sam_id]
        else:
            msg = 'Id do samurai invalido, perdeu a vez'

        if samurai.treat > 0: #se esta machucado nao joga
            msg = 'Samurai machucado nao joga'
            cont = False

        if samurai.orderStat == 1: #se ja jogou, nao joga
            msg = 'Samurai ja jogou nesse periodo'
            cont = False
        else:
            samurai.orderStat = 1

		if cont:
			if acao in range(10):
				cont, custo, msg = samurai.action(acao, budget)
			else:
				cont = False
                msg = 'Codigo de acao invalido'

		print(msg)

        # atualizar estado
		# return reward ?
