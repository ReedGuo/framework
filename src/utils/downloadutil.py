#-*- coding: UTF-8 -*-
import pycurl,re,StringIO,time,sys
#抓包

class DownloadUtil:

    #构造函数，初始化
    def __init__(self):
        #fixed attributes
        #以下属性基本固定，不太需要修改
        self.USERAGENT="Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"#浏览器信息（模拟浏览器）
        self.CONNECTTIMEOUT=60#建立连接超时时间
        self.TIMEOUT=120#建立连接后，操作超时时间。比如说下载
        self.ENCODING="gzip,deflate,sdch"
        self.REFERER=False#该页面从何而来
        self.header_write=StringIO.StringIO()#通过回调函数，不断把response header信息写入
        
        #changable attributes
        #以下属性必须在抓包前初始化
        self.HTTPAUTH=False#用户名和密码，如    foucheng:Guopete6*
        self.HTTPAUTH_TYPE=pycurl.HTTPAUTH_NTLM#有两种方式。一种是pycurl.HTTPAUTH_NTLM(qtool,obiee都是用这种)，另一种是pycurl.HTTPAUTH_BASIC（发邮件用这种）
        self.POST=False#提交方式。 默认是GET
        self.DATA=False#POST方式时，必须要有DATA
        self.COOKIE=False#cookie路径
        self.HEADERPARAMS = ["Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"]
        self.AGENCY={}#使用代理 代理的作用：1.提高访问速度， 大多数的代理服务器都有缓存功能。2.突破限制， 也就是翻墙了  3.隐藏身份。
        self.DOWNLOAD=False#是打开网页还是下载
        self.NOPROGRESS = 0#是否显示下载/上传进度条
        
        #以下属性的值是在程序执行过程中动态写入的。他们不是http头部信息，而是自己加的。他们的值都是根据response headers得到的
        self.header = False#http状态码。200 正确。302 跳转   404 无法找到
        self.headercontent = False#response header
        self.charset = 'utf-8'#网站编码字体，如utf-8
    
    #得到httpauth登录类型
    def setHttpAuthType(self,type='ntlm'):
        if type=='ntlm':
            pass
        elif type=='basic':
            self.HTTPAUTH_TYPE = pycurl.HTTPAUTH_BASIC
    
    #增加头部参数
    def setHeaderParams(self,headerKey,headerValue):
        combineStr = headerKey+':'+headerValue
        self.HEADERPARAMS.append(combineStr)
    
    #抓包
    #参数 url 要抓取网址的Url
    def download(self,url):
        #time.sleep(1)
        c = pycurl.Curl()#实例化对象
        self.header_write.truncate()#从读写位置起切断数据，参数size限定裁剪长度，缺省值为None。也就是，从读写位置起，把后面的数据都删除了
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.USERAGENT, self.USERAGENT)#伪装成某代理
        c.setopt(pycurl.CONNECTTIMEOUT, self.CONNECTTIMEOUT)#链接超时
        c.setopt(pycurl.TIMEOUT, self.TIMEOUT)#操作超时
        c.setopt(pycurl.ENCODING, self.ENCODING)#encoding
        c.setopt(pycurl.HTTPHEADER, self.HEADERPARAMS)#Accept信息
        if self.REFERER:
            c.setopt(pycurl.REFERER, self.REFERER)#告诉服务器从哪个连接过来的。
        if self.HTTPAUTH:#auth
            c.setopt(pycurl.HTTPAUTH, self.HTTPAUTH_TYPE)#request header中authorization需要这个信息
            c.setopt(pycurl.USERPWD, self.HTTPAUTH)
        if self.AGENCY.has_key('ADD') and self.AGENCY.has_key('PWD'):#agency
            c.setopt(pycurl.PROXY,self.AGENCY['ADD'])
            c.setopt(pycurl.PROXYUSERPWD,self.AGENCY['PWD'])#浏览器代理
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
               
        if self.DOWNLOAD:#download
            self.b = open(self.DOWNLOAD, 'wb')#把文件下载到DownLoad这个文件中
        else:
            self.b = StringIO.StringIO()#声明一个StringIO对象，在内存缓冲区写入内容
        ######################################################以下三个需要调用回调函数  
        c.setopt(pycurl.WRITEFUNCTION, self.contentwrite)
        c.setopt(pycurl.HEADERFUNCTION, self.headerwrite)#将头部信息（response header）写入
        if self.DOWNLOAD:#下载或上传时回调函数
            c.setopt(pycurl.NOPROGRESS, self.NOPROGRESS)
            c.setopt(pycurl.PROGRESSFUNCTION, self.progresswrite)
        ######################################################     
        c.setopt(pycurl.FOLLOWLOCATION, 1)#支持重定向  即http code 是3开头的
        c.setopt(pycurl.MAXREDIRS,10)#最大重定向数为10，防止爬虫陷阱
        c.setopt(pycurl.SSL_VERIFYPEER, 0)#SSL certificate   
        c.setopt(pycurl.SSL_VERIFYHOST, 0)#SSL certificate
        
        c.setopt(pycurl.NOSIGNAL, 1)#using multiple threads, please set it.
        #c.setopt(pycurl.SOCKET_TIMEOUT, 9)
        #c.setopt(pycurl.E_OPERATION_TIMEOUTED, 3600)
 
        #开始访问
        try:
            c.perform()#执行curl
            
            if self.DOWNLOAD:
                c.close()
                self.b.close()#关闭文件
                self.DOWNLOAD = False
                self.NOPROGRESS = 0
                return True
            
            self.headercontent=self.header_write.getvalue()#访问结束后，从response headers获取返回值
            self.header=c.getinfo(c.HTTP_CODE) 
            contenttype = re.compile('charset=(.*)',re.I|re.S|re.M).findall(c.getinfo(c.CONTENT_TYPE))
            if contenttype:
                self.charset = contenttype[0]
            
            value= self.b.getvalue()
            c.close()
            self.b.close()
            if self.header>=400:
                return False
        except pycurl.error, e:
            print sys.exc_info()[0],sys.exc_info()[1]#打印错误信息
            return False

        return value
    
##################回调函数###############################################

    #网页内容的回调函数
    def contentwrite(self,buf):
        self.b.write(buf)
    
    #头部信息的回调函数
    def headerwrite(self,buf):
        self.header_write.truncate()
        self.header_write.write(str(buf))
        
    #下载进度
    def progresswrite(self,download_total,download_now,upload_total,upload_now):
        if download_total > 0:
            Progress = 'download progress:  ' + str(round((download_now/download_total)*100,2)) + '%'
            print Progress+"                           \r"
        else:
            if upload_total > 0:
                Progress = 'upload progress:  ' + str(round((upload_now/upload_total)*100,2)) + '%'
                print Progress+"                           \r"
#######################回调函数结束##################################################

      
if __name__=='__main__':
    pass
