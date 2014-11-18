#-*- coding: UTF-8 -*-
import pg,re,sys
from commonutil import CommonUtil

commonutil = CommonUtil()

class PGDB: 
    '''
    全局变量
    '''
    Link=False#与数据库的链接
    Err=''#错误
    database=''#数据库名字
    dbhost=''#ip
    dbuser=''#数据库用户名
    dbpwd=''#数据库密码
    dbport=''
    
    #构造函数
    def __init__(self,dbhost,dbuser,dbpwd,database,port=5432,ifAutoCommit=True):
        self.dbhost  = dbhost
        self.dbuser  = dbuser
        self.dbpwd   = dbpwd
        self.database= database
        self.dbport=port
        self.ifAutoCommit = ifAutoCommit
        try:
            self.Link = pg.connect(dbname = database, host = dbhost, user = dbuser, passwd = dbpwd, port=port)
            if not ifAutoCommit:
                self.Link.query("begin")
        except Exception, e:
            self.Err=e.args[0]
            self.Link=False

             
    #重新链接         
    def relink(self):
        try:
            self.Link = pg.connect(dbname=self.database, host = self.dbhost, user = self.dbuser, passwd = self.dbpwd,port=self.dbport)
            if not self.ifAutoCommit:
                self.Link.query("begin")
        except Exception, e:
            self.Err=e.args[0]
            self.Link=False
             
    #查询
    def query(self,sql):
        self.Err = ''
        if not commonutil.isStr(sql):
            self.Err = 'the format of sql statement is incorrect'
            return False
        sql=sql.strip()
        
        if not re.search('^select',sql,re.I):#忽略大小写，判断sql语句中是否有select
            self.Err = 'sql statement error, because it does not contains "select".'
            return False
        
        try:
            resultset = self.Link.query(sql)
        except Exception, e:
            self.Err=e.args[0]
            return False
        self.Err=''
        return resultset.dictresult()
    
    #插入
    #参数：  table:数据表的名字，如site_base.customer
    #参数： data:要插入的数据
    def insert(self,table,data):
        self.Err = ''
        if not commonutil.isDict(data):
            self.Err='the format of data is incorrect'
            return False
        sql='insert into '+table+' '
        keys=''
        vals=''
        for i in data:
            keys+='"'+str(i)+'",'
            v=str(data[i])
            v=v.strip()
            if v=='' or v.lower()=='null':
                vals+="null,"
            else:
                vals+="'"+pg.escape_string(str(data[i]))+"',"
        keys=keys.strip(',')
        vals=vals.strip(',')
        sql=sql+"("+keys+") values("+vals+")"

        try:
            self.Link.query(sql)
        except Exception, e:
            self.Err=e.args[0]
            return False
        return True
        
    #批量插入
    #插入
    #参数：  table:数据表的名字，如site_base.customer
    #参数： dataList:要插入的数据列表
    def batchInsert(self,table,dataList):
        self.Err = ''
        if not commonutil.isList(dataList):
            self.Err='the format of data is incorrect'
            return False
        sqlList = []
        for dataDict in dataList:
            sql='insert into '+table+' '
            keys=''
            vals=''
            for i in dataDict:
                keys+='"'+str(i)+'",'
                v=str(dataDict[i])
                v=v.strip()
                if v=='' or v.lower()=='null':
                    vals+="null,"
                else:
                    vals+="'"+pg.escape_string(str(dataDict[i]))+"',"
            keys=keys.strip(',')
            vals=vals.strip(',')
            sql=sql+"("+keys+") values("+vals+")"
            sqlList.append(sql)
        try:
            for eachSql in sqlList:
                self.Link.query(eachSql)
        except Exception, e:
            self.Err=e.args[0]
            return False
        return True
    
    
    #更新
    #参数：  sql:  sql语句
    def update(self,sql):
        self.Err = ''
        if not re.search('^update',sql,re.I):#忽略大小写，判断sql语句中是否有update
            self.Err = 'sql statement error, because it does not contains "update".'
            return False
        try:
            self.Link.query(sql)
        except Exception, e:
            self.Err=e.args[0]
            return False
        return True
    
    #执行一个sql语句
    def executeSqlStatement(self,sql_statement):
        self.Err = ''
        try:
            self.Link.query(sql_statement)
        except Exception, e:
            self.Err=e.args[0]
            return False
        return True 
    
    #删除
    #参数：  sql:  sql语句
    def delete(self,sql):
        self.Err = ''
        if not re.search('^delete',sql,re.I):#忽略大小写，判断sql语句中是否有delete
            self.Err = 'sql statement error, because it does not contains "delete".'
            return False
        try:
            self.Link.query(sql)
        except Exception, e:
            self.Err=e.args[0]
            return False
        return True
    
    #事务提交
    def commit(self):
        try:
            self.Link.query("commit")
            return True
        except Exception, e:
            self.Err = e.args[0]
            return False
    
    #事务回滚
    def rollback(self):
        try:
            self.Link.query("rollback")
            return True
        except Exception, e:
            self.Err = e.args[0]
            return False
    
    #事务终止
    def end(self):
        try:
            self.Link.query("end")
            return True
        except Exception, e:
            self.Err = e.args[0]
            return False
            
    #断开链接    
    def __del__(self):
        try:
            self.Link.close()
        except:
            pass
    
        
if __name__=='__main__':
    psql=PGDB('172.18.65.200','gpadmin','','finance',ifAutoCommit=False)
    sql_1 = "insert into site_base.finance_t_data_log(data_log_desc) values ('download success1');"
    print psql.executeSqlStatement(sql_1)
    sql_2 = "insert into site_base.finance_t_data_log(data_log_desc) values ('download success2');"
    print psql.executeSqlStatement(sql_2)
    datadict = psql.query('select id from site_ase.pivotal_revenue limit 3;')
    psql.commit()
