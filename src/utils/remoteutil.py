#-*- coding: UTF-8 -*-
import os,paramiko
#########操作方法#######
#把文件或目录scp到远程机器 
#把远程机器的文件或目录scp到本地
#在远程服务器上执行命令  


class ScpUtil:
    def __init__(self,scpIp,scpUser,scpPassword):
        self.scpIp = scpIp
        self.scpUser = scpUser
        self.scpPassword = scpPassword

    #把文件或目录scp到远程机器   
    #参数：
    #localFile:带路径的文件名（只scp单个文件）
    #localCatalogue 目录名（把目录低下的所有文件都scp过去）
    #remoteFilePath保存文件的路径
    #scp语法：scp /usr/home/reed/test/aaa.txt gpadmin@10.110.123.43/usr/home/reed/aaa.txt
    def scpToRemoteMachine(self,remoteFilePath,localFile='', localCatalogue = ''):
        if localFile and localCatalogue:
            print 'SCP parameters are wrong.'
        t = paramiko.Transport((self.scpIp,22))
        t.connect(username = self.scpUser, password = self.scpPassword)
        sftp = paramiko.SFTPClient.from_transport(t)
        if localFile:
            scpInfo="scp %s %s@%s:%s" % (localFile,self.scpUser,self.scpIp,remoteFilePath)
            print scpInfo
            basename=os.path.basename(localFile)#文件的不带路径的名字
            sftp.put(localFile,remoteFilePath+'/'+basename)
        elif localCatalogue:
            from fileutil import FileUtil
            fileutil = FileUtil()
            scpInfo="scp %s/* %s@%s:%s" % (localCatalogue,self.scpUser,self.scpIp,remoteFilePath)
            print scpInfo
            files=os.listdir(localCatalogue)
            for eachFile in files:
                if fileutil.isExistFile(eachFile):
                    sftp.put(os.path.join(localCatalogue,eachFile),os.path.join(remoteFilePath,eachFile))
                else:
                    print eachFile + ' is not a file.'
        t.close()
        
    #把远程机器的文件或目录scp到本地  
    #localFilePath  下载到本地的路径
    #remoteFile 远程文件
    #remoteCatalogue 远程目录
    def scpToLocalMachine(self,localFilePath,remoteFile='',remoteCatalogue=''):
        if remoteFile and remoteCatalogue:
            print 'SCP parameters are wrong.'
        t = paramiko.Transport((self.scpIp,22))
        t.connect(username = self.scpUser, password = self.scpPassword)
        sftp = paramiko.SFTPClient.from_transport(t)
        if remoteFile:
            scpInfo="scp %s@%s:%s %s" % (self.scpUser,self.scpIp,remoteFile,localFilePath)
            print scpInfo
            basename=os.path.basename(remoteFile)
            localFile = localFilePath + '/' + basename
            sftp.get(remoteFile,localFile)
        elif remoteCatalogue:
            scpInfo="scp %s@%s:%s/* %s" % (self.scpUser,self.scpIp,remoteCatalogue,localFilePath)
            print scpInfo
            files=sftp.listdir(remoteCatalogue)
            for eachFile in files:
                sftp.get(os.path.join(remoteCatalogue,eachFile),os.path.join(localFilePath,eachFile))
        t.close()
        
    #在远程服务器上执行命令  
    #参数： sshCmd要在远程机器上执行的命令
    def sshCmdOnRemoteMachine(self,sshCmd):
        sshInfo=self.scpUser + '@' + self.scpIp + ' executes this command   :  '+sshCmd
        print sshInfo
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.scpIp,username = self.scpUser,password=self.scpPassword)
        stdin,stdout,stderr = ssh.exec_command(sshCmd)
        res=stdout.read()
        err=stderr.read()
        if err:
            print err
        ssh.close()
        return res


if __name__=='__main__':
    #put a file named /home/gpadmin/reed/scptest/a1.txt at 10.110.123.43 to 10.110.123.44 /home/gpadmin/reed/scptest
    scputil = ScpUtil('10.110.123.44','gpadmin','changeme')
    scputil.sshCmdOnRemoteMachine('rm -rf /home/gpadmin/reed/scptest/*')
 
