def init():
    from BTrees.IOBTree import IOBTree
    import ZODB
    import ZODB.FileStorage as FS
    import transaction

    storage = FS.FileStorage('SamurAI/database/IAs/index.fs')
    conn = ZODB.DB(storage).open()                           
    dbroot = conn.root()
    dbroot['ultimo'] = 0
    dbroot['ias'] = IOBTree()

    conn.close()
    storage.close()
