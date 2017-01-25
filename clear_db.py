import os

DIR = 'SamurAI/database/tmp/'
def main():
	#deve apagar todos os arquivos em Jogos_db
	y = input('Quer mesmo apagar todos os arquivos? (y)')
	if y == 'y':
		os.remove(DIR + 'Jogos.fs')
		os.remove(DIR + 'Jogos.fs.index')
		os.remove(DIR + 'Jogos.fs.lock')
		os.remove(DIR + 'Jogos.fs.tmp')

if __name__ == '__main__':
    main()