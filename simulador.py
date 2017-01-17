##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################


from gamemanager import Game, Jogador, Samurai


class Simulador:
	def __init__(self):
		pass

	@property
	def estado(self):
		return self.__estado

	@estado.setter
	def estado(self, s):
		self.__estado = s.copy()
        # atualizar tabuleiro e samurais

	def atuar(self, acao):
		pass
        # atualizar estado
		# return reward ?
