import os

DIR = 'SamurAI/database/tmp/'
def main():
	#deve apagar todos os arquivos em Jogos_db
	y = input('Quer mesmo apagar todos os arquivos? (y)')
	if y == 'y':
		os.remove(DIR + 'historico_jogos.fs')
		os.remove(DIR + 'historico_jogos.fs.index')
		os.remove(DIR + 'historico_jogos.fs.lock')
		os.remove(DIR + 'historico_jogos.fs.tmp')

if __name__ == '__main__':
    main()