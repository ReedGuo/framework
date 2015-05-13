#-*- coding: UTF-8 -*-

'''
本类包含文件所有操作
###############文件相关操作##############
#从本地读取文件  
#把内容写到文件中
#按行读取文件
#得到文件的行数
#读csv文件
#生成csv文件
#解析json
#删除文件 
#得到文件所在的目录
#判断文件是否存在
#文件重命名
###############目录相关操作##############
#创建目录
#得到当前目录
#删除目录
#遍历目录下所有文件或目录
###############文件和目录通用相关操作#######
#判断文件或目录是否存在
#获取文件或目录的大小
#得到文件名或目录不含路径的的名字
#得到文件或目录的绝对路径
'''

import csv,os,shutil,json,sys

reload(sys)
sys.setdefaultencoding('utf-8')


class FileUtil:
    def __init__(self):
        pass
    ###################文件的相关操作#######################################
    
    #从本地读取文件  
    #参数：fileName:文件名字。如/usr/tin/qtool_consumer.py
    def readLocalFile(self,fileName,mod='rb'):
        local_file=open(fileName,mod)
        strline=local_file.read()
        local_file.close()
        return strline
    
    #把内容写到文件中  
    #参数：content:要写入的内容   fileName：要写入到哪个文件中去
    #参数 mod: 模式   还可以写成ab，意思是以二进制格式追加.w+表示可读写
    def writeIntoFile(self,fileName,content,mod='wb'):
        local_file=open(fileName,mod)
        local_file.write(content)
        local_file.close()
    
    #按行读取文件
    def readFileLineByLine(self,filename):
        with open(filename) as fh:
            for line in fh: 
                line = line.replace('\n','')
                print line
    
    #得到文件的行数
    #参数 filename：文件名
    def getLineCountOfFile(self,filename):
        return len(open(filename).readlines())
    
    #读csv文件    rely on : https://docs.python.org/2/library/csv.html
    #参数
    #fileName csv文件名字
    #delimiter 数据之间以什么符号分割。默认是以逗号分割的
    #quotechar 文本围栏
    def readCSVFile(self,fileName,delimiter=',',quotechar='"'):
        with open(fileName,'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
            for row in reader:
                print row[0]
                #print row[0].decode('UTF-8')#如果是中文
    
    #生成csv文件
    #参数：  
    #filename 要生成的csv文件名，如/home/gpadmin/reed/reed.csv
    #delimiter    内容之间以什么符号分割。默认是tab符号分割
    #quotechar 如果一个数据内部含有delimit制定的字符，那么就用quotechar制定的字符把它包起来
    def writeCSVFile(self,filename,mod='wb', delimiter='\t',quotechar='^'):
        with open(filename, mod) as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=delimiter,quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['guo','feng','reed'])#参数是数组
    
    #解析json
    def parseJson(self,jsonStr,key):
        token_cmd = '''curl -s -d "grant_type=password" -d "client_id=3MVG9Y6d_Btp4xp6Vd8gA42F.T7wInE20rDK4Pta2LIbHRhXll.HfV_oxUizgVTxkt3Q.C2UcwVnvzz6SeFlB" -d "client_secret=5167302065507657205" -d "username=el" -d "password=Pivotan" https://ap1.salesforce.com/services/oauth2/token''';
        p = subprocess.Popen(token_cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        outputToken = json.loads(stdout)
        access_token = outputToken['access_token']
        print 'access_token',access_token
    
    #解析json文件
    def parseJsonFile(self,outputFile):
        dataList = []
        opportunityCount = 0
        lineitemCount = 0
        with open(outputFile, 'r') as f:
            data = json.load(f)
        opportunityRecords = data['records']
        for eachOpportunityRecord in opportunityRecords:
            opportunityId = eachOpportunityRecord['Id']
            opportunityCount +=1
            opportunityLineItem = eachOpportunityRecord['OpportunityLineItems']
            if opportunityLineItem == None:
                continue
            opportunityLineItemRecords = opportunityLineItem['records']
            for eachLineItemRecord in opportunityLineItemRecords:
                lineId = eachLineItemRecord['Id']
                sku = self.handleFormat(eachLineItemRecord['ProductCode'],'string')
                product = ''
                fullName = self.handleFormat(eachLineItemRecord['PricebookEntry']['Name'],'string')
                priceBook = ''
                quantity = self.handleFormat(eachLineItemRecord['Quantity'],'int')
                uom = self.handleFormat(eachLineItemRecord['Unit_of_Measure__c'],'string')
                listPrice = self.handleFormat(eachLineItemRecord['ListPrice'],'int')
                unitPrice = self.handleFormat(eachLineItemRecord['UnitPrice'],'int')
                totalPrice = self.handleFormat(eachLineItemRecord['TotalPrice'],'int')
                discount = self.handleFormat(eachLineItemRecord['Discount'],'int')
                years = self.handleFormat(eachLineItemRecord['Years__c'],'string')
                firstYearBooking = self.handleFormat(eachLineItemRecord['First_Year_Booking__c'],'int')
                productFamily = self.handleFormat(eachLineItemRecord['Product_Family__c'],'string')
                sellingMotion = self.handleFormat(eachLineItemRecord['Selling_Motion__c'],'string')
                productPortfolio = self.handleFormat(eachLineItemRecord['Product_Portfolio__c'],'string')
                gtmCategory = ''
                manualProductType = ''
                dataDict = {}
                dataDict['opportunityId'] = opportunityId
                dataDict['lineId'] = lineId
                dataDict['sku'] = sku
                dataDict['product'] = product
    
    #删除文件 
    # 参数：fileName  如，/usr/tin/qtool_consumer.py
    def deleteFile(self,fileName):
        os.remove(fileName)
    
    
    #得到文件所在的目录
    #参数：fileName 文件路径
    def getCatalogueOfFile(self,fileName):
        fileName = self.getAbsoluteFilePath(fileName)#先得到文件的绝对路径
        return os.path.split(fileName)[0]
    
    #判断文件是否存在
    #参数 fileName 文件名
    def isExistFile(self,fileName):
        return os.path.isfile(fileName)

    #文件重命名
    #参数：
    #oldFile 旧的文件名
    #newFile 新的文件名
    def renameFile(self,oldFile,newFile):
        os.rename(oldFile,newFile)
    

    ###################目录的相关操作#######################################
    
    #创建目录  
    #参数：directName 目录名
    def createCatalogue(self,directName):
        os.makedirs(directName)
    
    #得到当前目录
    def getCurrentCatalogue(self):
        return os.getcwd()

    #删除目录
    #参数 dirName 目录的名字
    def deleteCatalogue(self,dirName):
        shutil.rmtree(dirName)


    ###################文件目录通用操作#######################################
    
    #判断文件或目录是否存在
    #参数 name 文件或目录名
    def isExistCatalogue(self,name):
        return os.path.exists(name)
    
    #获取文件或目录的大小
    #参数 fileName:文件名字
    def getFileSize(self,fileName):
        try:
            size = os.path.getsize(fileName)
            gSize = size/(1024*1024*1024)
            if  gSize >= 1:
                return str(gSize) + ' G'
            else:
                mSize = size/(1024*1024)
                if mSize >=1:
                    return str(mSize) + ' M'
                else:
                    kSize = size/1024
                    if kSize >=1:
                        return str(kSize) + ' K'
                    else:
                        return str(size) + ' B'
        except:
            return ''
    
    #得到文件名或目录不含路径的名字
    #参数：fileName  带路径的文件名或目录名
    def getBasenameOfFile(self,fileName):
        return os.path.basename(fileName)
    
    #得到文件或目录的绝对路径
    #参数：filePath 文件的相对路径
    def getAbsoluteFilePath(self,filePath):
        allPath=os.path.abspath(filePath)
        return allPath
     
    #遍历目录下所有文件或目录
    def listCatalogue(self,catalogueName):
        files=os.listdir(catalogueName)
        for eachFile in files:
            print eachFile
        
if __name__=='__main__':
    
    
    
    fileutil = FileUtil()
    rightmap = {}
    with open('right.csv','rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            id = row[0]#学籍号
            name = row[1].decode('UTF-8')#姓名
            father = row[2].decode('UTF-8')#爸爸
            sex = row[3].decode('UTF-8')
            relation = row[4].decode('UTF-8')
            att = name + '~' + father + '~' + sex + '~' + relation
            if not rightmap.has_key(id):
                rightmap[id] = att
    
    result = []            
    with open('left.csv','rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            id = row[0]#学籍号
            if rightmap.has_key(id):
                values = rightmap[id]
                attArray = values.split('~')
                name = attArray[0]
                father = attArray[1]
                sex = attArray[2]
                relation = attArray[3]
                row[12] = id
                row[13] = name
                row[14] = father
                row[15] = sex
                row[16] = relation
                result.append(row)
            else:
                print id + ' failed'
                
    #生成csv文件
    with open('./result.csv','wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for eachLine in result:
            spamwriter.writerow(eachLine)#参数是数组
    '''
    content = ''
    idDict = {}
    with open('./info.csv') as fh:
        for line in fh: 
            line = line.replace('\n','')
            lineArray = line.split(',')
            id = lineArray[0]
            print id
            if not idDict.has_key(id):
                idDict[id] = 1
                content += line + '\n'
    fileutil.writeIntoFile('information.csv', content)
    '''
    
    
    
    
    
    
    
    '''
    fileutil = FileUtil()
    #首先把right.csv数据提取出来。学籍号为key,爸爸为value
    leftmap = {}
    with open('left.csv','rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            id = row[0]+row[2].decode('UTF-8')
            if not leftmap.has_key(id):
                leftmap[id] = 1
                
    rightmap = {}
    with open('right.csv','rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            id = row[0]+row[1].decode('UTF-8')
            if not rightmap.has_key(id):
                rightmap[id] = 1
                
    print '在"导出文件"中存在的异常学生为：'
    for i in leftmap:
        if not rightmap.has_key(i):
            print i
            
    print '在"导出文件3"中存在的异常学生为：'
    for j in rightmap:
        if not leftmap.has_key(j):
            print j
    '''
    
    