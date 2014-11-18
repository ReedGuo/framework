#-*- coding: UTF-8 -*-
from berkeleydb import *

class CrawlerExtendQueue:
    def __init__(self):
        self.unVisitedUrlQueue = QueueDB()#TODO queue
        self.visitedUrlSet = VisitedDB()#已经访问过的hash set
        
        
    #从未访问url队列中取出一个url
    def popUrl(self):
        return self.unVisitedUrlQueue.popUrl()
    
    #将一个url添加到未访问url 队列中
    def pushUrls(self,url_list):
        urls = self.visitedUrlSet.getUniqueUrlList(url_list)
        if urls:
            self.unVisitedUrlQueue.pushUrls(urls)
    
    #已经访问过的url 数目
    def getCountOfVisitedUrl(self):
        all_url_count = self.visitedUrlSet.getCount()
        url_inside_queue_count = self.unVisitedUrlQueue.getCount()
        return (all_url_count - url_inside_queue_count)
    
    #还没有访问过的url 数据
    def getCountOfUnvisitedUrl(self):
        return self.unVisitedUrlQueue.getCount()
    
    #未访问url 队列是否为空
    def isUnvisitedQueueEmpty(self):
        return self.unVisitedUrlQueue.getCount()==0




if __name__ == "__main__":
    obj = CrawlerExtendQueue()
    obj.pushUrls(['www.godogle.com','www.yahoo.com'])
    print obj.getCountOfUnvisitedUrl()
    print obj.popUrl()
    print obj.getCountOfVisitedUrl()
    print obj.getCountOfUnvisitedUrl()
