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
import transaction


MAX_RNs = 20


class RN_Manager:
    storage = FS.FileStorage(os.path.join('SamurAI', 'database', 'IAs', 'index.fs'))
    db = ZODB.DB(storage)
    conn = db.open()
    dbroot = conn.root()
    ultimo_da_fila = dbroot['ultimo'] #if 'ultimo' in dbroot else 0
    ias = dbroot['ias']

    def __init__(self):
        pass

    @classmethod
    def proximo_indice(cls):
        if len(cls.ias) == MAX_RNs:
            return cls.ultimo_da_fila
        return len(cls.ias)

    @classmethod
    def registrar(cls, nome_arquivo):
        if len(cls.ias) == MAX_RNs:
            # registra o novo arquivo
            cls.ias[cls.ultimo_da_fila] = nome_arquivo
            # avança o ponteiro para o proximo da fila
            cls.ultimo_da_fila = (cls.ultimo_da_fila + 1)%MAX_RNs
            cls.dbroot['ultimo'] = cls.ultimo_da_fila
        else:
            cls.ias[len(cls.ias)] = nome_arquivo
        transaction.commit()

    @classmethod
    def close(cls):
        cls.conn.close()
        cls.db.close()
        cls.storage.close()
