from database.JogadasDB import JogadasDB

j = JogadasDB()

j.imprimir_jogo(len(j.jogos) - 1)

j.close()
