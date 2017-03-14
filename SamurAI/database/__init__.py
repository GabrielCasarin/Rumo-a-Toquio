##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################
import os
import ZODB
import ZODB.FileStorage as FS
from BTrees.OOBTree import OOBTree
from BTrees.IOBTree import IOBTree
import transaction
from SamurAI.config import ROOT_DIR
from .Estados import Estado, EstadosManager
from .Jogos import Partida, JogosManager


class DatabaseService:
    def __init__(self, arq='database.fs'):
        # armazena os dados fisicamente no arquivo .fs
        self.storage = FS.FileStorage(os.path.join(ROOT_DIR, 'database', 'jogos', arq))
        # encapsula o objeto de armazenamento (storage),
        # além de prover o comportamento do DB
        self.db = ZODB.DB(self.storage)
        # começa uma conexão com o DB a fim de podermos realizar transações
        self.conn = self.db.open()
        # o objeto root funciona como um namespace para
        # todos os outros contêineres do DB
        self.dbroot = self.conn.root()

        # Cria o esquema de estados
        if 'estados' not in self.dbroot.keys():
            self.dbroot['estados'] = OOBTree()
        self.estados = self.dbroot['estados']

        # Cria o esquema de jogos
        if 'historico_jogos' not in self.dbroot.keys():
            self.dbroot['historico_jogos'] = IOBTree()
        self.historico_jogos = self.dbroot['historico_jogos']
    
    def __enter__(self):
        Estado.objects = EstadosManager(self.estados)
        Partida.objects = JogosManager(self.historico_jogos)

    def __exit__(self, type, value, traceback):
        try:
            transaction.commit()
        except Exception as e:
            raise e
        finally:
            self.conn.close()
            self.db.close()
            self.storage.close()
