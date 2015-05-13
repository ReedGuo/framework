#-*- coding: UTF-8 -*-

'''
本类涉及到berkeley db的所有基础操作
目的：构建URL的TODO表
'''

from bsddb import db
from commonutil import CommonUtil
import sys,os

dirname=os.path.dirname(sys.argv[0])#数据库存放路径
dirname += '/berkeleydb'

commonUtil = CommonUtil()
#基类
class CrawlerDB:
    
    #dbFile:数据库名字。如visited.db
    #envFile：数据库环境的路径
    def __init__(self, dbFile, envFile=dirname):
        self.databaseFile = dbFile#数据库名字
        try:
            os.mkdir(envFile)
        except:
            pass
        self.dbenv = db.DBEnv()# 创建数据库环境
        self.dbenv.open(envFile, db.DB_CREATE | db.DB_INIT_MPOOL)# 打开数据库环境。db.DB_INIT_MPOOL：  Initialize the shared memory buffer pool subsystem. This subsystem should be used whenever an application is using any Berkeley DB access method.
        self.database = db.DB(self.dbenv,0)#构造一个数据库
    
    #关掉数据库 
    def __del__(self):
        self.database.sync()
        self.database.close()
        self.dbenv.close()
        
    #打开数据库
    #dbtype:数据结构类型。分为队列类型和hash类型等等
    #open函数的原型：open(filename, dbname=None, dbtype=DB_UNKNOWN, flags=0, mode=0660, txn=None)
    def openDb(self, dbtype):
        self.dbType = dbtype
        if not dbtype:
            raise RuntimeError('Dbtype can not be null.')
        if dbtype == 'DB_HASH':
            self.database.open(self.databaseFile,dbname=None,dbtype=db.DB_HASH,flags=db.DB_CREATE,mode=0,txn=None)
        elif dbtype == 'DB_BTREE':
            self.database.open(self.databaseFile,dbname=None,dbtype=db.DB_BTREE,flags=db.DB_CREATE,mode=0,txn=None)
        elif dbtype == 'DB_QUEUE':#Ordered
            self.database.set_re_len(1024)
            self.database.open(self.databaseFile,dbname=None,dbtype=db.DB_QUEUE,flags=db.DB_CREATE,mode=0,txn=None)
        elif dbtype == 'DB_RECNO':
            self.database.open(self.databaseFile,dbname=None,dbtype=db.DB_RECNO,flags=db.DB_CREATE,mode=0,txn=None)
    
    #从队列的顶部拿到一个url
    def popUrl(self):
        return self.database.consume()#消费一个url
    
    #将key/value对 插入到数据库
    #参数 key:单个的url
    def insertUrl(self,key,val='',md5=False):
        key = key.lower()
        if md5:
            key = commonUtil.md5Str(key)
        if self.dbType=='DB_QUEUE' or self.dbType =='DB_RECNO':
            self.database.append(key)
        else:
            self.database.put(key,val)
        self.database.sync()
        
    #根据key得到value
    #参数 key:单个的url
    def selectValue(self,key,md5=False):
        key = key.lower()
        if md5:
            val = self.database.get(commonUtil.md5Str(key))
        else:
            val = self.database.get(key)
        return val
    
    #删除key/value对
    #参数 key:单个的url
    def deleteKey(self,key,md5=False):
        key = key.lower()
        try:
            if md5:
                self.database.delete(commonUtil.md5Str(key))
            else:
                self.database.delete(key)
        except:
            pass

    #是否存在指定的key
    #参数 key:单个的url
    def existKey(self,key,md5=False):
        key = key.lower()
        if md5:
            sval = self.database.get(commonUtil.md5Str(key))
        else:
            sval = self.database.get(key)
        if sval != None:
            return True
        else:
            return False

    #得到游标
    def getCursor(self):
        return self.database.cursor()

    #将数据库内容清空
    def truncate(self):
        self.database.truncate()
    
    #得到key/value数目
    def getCount(self):
        return len(self.database.items())
   
    
if __name__ == "__main__":
    pass
    