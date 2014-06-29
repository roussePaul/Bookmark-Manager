from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
import transaction

db = 0
class MyZODB(object):
    def __init__(self, path):
        self.storage = FileStorage(path)
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.dbroot = self.connection.root()

    def close(self):
        self.connection.close()
        self.db.close()
        self.storage.close()

def initBDD():
    global db
    db = MyZODB('Data.fs')

def closeBDD():
    global db
    transaction.commit()
    db.close()

def putTag(tag,n):
    global db
    root = db.dbroot
    root[tag] = n

def putTags(t1,t2,n):
    global db
    root = db.dbroot
    root[(t1,t2)] = n
    
def getTag(tag):
    global db
    root = db.dbroot
    
    if tag in root.keys():
        return root[tag]
    else:
        return -1

def getTags(t1,t2):
    global db
    root = db.dbroot
    if (t1,t2) in root.keys():
        return root[(t1,t2)]
    elif (t2,t1) in root.keys():
        return root[(t2,t1)]
    else:
        return -1
