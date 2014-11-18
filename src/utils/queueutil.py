#-*- coding: UTF-8 -*-
from utils.commonutil import *
import Queue


class CrawlerQueue:

    #构造函数    初始化未访问的url队列，已访问的url set
    def __init__(self):
        self.unVisitedUrlQueue = Queue.Queue()#未访问url队列
        self.visitedUrlSet = set()#已访问url集合
    
    
    #从未访问url队列中取出一个url
    def popUrl(self):
        return self.unVisitedUrlQueue.get()
    
    #将一个url添加到未访问url 队列中
    def pushUrls(self,url_list):
        urls = self.getUniqueUrlList(url_list)
        if urls:
            for url in urls:
                self.unVisitedUrlQueue.put(url)
                
            
    
    #已经访问过的url 数目
    def getCountOfVisitedUrl(self):
        all_url_count = len(self.visitedUrlSet)
        url_inside_queue_count = self.unVisitedUrlQueue.qsize()
        return (all_url_count - url_inside_queue_count)
    
    #还没有访问过的url 数据
    def getCountOfUnvisitedUrl(self):
        return self.unVisitedUrlQueue.qsize()
    
    #未访问url 队列是否为空
    def isUnvisitedQueueEmpty(self):
        return self.unVisitedUrlQueue.empty()

    #得到不重复的url
    def getUniqueUrlList(self, url_list):
        urls = []
        for url in url_list:
            if md5Str(url) not in self.visitedUrlSet:
                urls.append(url)
                self.visitedUrlSet.add(md5Str(url))
        return urls
    
    
if __name__=='__main__':

    obj = CrawlerQueue()
    obj.pushUrls(['www.baidu.com','www.google.com'])
    print obj.getCountOfUnvisitedUrl()
    print obj.popUrl()
    print obj.popUrl()
    print obj.getCountOfVisitedUrl()
    print obj.getCountOfUnvisitedUrl()
    
    
