#-*- coding: UTF-8 -*-

'''
本类负责底层的网页抓取
'''
import pycurl,re,StringIO,time,sys
from commonutil import CommonUtil
#http://curl.haxx.se/libcurl/c/curl_easy_setopt.html
#http://note.sdo.com/u/1500295617/NoteContent/prb71~km-Z0wLX0NY0047G


class DownloadUtil:

    #构造函数，初始化
    def __init__(self):
        #以下属性基本固定，不太需要修改
        self.charset = 'utf-8'#网站编码字体，如utf-8
        self.encoding="gzip,deflate,sdch"
        self.headerParams = ["Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"]
        
        #以下属性必须在抓包前初始化
        self.userAgent="Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"#伪装成浏览器。或者伪装成百度爬虫：  Baiduspider+(+http://www.baidu.com/search/spider.htm)
        self.connectionTimeout=60#Timeout for the connection phase. seconds
        self.operationTimeout=120#the maximum time in seconds that you allow the libcurl transfer operation to take
        self.referer=False#该页面从何而来
        self.httpAuth=False#用户名和密码，如    foucheng:Guofeng
        self.httpAuthType=pycurl.HTTPAUTH_NTLM#有两种方式。一种是pycurl.HTTPAUTH_NTLM(qtool,obiee都是用这种)，另一种是pycurl.HTTPAUTH_BASIC
        self.POST=False#提交方式。 默认是GET
        self.DATA=False#POST方式时，必须要有DATA
        self.COOKIE=False#cookie路径
        self.agency={}#使用代理 代理的作用：1.提高访问速度， 大多数的代理服务器都有缓存功能。2.突破限制， 也就是翻墙了  3.隐藏身份。
        self.isDownload=False#是打开网页还是下载
        self.noProgress = 1#是否显示 下载/上传 进度条
        
        
    #得到httpauth登录类型
    def setHttpAuthType(self,type='ntlm'):
        if type=='ntlm':
            pass
        elif type=='basic':
            self.httpAuthType = pycurl.HTTPAUTH_BASIC
    
    #增加头部参数
    def setHeaderParams(self,headerKey,headerValue):
        combineStr = headerKey+':'+headerValue
        self.headerParams.append(combineStr)
    
    #抓包
    #参数 url 要抓取网址的Url
    def download(self,url):
        c = pycurl.Curl()#实例化对象
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.USERAGENT, self.userAgent)#伪装成某代理
        c.setopt(pycurl.CONNECTTIMEOUT, self.connectionTimeout)#链接超时
        c.setopt(pycurl.TIMEOUT, self.operationTimeout)#操作超时
        c.setopt(pycurl.ENCODING, self.encoding)#encoding
        c.setopt(pycurl.HTTPHEADER, self.headerParams)#Accept信息
        c.setopt(pycurl.DNS_CACHE_TIMEOUT,60)#设置保存DNS信息的时间，默认为60秒 
        if self.referer:
            c.setopt(pycurl.REFERER, self.referer)#告诉服务器从哪个连接过来的。
        if self.httpAuth:#auth
            c.setopt(pycurl.HTTPAUTH, self.httpAuthType)#request header中authorization需要这个信息
            c.setopt(pycurl.USERPWD, self.httpAuth)
        if self.agency.has_key('ADD') and self.agency.has_key('PWD'):#agency
            c.setopt(pycurl.PROXY,self.agency['ADD'])
            c.setopt(pycurl.PROXYUSERPWD,self.agency['PWD'])#浏览器代理
        if self.COOKIE:#cookie
            c.setopt(pycurl.COOKIEFILE, self.COOKIE)
            c.setopt(pycurl.COOKIEJAR, self.COOKIE)
        if self.POST:#post
            if self.DATA:
                Data=self.DATA
            else:
                print 'DATA is necessary when request type is POST'
                return False
            c.setopt(pycurl.POST, 1)
            c.setopt(pycurl.POSTFIELDS, Data)
            self.POST=0
        
        self.headerWrite=StringIO.StringIO()#通过回调函数，不断把response header信息写入.(StringIO作为'内存文件'对象)       
        if self.isDownload:#download
            self.b = open(self.isDownload, 'wb')#把文件下载到DownLoad这个文件中
        else:
            self.b = StringIO.StringIO()#声明一个StringIO对象，在内存缓冲区写入内容
        
        ######################################################以下三个需要调用回调函数  
        c.setopt(pycurl.WRITEFUNCTION, self.contentWriteCallBack)#把网页内容写入
        c.setopt(pycurl.HEADERFUNCTION, self.headerWriteCallBack)#将头部信息（response header）写入
        if self.isDownload:#下载或上传时回调函数
            c.setopt(pycurl.NOPROGRESS, self.noProgress)
            c.setopt(pycurl.PROGRESSFUNCTION, self.progressWriteCallBack)#把进度输出
        ######################################################     
        
        c.setopt(pycurl.FOLLOWLOCATION, 1)#支持重定向  即http code 是3开头的
        c.setopt(pycurl.MAXREDIRS,10)#最大重定向数为10，防止爬虫陷阱
        c.setopt(pycurl.SSL_VERIFYPEER, 0)#SSL certificate   
        c.setopt(pycurl.SSL_VERIFYHOST, 0)#SSL certificate
        
        c.setopt(pycurl.NOSIGNAL, 1)#This option is here to allow multi-threaded unix applications to still set/use all timeout options etc, without risking getting signals.
        #c.setopt(pycurl.FRESH_CONNECT,1)#强制获取新的连接，即替代缓存中的连接
        #c.setopt(pycurl.FORBID_REUSE, 1)#完成交互后强制断开连接，不重用
        #c.setopt(pycurl.SOCKET_TIMEOUT, 9)
        #c.setopt(pycurl.E_OPERATION_TIMEOUTED, 3600)
 
        #开始访问
        try:
            c.perform()#执行curl
            
            #以下为抓包的一些详细信息.以毫秒为单位
            dnsTime =  c.getinfo(c.NAMELOOKUP_TIME)*1000#域名解析时间
            connectTimeTemp =  c.getinfo(c.CONNECT_TIME)*1000#远程服务器连接时间
            preTransferTimeTemp =   c.getinfo(c.PRETRANSFER_TIME)*1000#从建立连接到准备传输所消耗的时间
            startTransferTimeTemp = c.getinfo(c.STARTTRANSFER_TIME)*1000#从准备传输到传输第一个字节消耗的时间
            totalTime = c.getinfo(c.TOTAL_TIME)*1000#上一请求总的时间
            connectTime = connectTimeTemp - dnsTime
            transferTime = totalTime - preTransferTimeTemp
            
            #print 'dnsTime:',dnsTime
            #print 'connectTime:',connectTime
            #print 'transferTime:',transferTime
            #print 'totalTime:',totalTime
            
            if self.isDownload:
                c.close()
                self.b.close()#关闭文件
                self.isDownload = False
                return True
            
            self.headerContent=self.headerWrite.getvalue()#访问结束后，从response headers获取返回值
            self.httpCode=c.getinfo(c.HTTP_CODE)#HTTP状态码
            contenttype = re.compile('charset=(.*)',re.I|re.S|re.M).findall(c.getinfo(c.CONTENT_TYPE))#c.getinfo(c.CONTENT_TYPE)的返回值为text/html; charset=utf-8
            if contenttype:
                webCharset = contenttype[0]
            else:
                webCharset = self.charset
            
            value= self.b.getvalue()
            if webCharset.lower() !='utf-8':
                #print 'encoding to utf-8...'
                commonutil = CommonUtil()
                value = commonutil.convertCoding(webCharset,self.charset,value)
            c.close()
            self.b.close()
            
            if self.httpCode>=400:
                errorMessages = re.compile('<title>(.*)</title>',re.I|re.S|re.M).findall(value)
                if errorMessages:
                    errorMessage = errorMessages[0]
                else:
                    errorMessage = 'Http code >=400'
                raise pycurl.error(errorMessage.decode('UTF-8'))#decode是为了处理中文
        except pycurl.error, e:
            print sys.exc_info()[0],sys.exc_info()[1]#打印错误信息
            return False
        
        return value
    
