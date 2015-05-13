#-*- coding: UTF-8 -*-

'''
本类包含常用操作
#显示进度条
#调用系统命令（高级用法）
#获取access token(curl方式)
#将带时间格式的字符串替换成真正的时间字符串
#将字典类型的数据转换成url码
#延迟退出，要不然调试窗口一下子就没有了
#打开文件或应用程序
#将字符串用md5压缩
#睡眠一会儿
#是否是str类型。返回True 或False
#将网页转码,避免生成乱码 
#生成随机数
#将列表顺序打乱
#*的使用      *表示数组或列表
#**的使用    **表示字典
#从指定序列中随机获取指定长度的片断
'''

import sys,time,os,urllib,random,subprocess,json
import hashlib


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
    
    
    #调用系统命令（高级用法）
    #参数cmdStr  多条命令以分号分割
    def callSystemCommandAdvance(self,cmdStr):
        p = subprocess.Popen(cmdStr, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print 'stdout:',stdout
        print 'stderr:',stderr
    
    #获取access token
    def getAccessToken(self):
        token_cmd = '''curl -s -d "grant_type=password" -d "client_id=3MVG9Y6d_Btp4xp6Vd8gA42F.T7wInE20rDK4Pta2LIbHRhXll.HfV_oxUizgVTxkt3Q.C2UcwVnvzz6SeFlB" -d "client_secret=5167302065507657205" -d "username=el" -d "password=Pivotan" https://ap1.salesforce.com/services/oauth2/token''';
        p = subprocess.Popen(token_cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        outputToken = json.loads(stdout)
        access_token = outputToken['access_token']
        print 'access_token',access_token
        
    #将带时间格式的字符串替换成真正的时间字符串
    #参数： strWithDate  带时间参数的字符串 如guofeng_%Y-%m-%d-%H:%M:%S.csv   。此函数将把它变成  guofeng_2014-08-30-13:53:01.csv
    def replaceStrWithDate(self,strWithDate):
        return time.strftime(strWithDate, time.localtime())
    
    #将字典类型的数据转换成url码
    #参数： dictData：字典数据
    def dictToUrlData(self,dictData):
        if not self.isDict(dictData):#如果要转换的数据不是字典类型
            print 'Parameter must be dictionary type.'
            return ''
        return urllib.urlencode(dictData)#类似于urllib.quote()
     
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
        m = hashlib.md5()
        m.update(content)
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
    
    #生成随机数
    #type=int整形    type=float浮点型
    def generateRandomNumber(self,beginNumber,endNumber,type='int'):
        if type=='int':
            beginNumber = int(beginNumber)
            endNumber = int(endNumber)
            number = random.randint(beginNumber, endNumber)#beginNumber<=number<=endNumber
        elif type=='float':
            number = random.uniform(beginNumber, endNumber)
        return number
    
    #将列表顺序打乱
    def shuffleListOrder(self,originalList):
        random.shuffle(originalList)
        return originalList
    
    
    #*的使用      *表示数组或列表
    def reedGuo2(self,*size_info):
        print size_info
        print type(size_info)#dict类型
    
    #*的使用      *表示数组或列表    
    def reedGuo3(self,width,height):
        print width,height
    
    #**的使用    **表示字典
    #调用方法  commonutil.reedGuo1(host= 'www.baidu.com' ,port = 'cd',path = 'af')
    def reedGuo1(self,**http_info):
        print http_info
        print type(http_info)#dict类型
    
    #参数 从指定序列中随机获取指定长度的片断
    #seq既可以是list,也可以是字符串
    def getSnip(self,seq,length):
        s = random.sample(seq,length)#返回一个列表
        if self.isStr(seq):
            return ''.join(s)
        return s
        

if __name__ == '__main__':  
    commonutil = CommonUtil()
    dict={}
    dict['name'] = '=4'
    print commonutil.dictToUrlData(dict)
    







    

