#!/usr/bin/python
#-*- coding: UTF-8 -*-
'''
google drive api基础类
'''
import requests,time,httplib2,apiclient.discovery,apiclient.http,oauth2client.client
from apiclient import errors
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload

class GoogleDriveUtil:
    
    def __init__(self,client_id,client_secret,oauth2_scope,redirect_uri,storage_file):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth2_scope = oauth2_scope
        self.redirect_uri = redirect_uri
        self.storage = Storage(storage_file)
        self.credentials = None

#########################授权 开始###############################################    
    #得到授权后的service
    def getService(self):
        self.getCredentials()#首先授权
        http = httplib2.Http()
        http.disable_ssl_certificate_validation = True
        if self.credentials.access_token_expired:#通过token_expiry属性判断access_token是否过期了。
            self.credentials.refresh(http)#如果过期了，就用refresh_token刷新，重新得到access_token
        self.credentials.authorize(http)
        try:
            service = apiclient.discovery.build('drive', 'v2', http=http)
            return service
        except Exception, e:
            return None
        
    
    #得到授权    
    def getCredentials(self):
        self.credentials = self.storage.get()
        if self.credentials == None or self.credentials.invalid:
            self.login()
    #登录
    def login(self):
        flow = oauth2client.client.OAuth2WebServerFlow(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.oauth2_scope,
            user_agent='',
            redirect_uri=self.redirect_uri,
            access_type='offline', # This is the default
            approval_prompt='force'
        )
        authorize_url = flow.step1_get_authorize_url()
        print 'Go to the following link in your browser: ' + authorize_url
        code = raw_input('Enter verification code: ').strip()
        self.credentials = flow.step2_exchange(code)
        self.storage.put(self.credentials)
    
    #验证token是否有效(这个链接有时候走不通，所以暂时没有用到)
    def validToken(self,access_token):
        VALIDATE_URI='https://www.googleapis.com/oauth2/v1/tokeninfo'
        r = requests.get('%s?access_token=%s' % (VALIDATE_URI, access_token))
        if r.status_code==200:
            return True
        else:
            return False
        
############################授权 结束############################################ 


############################Spreadsheet 相关操作 开始############################################         
    ###############revisions相关操作 开始###############
    #list
    #得到revision列表
    def getSpreadsheetRevisionsList(self,service, file_id):
        try:
            revisions = service.revisions().list(fileId=file_id).execute()
            revisionsList = revisions.get('items', [])
            return (True,revisionsList)
        except Exception, e:
            error = 'An error occured when get revision list.'
            return (False,error)
    
    #get
    #得到具体的某个revision的信息
    def getSpreadsheetRevision(self,service, file_id, revision_id):
        try:
            revision = service.revisions().get(fileId=file_id, revisionId=revision_id).execute()
            if revision.get('pinned'):
                print 'This revision is pinned'
            return (True,revision)
        except Exception, e:
            error = 'An error occurred when getRevision'
            return (False,error)
    
    #delete
    #patch
    #update
    ###############revisions相关操作 结束###############
    
    ###############files相关操作 开始###############
    #get
    #下载文件
    #export_format目前支持三种。xlsx,csv,pdf
    def downloadSpreadsheet(self,service,file_id,export_format):
        try:
            response = service.files().get(fileId=file_id).execute()
            download_url = response["exportLinks"].values()[0]
            download_url = download_url.split("exportFormat")[0]+"exportFormat="+export_format
            resp, content = service._http.request(download_url)#resp是该文件的一些信息
            if resp.status == 200:
                return (True,content)
            else:
                return (False,'Error. Status code is not 200.')
        except Exception, e:
            error = 'An error occurred when downloadFile'
            return (False,error)
    
    #insert
    #上传spreadsheet
    #parent_id: Parent folder's ID
    #mime_type: MIME type of the file to insert.
    def uploadSpreadsheet(self,service, title, description, parent_id, filename, mime_type='text/csv'):
        media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
        body = {
        'title': title,
        'description': description,
        'mimeType': mime_type
        }
        if parent_id:
            body['parents'] = [{'id': parent_id}]
        try:
            req = service.files().insert(body=body,media_body=media_body)
            req.uri = req.uri + '&convert=true'
            req.execute()
            return (True,'')
        except errors.HttpError, error:
            error = 'An error occured when upload spreadsheet.'
            return (False,error)
    
    #update
    #更新一个文件的内容
    #new_revision: Whether or not to create a new revision for this file.
    def updateContentOfSpreadsheet(self,service, file_id, new_title, new_description,new_filename, new_revision=False, new_mime_type='text/csv'):
        try:
            fileInfo = service.files().get(fileId=file_id).execute()
            fileInfo['title'] = new_title
            fileInfo['description'] = new_description
            fileInfo['mimeType'] = new_mime_type
            media_body = MediaFileUpload(new_filename, mimetype=new_mime_type, resumable=True)
            req = service.files().update(fileId=file_id,body=fileInfo,newRevision=new_revision,media_body=media_body)
            req.uri = req.uri + '&convert=true'
            req.execute()
            return (True,'')
        except errors.HttpError, error:
            error = 'An error occurred when update spreadsheet'
            return (False,error)
    
    #list
    #得到所有文件对象（目录，脚本也算文件）
    #query_filter 过滤条件 如:mimeType = 'application/vnd.google-apps.folder'
    #详细可参考   https://developers.google.com/drive/web/search-parameters
    def getAllSpreadsheetResource(self,service,query_filter):
        fileResourceList = []
        page_token = None#延续令牌，用于逐页浏览页数较多的结果集合。要获取下一页结果，请在上一个响应中将此参数的值设置为“nextPageToken”。
        while True:
            try:
                param = {}
                if page_token:
                    param['pageToken'] = page_token
                if query_filter:
                    param['q'] = query_filter
                files = service.files().list(**param).execute()
                fileList = files['items']
                for i in fileList:
                    fileResourceList.append(i)
                    #fileResourceList.append(i['title'])
                page_token = files.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError, error:
                error = 'An error occurred when retrieve all files.'
                return (False,error)
        return (True,fileResourceList)
    
    #get
    #得到具体的一个文件对象（目录，脚本也算文件）
    def getSpreadsheetResource(self,service,file_id):
        try:
            fileResource = service.files().get(fileId=file_id).execute()
        except errors.HttpError, error:
            error = 'An error occurred when get file resource.'
            return (False,error)
        return (True,fileResource)
    
    #delete
    #删除文件
    def deleteSpreadsheetById(self,service, file_id):
        try:
            service.files().delete(fileId=file_id).execute()
        except Exception, e:
            error = 'An error occurred when delete file'
            return (False,error)
        return (True,'')
    
    #patch
    #copy
    #touch
    #trash
    #untrash
    #watch
    #emptyTrash
    ###############files相关操作 结束###############
    
    ###############children相关操作 开始###############    
    #得到某个文件夹下的所有文件id
    #query_filter 过滤条件   如：query_filter = "modifiedDate < '2014-09-12T12:00:00-08:00' and title contains 'Fianace For Test2'"  
    #详细可参考   https://developers.google.com/drive/web/search-parameters
    def getAllSpreadsheetsIdFromFolder(self,service, folder_id,query_filter):
        fileIdList = []
        page_token = None
        while True:
            try:
                param = {}
                if page_token:
                    param['pageToken'] = page_token
                if query_filter:
                    param['q'] = query_filter
                children = service.children().list(folderId=folder_id, **param).execute()
                for child in children.get('items', []):
                    fileIdList.append(child['id'])
                page_token = children.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError, error:
                error = 'An error occurred when get all files id from folder.'
                return (False,error)
        return (True,fileIdList)
              
    ###############children相关操作 结束###############
    
    ###############permissions相关操作 开始############### 
     
    #为spreadsheet授权    Type, role, and value work together to limit the access appropriately
    #type: The type limits access to a set of users.       The value 'user', 'group', 'domain' or 'default'.
    #value: The value specifies which user of the type can have access.             User or group e-mail address, domain name or None for 'default'
    #role: The role gives these users the ability to do something to the file, like read it             The value 'owner', 'writer' or 'reader'.
    def shareSpreadsheet(self,service, file_id, type, role, value):
        new_permission = {'value': value,'type': type,'role': role}
        try:
            service.permissions().insert(fileId=file_id, body=new_permission).execute()
            return (True,'')
        except errors.HttpError, error:
            error = 'An error occurred when share spreadsheet'
            return (False,error)
  
    ###############permissions相关操作 结束############### 
    
