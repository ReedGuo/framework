#-*- coding: UTF-8 -*-
import sys
import re
import time
#from database import QueueDB, WebpageDB, DuplCheckDB
#from downloader import DownloadManager
from webpage import WebPage

#爬虫框架主类
class Crawler():

    def __init__(self):
        self.downloader = DownloadManager()#下载网页的对象
        self.webpage = None#解析页面的对象
        self.initDatabase()
        self.rules = {}

    #初始化数据库
    def initDatabase(self):
        self.queue = QueueDB()#TODO 表
        self.webpagedb = WebpageDB()
        self.duplcheck = DuplCheckDB()
    
    #增加种子url
    #参数： links   url 列表
    def addSeeds(self, links):
        new_links = self.duplcheck.filterDuplUrls(links)#把重复的url过滤掉
        self.duplcheck.addUrls(new_links)#已经访问过的url
        self.queue.pushUrls(new_links)#向todo表中增加url
    
    def addRules(self, rules):
        self.rules = {}
        for url, inurls in rules.items():
            reurl = re.compile(url)
            repatn = []
            for u in inurls:
                repatn.append(re.compile(u))
            self.rules[reurl] = repatn

    def get_patterns_from_rules(self,url):
        patns = []
        for purl,ru in self.rules.items():
            if purl.match(url)!= None:
                patns.extend(ru)
        return list(set(patns))

    #开始执行
    def start(self):
        while 1:
            url = self.queue.popUrl()
            print url
            if url == None:
                print "crawling task is done."
                break
            error_msg, url, redirected_url, html = self.downloader.download(url)
            #print error_msg, url, redirected_url, html
            if html !=None:
                self.webpagedb.storeHtmlToDb(url,html)#把网页存储起来
                
                self.webpage = WebPage(url,html)#开始解析网页
                self.webpage.parseLinks()#得到全部的超链接
                ruptn = self.get_patterns_from_rules(url)
                print ruptn
                links = self.webpage.filter_links(tags = ['a'], patterns= ruptn)#得到None
                if links:
                    self.addSeeds(links)
            self.mysleep(3)#休息一下再继续爬

    def mysleep(self, n):
        for i in range(1,n+1):
            time.sleep(1)
            print "sleep",i,"of",n



if __name__ == "__main__":
    
    mycrawler = Crawler()
    mycrawler.addSeeds(['http://www.livejournal.com/'])
    rules = {'^(http://.+livejournal\.com)(.+)$':['^(http:)//((?!www).*)(\.livejournal\.com.+)$']}
    mycrawler.addRules(rules)
    mycrawler.start()
    

