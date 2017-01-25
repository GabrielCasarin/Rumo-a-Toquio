import sys

from SamurAI.database.JogadasDB import JogadasDB
from SamurAI.interface import gui_ia as gui


def imprimir_jogo(num_match):
    j = JogadasDB()
    for i in range(len(j.jogos[num_match])):
        rodada = j.jogos[num_match][i]
        print('Rodada', i)
        print('Estado:')
        print(rodada['estado'])
        print('Acao:', rodada['acao'])
        print('Reward:', rodada['reward'])
        print('\n')
        gui.cliente(str(rodada['estado']))

    j.close()

if __name__ == '__main__':
    imprimir_jogo(int(sys.argv[1]))
