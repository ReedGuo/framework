#-*- coding: UTF-8 -*-
#所有邮箱服务器的地址：http://wenku.baidu.com/link?url=BsDqc87fYMXG_A-7HXC6qTm-kGHHLNceo9TdRP9c4aozBVDDCPWyjRRuaudltyNbmED3-WL-PPGw18G2c0orrmE1YAgAlBOZFmVxxzqZKJW
#各大邮箱每天发送数量限制http://www.freehao123.com/mail-smtp/
'''
本类包含邮件的两大操作
1.发送邮件 
2.接收邮件
'''


import smtplib,imaplib,email,re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from commonutil import CommonUtil
from fileutil import FileUtil

commonutil = CommonUtil()
fileutil = FileUtil()

  

class EmailUtil:
    
    #参数：server 邮箱类型
    #user：邮箱用户名
    #password：邮箱密码
    def __init__(self,server='google',user='fuzhuangdazhele@gmail.com',password='microsoft!'):
        if server!='qq' and server!='google' and server!='163' and server!='sina':
            print 'Now only accept qq mail, 163 mail, sina mail and google mail'
        self.server = server#邮箱服务器
        self.user = user#邮箱用户名
        self.password = password#邮箱密码
    

    #发送邮件 
    #toList 收件人列表。如：['986851900@qq.com','986851901@qq.com']
    #subject：主题
    #content：邮件内容
    #ccList:抄送
    #bccList:密送
    #mailType：邮件类型。分为三种：纯文本邮件，html邮件，多媒体邮件
    #imagesDict：
    #attachsDict：
    def sendEmail(self,toList,subject,content='Wish you al the best',ccList=[],bccList=[],nickName = 'Reed Guo',mailType='text',imagesDict=[],attachsDict=[]):
        if not toList:
            print 'Make sure receiver list is not empty'
            return False
        if not subject:
            print 'Make sure subject is not empty'
            return False
        if self.server=='google':
            mailHost='smtp.gmail.com:587'
        elif self.server=='qq':
            mailHost='smtp.qq.com'
        elif self.server=='163':
            mailHost='smtp.163.com'
        elif self.server=='sina':
            mailHost = 'smtp.sina.com.cn'
        index = self.user.find('@')    
        mailUser = self.user[:index]#只取@符号之前的
        mailPass = self.password
        sender = nickName + '<' + self.user + '>'
        
        if mailType =='text':#普通文本邮件
            msg = MIMEText(content,_subtype='plain',_charset='UTF-8')
        if mailType == 'html':#html邮件
            msg = MIMEText(content,_subtype='html',_charset='UTF-8')
        if mailType == 'multi':#文本，html，附件，图片都掺杂着
            msg = MIMEMultipart()#声明对象
            msgHtml = MIMEText(content,_subtype='html',_charset='UTF-8')
            msg.attach(msgHtml)
            fp = open('./clothing.jpg', 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID', '<image1>')
            msg.attach(msgImage)
            
                    
            #最后加载附件
            if attachsDict:
                print 'Load attach...'
                attachCount = 1
                for j in attachsDict:
                    nPos = j.rindex("/")+1
                    fileName = j[nPos:]#get the name of file
                    att1 = MIMEText(open(j, 'rb').read(), 'base64', 'UTF-8')
                    att1["Content-Type"] = 'application/octet-stream'
                    att1["Content-Disposition"] = 'attachment; filename='+fileName+'"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
                    msg.attach(att1)
                    attachCount += 1
                 
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ';'.join(toList)
        if ccList:
            msg['Cc'] = ';'.join(ccList)
        if bccList:
            msg['Bcc'] = ';'.join(bccList)
        try:
            smtpServer = smtplib.SMTP()
            smtpServer.connect(mailHost)#连接到指定的smtp服务器
            if self.server=='google':
                smtpServer.starttls()
            smtpServer.login(mailUser,mailPass)#登陆到smtp服务器
            smtpServer.sendmail(sender, toList+ccList+bccList, msg.as_string())
            smtpServer.quit()
            return True
        except Exception, e:
            print 'Failed to send an email because ' + str(e)
            return False
    
    
    #接收邮件   
    #返回：一个list。每个list元素是一个邮件对象。对象包含以下内容：from，attach，text，to，subject
    #folder 要查看的文件夹。有如下几种：inbox,drafts,sent,junk,trash
    #emailStatus 邮件状态。有如下几种：seen,unseen
    #criteria搜索条件。比如说只搜索严盈盈发给我的邮件
    #limit 只取limit封邮件，而不是全取。
    #nohint：是否无痕取信
    #isGetAttach 是否下载附件
    def receiveEmail(self,folder='inbox',emailStatus='unseen',criteria='',limit=0,nohint=0,isGetAttach=False):
        if self.server=='qq' or self.server=='google':
            port = 993
        resultsList = []
        folder = folder.lower()
        folderList = []
        folderList.append('inbox')
        folderList.append('drafts')
        folderList.append('sent')
        folderList.append('junk')
        folderList.append('trash')
        
        if folder not in folderList:
            print 'The value of folder must be one of these: inbox,drafts,sent,junk,trash.'
            return False
        
        emailStatus = emailStatus.upper()
        statusList = []
        statusList.append('SEEN')
        statusList.append('UNSEEN')
        if emailStatus not in statusList:
            print 'The value of emailStatus must be one of these: seen,unseen.'
            return False
        
        if self.server =='qq':
            serverUrl = 'imap.qq.com'
            if folder == 'inbox':
                folder = 'INBOX'
            elif folder == 'drafts':
                folder = 'Drafts'
            elif folder == 'sent':
                folder = 'Sent Messages'
            elif folder == 'junk':
                folder = 'Junk'
            elif folder == 'trash':
                folder = 'Deleted Messages'
        elif self.server == 'google':
            serverUrl = 'imap.googlemail.com'
            if folder == 'inbox':
                folder = 'INBOX'
            elif folder == 'drafts':
                folder = '[Gmail]/Drafts'
            elif folder == 'sent':
                folder = '[Gmail]/Sent Mail'
            elif folder == 'junk':
                folder = '[Gmail]/Spam'
            elif folder == 'trash':
                folder = '[Gmail]/Trash'
        try:
            conn = imaplib.IMAP4_SSL(serverUrl, port)#IMAP4_SSL uses encrypted communication over SSL sockets
            conn.login(self.user, self.password)
            #print conn.list()#打印出所有的folder
            conn.select(folder,False)
            #criteria = '(FROM 986851900@qq.com)'    或者        criteria = '(SUBJECT reed)'
            if folder!='INBOX':
                emailStatus = 'SEEN'#对于已发送、草稿箱来说，都是SEEN状态的。
            if self.server=='google' and criteria:#只有google邮箱才能用到条件搜索
                typ, data = conn.search(None, emailStatus,criteria)#SEEN表示已读的。typ是状态。正确返回OK。data is space separated list of matching message numbers.   #然后返回的是这个收件箱里所有邮件的编号,按接收时间升序排列,最后的表示最近.
            else:
                typ, data = conn.search(None, emailStatus)#SEEN表示已读的。typ是状态。正确返回OK。data is space separated list of matching message numbers.   #然后返回的是这个收件箱里所有邮件的编号,按接收时间升序排列,最后的表示最近.
            emailList = data[0].split()
            emailList.reverse()#让第一封邮件是最近日期的
            for num in emailList:
                if limit!=0 and len(resultsList)>=limit:
                    break
                typ, msg_data = conn.fetch(num, '(UID BODY.PEEK[])')#无痕取信
                msg = email.message_from_string(msg_data[0][1])#把邮件内容转换成email.message实例
                dictEml = EmailtoDict(str(msg),isGetAttach)
                dataDict=dictEml.getData()
                resultsList.append(dataDict)
                if not nohint:#如果不是无痕浏览
                    conn.store(num, '+FLAGS','\Seen')
            return resultsList
        except Exception, e:
            print 'receive email failed because ' + str(e)
            return False
        finally:
            try:
                conn.close()
            except:
                pass
            conn.logout()



#收邮件的一个辅助类
class EmailtoDict:
    
    def __init__(self,content,isGetAttach = False):
        if 'file' in str(type(content)):
            self.msg = email.message_from_file(content)
        else:
            self.msg = email.message_from_string(content)
        
        self.Data = {}
        self.charset=self.getcharset(content)
        self.isGetAttach = isGetAttach#是否下载附件
        subject = self.msg.get("subject")
        h = email.Header.Header(subject)
        dh = email.Header.decode_header(h)
        subject = dh[0][0]
 
        self.Data['subject']=subject
        self.Data['from']=email.utils.parseaddr(self.msg.get("from"))[1]
        self.Data['to']=email.utils.parseaddr(self.msg.get("to"))[1]
        textdate = self.msg.get("Date").split(',')[-1]
        self.Data['date']=re.compile('\(.*?\)').sub('',textdate)
        #self.Data['contents']=[]
        self.Data['content']=''#整个邮件的信息，包括超链接等等
        self.Data['text']=''#文本信息
        
        self.Data['messageid']=email.utils.parseaddr(self.msg.get("Message-ID"))[1]
        self.Data['inreplyto']=email.utils.parseaddr(self.msg.get("In-Reply-To"))[1]
        self.Data['allreferences']=self.msg.get("References")
 
        if self.Data['allreferences']:
            self.Data['references']=email.utils.parseaddr(self.Data['allreferences'])[1]
        else:
            self.Data['references']=''
        self.Data['attach'] = ''
        


    #得到邮件编码
    def getcharset(self,content):
        
        if 'file' in str(type(content)):
            content.seek(0)
            content=content.read()
        s=re.compile('charset\W+([a-z0-9\-]{1,12})\W?',re.I).findall(content)
        if not s:
            return ''
        for i in s:#处理
            v=i.lower()
            if 'utf' in v:
                return 'UTF-8'
            elif 'gb' in v:
                return 'GBK'
            elif 'ascii' in v:
                return 'GBK'
            elif 'iso-8859-1' in v:
                return 'iso-8859-1'
            
        return s[0]
    

    #得到完整的data信息
    def getData(self):
        # 循环信件中的每一个mime(Multipurpose Internet Mail Extensions)的数据块
        for par in self.msg.walk():
 
            if not par.is_multipart():#如果不是多媒体类型
    
                contenttype = par.get_content_type()#如text/plain，text/html
                filename = par.get_filename()
                if not filename:
                    filename=par.get('Content-ID')
                    if filename:
                        filename=filename.strip('>').strip('<')
                
                #如果有附件
                if filename and self.isGetAttach:
                    content_type = par.get('Content-Type')
                    self.Data['attach'] = self.getAttach(filename,content_type,par)
                    
                d=par.get_payload(decode=True).strip()
                if 'text' in contenttype:
                    if 'plain' in contenttype:
                        self.Data['text']=d
                    if 'html' in contenttype:
                        self.Data['content']=d

        #如果只有content却没有text，那么就从content中提取
        if self.Data['content'] and not self.Data['text']:
            self.Data['text']=re.compile('<style[^>]*?>.*?</style>',re.I|re.S|re.M).sub('',self.Data['content'])
            self.Data['text']=re.compile('<script[^>]*?>.*?</script>',re.I|re.S|re.M).sub('',self.Data['text'])
            self.Data['text']=re.compile('<[^>]*?>',re.I|re.S|re.M).sub('',self.Data['text'])
            self.Data['text']=re.compile('\n\s+\n',re.I|re.S|re.M).sub('\n',self.Data['text'])
            self.Data['text']=self.Data['text'].strip()
        
        
        #处理每一部分data，主要是解决乱码
        for i in self.Data:

            if self.charset and self.charset!='UTF-8':
                self.Data[i]=commonutil.convertCoding(self.charset,'UTF-8',self.Data[i])
            else:
                if self.charset:
                    self.Data[i]=unicode(str(self.Data[i]),self.charset,'ignore').encode(self.charset,'ignore')
                else:
                    self.Data[i]=unicode(str(self.Data[i]),'UTF-8','ignore').encode('UTF-8','ignore')
            if self.Data[i]:
                self.Data[i]=self.Data[i].replace('\\',"")
            else:
                self.Data[i]=''
 
        return self.Data
    
    #得到附件
    def getAttach(self,filename,content_type,par,savepath="attachs/"):
        if not '.' in filename and content_type:
            suffixfind=re.compile('name=.*?\.([\w]+)').findall(content_type)
            if suffixfind:
                suffix=suffixfind[0]
                filename='%s.%s' % (filename,suffix)
        if not '.' in filename:
            return ''
                            
        # 下面的三行代码只是为了解码象=?gbk?Q?=CF=E0=C6=AC.rar?=这样的文件名
        h = email.Header.Header(filename)
        dh = email.Header.decode_header(h)
        fname = dh[0][0]
        
        data = par.get_payload(decode=True) #　解码出附件数据，然后存储到文件中
        fpath=savepath+fname
        try:
            fileutil.createCatalogue(savepath)
        except:
            pass
        try:
            fileutil.writeIntoFile(data,fpath) #注意一定要用wb来打开文件，因为附件一般都是二进制文件
        except:
            return ''
   
        return fname

    


if __name__ == '__main__':
    emailutil = EmailUtil()
    status = emailutil.sendEmail(['guo_f@founder.com.cn'],'Test nick name.',ccList=['986851900@qq.com'])#发送邮件
        
 