##################回调函数###############################################

    #网页内容的回调函数
    def contentWriteCallBack(self,buf):
        self.b.write(buf)
    
    #头部信息的回调函数
    def headerWriteCallBack(self,buf):
        self.headerWrite.truncate()#从当前位置开始，后面的内容全部删除
        self.headerWrite.write(str(buf))
        
    #下载/上传进度
    def progressWriteCallBack(self,downloadTotal,downloadNow,uploadTotal,uploadNow):
        if downloadTotal > 0:
            Progress = 'download progress:  ' + str(round((downloadNow/downloadTotal)*100,2)) + '%'
            print Progress+"                           \r"
        else:
            if uploadTotal > 0:
                Progress = 'upload progress:  ' + str(round((uploadNow/uploadTotal)*100,2)) + '%'
                print Progress+"                           \r"
#######################回调函数结束##################################################
 
if __name__=='__main__':
    from fileutil import FileUtil
    fileutil = FileUtil()
    downloadutil = DownloadUtil()
    value = downloadutil.download('http://s.taobao.com/search?q=10%E5%85%83%E5%8C%85%E9%82%AE')
    if value:
        print 'Login success'
        fileutil.writeIntoFile('C:/Users/guo_f/Desktop/compare/search_pycurl.html',value)
    else:
        print 'error'