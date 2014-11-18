#-*- coding: UTF-8 -*-
from bsddb import db
from utils.commonutil import *
dirname=os.path.dirname(sys.argv[0])
dirname += '/crawler/berkeleydb'
#基类
class CrawlerDB:
    def __init__(self, db_file, env_file=dirname+'/db_home'):
        self.database_file = db_file
        try:
            os.mkdir(env_file)
        except:
            pass
        self.dbenv = db.DBEnv()# 创建数据库环境
        self.dbenv.open(env_file, db.DB_CREATE | db.DB_INIT_MPOOL)# 打开数据库环境
        self.database = db.DB(self.dbenv,0)

    #打开数据库
    def open_db(self, dbtype, readonly):
        if readonly == True:
            self.BDB.open(self.database_file,dbname=None,mode=0,txn=None)
            return
        if dbtype == 'DB_HASH':
            #if cache == True:
                #self.BDB.set_cachesize(0,536870912)
            self.database.open(self.database_file,dbname=None,dbtype=db.DB_HASH,flags=db.DB_CREATE,mode=0,txn=None)
        elif dbtype == 'DB_BTREE':
            #if cache == True:
                #self.BDB.set_cachesize(0,536870912)
            self.database.open(self.database_file,dbname=None,dbtype=db.DB_BTREE,flags=db.DB_CREATE,mode=0,txn=None)
        elif dbtype == 'DB_QUEUE':
            self.database.set_re_len(1024)
            self.database.open(self.database_file,dbname=None,dbtype=db.DB_QUEUE,flags=db.DB_CREATE,mode=0,txn=None)
        elif dbtype == 'DB_RECNO':
            self.database.open(self.database_file,dbname=None,dbtype=db.DB_RECNO,flags=db.DB_CREATE,mode=0,txn=None)
        else:
            self.database.open(self.database_file,dbname=None,mode=0,txn=None)
    
    #将key/value对插入到数据库
    #参数 key:单个的url
    def insertUrl(self,key,val=""):
        try:
            self.database.put(md5Str(key),val)
            self.database.sync()
        except:
            raise
        
    #将key/value对插入到数据库
    #参数 keys: url list
    def insertUrls(self,keys,val=""):
        try:
            for key in keys:
                self.database.put(md5Str(key),val)
            self.database.sync()
        except:
            raise

    #根据key得到value
    def selectValue(self,key):
        val = self.database.get(md5Str(key))
        return val
    
    #删除key/value对
    def deleteKey(self,key):
        try:
            self.database.delete(md5Str(key))
        except:
            return False
        return True

    #是否存在指定的key
    def existKey(self,key):
        sval = self.database.get(md5Str(key))
        if sval != None:
            return True
        else:
            return False

    #关掉数据库 
    def __del__(self):
        try:
            self.database.sync()
            self.database.close()
            self.dbenv.close()
        except:
            pass
        

    #得到游标
    def get_cursor(self):
        return self.database.cursor()

    #将数据库内容清空
    def truncate(self):
        self.database.truncate()
    
    #得到key/value数目
    def getCount(self):
        return len(self.database.items())    
    
#构造未访问的爬虫队列
#继承自berleley db基础类        用了queue数据结构
class QueueDB(CrawlerDB):
    
    def __init__(self, dbfile='unvisited.db'):
        CrawlerDB.__init__(self, dbfile)
        self.open_db('DB_QUEUE', False)
    
    #从队列取出一个元素    
    def popUrl(self):
        url = self.database.consume()#消费一个url
        if url == None:#means crawling task is done.
            return url
        url = url[1].strip()
        return url
    
    #把元素追加到队列中
    def pushUrls(self, url_list):
        for url in url_list:
            self.database.append(url)
            
    
#构造已访问的爬虫 hash set
#继承自berleley db基础类        用了hash数据结构
class VisitedDB(CrawlerDB):
    def __init__(self, dbfile='visited.db'):
        CrawlerDB.__init__(self, dbfile)
        self.open_db('DB_HASH', False)
    
    #得到不重复的url list
    def getUniqueUrlList(self, url_list):
        unique_urls = []
        for url in url_list:
            if not self.existKey(url):
                self.insertUrl(url)
                unique_urls.append(url)
        return unique_urls
    
    
if __name__ == "__main__":

    visitedobj = VisitedDB()
    visitedobj.insertUrl('wwer', 'gf')
    #print visitedobj.select('guofeng')
    print visitedobj.getCount()

    '''
    queuedb = QueueDB()
    queuedb.pushUrls(['www.baidu.com','www.google.com'])
    print queuedb.getUrlCount()
    '''