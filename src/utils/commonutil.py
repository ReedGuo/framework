#-*- coding: UTF-8 -*-
import sys,time,os,urllib
from hashlib import md5

#显示进度条
#将带时间格式的字符串替换成真正的时间字符串
#将字典类型的数据转换成url码
#延迟退出，要不然调试窗口一下子就没有了
#打开文件或应用程序
#将字符串用md5压缩
#睡眠一会儿
#是否是str类型。返回True 或False
#将网页转码,避免生成乱码 


class CommonUtil:
    def __init__(self):
        pass

    #显示进度条
    #参数：i:当前第几个文件  total:总共有几个文件
    def showProgress(self,i,total,message='Current Progress'):
        Jindu=str(round((i/float(total))*100,2))#进度条
        Progress = message + ': %d/%d %s%%' %(i,total,Jindu)
        print Progress+"                           \r",
        sys.stdout.flush()
    
    #将带时间格式的字符串替换成真正的时间字符串
    #参数： strWithDate  带时间参数的字符串 如guofeng_%Y-%m-%d-%H:%M:%S.csv   。此函数将把它变成  guofeng_2014-08-30-13:53:01.csv
    def replaceStrWithDate(self,strWithDate):
        return time.strftime(strWithDate, time.localtime())
    
    #将字典类型的数据转换成url码
    #参数： dictData：字典数据
    def dictToUrlData(self,dictData):
        if not commonutil.isDict(dictData):#如果要转换的数据不是字典类型
            return ''
        
        ret=''
        for i in dictData:
            ret+='&'+urllib.quote(str(i))+'='+urllib.quote(str(dictData[i]))
        ret=ret.lstrip('&')
        return ret
     
    #延迟退出，要不然调试窗口一下子就没有了
    #参数：msg 要打印的信息  seconds:sleep的时间
    def delayExit(self,msg,seconds):
        print msg
        time.sleep(seconds)
        sys.exit()
    
    #打开文件或应用程序
    #fileName  程序名或文件名
    def openFileOrProgram(self,fileName):
        os.startfile(fileName)
        
    #将字符串用md5压缩
    #参数：content：要压缩的内容
    def md5Str(self,content):
        m = md5.new(content)
        m.digest()
        return m.hexdigest()
    
    #睡眠一会儿
    #参数： seconds 睡眠的时间(秒)
    def programSleep(self, seconds):
        for i in range(1,seconds+1):
            time.sleep(1)
            print "sleep",i,"of",seconds
                
                    
    #是否是str类型。返回True 或False
    #参数：obj:变量名
    def isStr(self,obj):
        return 'str' in str(type(obj))
    
    #是否是List类型.即[]
    def isList(self,obj):
        return 'list' in str(type(obj))
    
    #是否是boolean类型
    def isBool(self,obj):
        return 'bool' in str(type(obj))
    
    #是否是字典类型。即{}
    def isDict(self,obj):
        return 'dict' in str(type(obj))
    
    #是否是file类型。
    def isFile(self,obj):
        return 'file' in str(type(obj))
    
    #将网页转码,避免生成乱码 
    #参数：sourceCode:原始编码。newCode:新编码。其中原始编码在网页的头部可以找到
    def convertCoding(self,sourceCode,newCode,content):
        try:
            out=unicode(content,sourceCode,'ignore')
            outgbk=out.encode(newCode,'ignore')
            return outgbk
        except:
            return content
    

if __name__ == '__main__':  
    commonutil = CommonUtil()
    reed = 'guo%Y%m%d'






    