############################Spreadsheet 相关操作 结束############################################

def writeIntoFile(content,fileName,mod='wb'):
        if len(fileName)==0:
            return False
        if len(content)==0:
            return False
        try:
            local_file=open(fileName,mod)
            local_file.write(content)
            local_file.close()
            return True
        except Exception, e:
            print e
            return False
                        
if __name__ == "__main__":
    log_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print 'At ' + log_start_time + ' begin'
    #client_id='1054006892148-cu408dojk3jihluluevcctoi5vf6m35n.apps.googleusercontent.com'
    client_id = '395154129764-apkn3vftlhmovdbmo47i2h374dg5ro3m.apps.googleusercontent.com'
    #client_secret='uiv0X-jbbo10Tm6S7iwzo7l9'
    client_secret = 'geAvNqnY-1Wv0HbiUJLy8r1o'
    oauth2_scope ='https://www.googleapis.com/auth/drive'
    #redirect_uri='http://www.gopivotal.com/'
    redirect_uri = 'https://www.gopivotal.com'
    #storage_file = 'arvin_credentials_file'
    storage_file='success.txt'
    #file_id = '1x2s-ySX5Zu6J76xqleXWoLOZjuV4CTldZipFXaViNDc'
    file_id = '1--oLkqZxJlGadCHeW6p2hoaom3FgH1ILtySqdHhkeYo'
    googledriveutil = GoogleDriveUtil(client_id,client_secret,oauth2_scope,redirect_uri,storage_file)
    service = googledriveutil.getService()
    if service:
        folder_id = '0B3_BXWDJTbTPcTVtTm81R09GdUU'#arvin
        #folder_id = '0B7gDziZGGWm_aFVyd3c4WC1GU3c'#reed
        #query_filter = "modifiedDate < '2014-09-17T00:00:00' and title contains 'Fianace For Test2'"
        #query_filter = "modifiedDate < '2014-09-17T00:00:00'"
        query_filter = ''
        (isSuc,errorMessage) = googledriveutil.getAllSpreadsheetResource(service,query_filter)
        print errorMessage
        #(isSuc,errorMessage) = googledriveutil.getAllSpreadsheetResource(service,'')
        #writeIntoFile(str(errorMessage),'reed.txt')
    else:
        print 'error. Service is none.'
    tm_end=time.strftime( '%Y-%m-%d %H:%M:%S', time.localtime())
    print 'At ' + tm_end + ' end'