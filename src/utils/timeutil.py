#-*- coding: UTF-8 -*-
import datetime,time,re

class TimeUtil:
    def __init__(self):
        pass
    #当前时间（精确到秒）距离1970-01-01的秒数
    def getCurrentIntTime(self):
        t=time.localtime()
        s = datetime.datetime(t[0],t[1],t[2],t[3],t[4],t[5])
        return int(time.mktime(s.timetuple()))
    
    
    #把ISO 8601 Standard时间转换成格式化的时间
    #参数 timeStr  2014-09-10T09: 49: 54.270Z
    def changeTimeFormat(self,timeStr):
        tIndex = timeStr.find('T')
        dateStr = timeStr[:tIndex]
        hourStr = timeStr[tIndex+1:]
        hIndex = hourStr.rfind('.')
        hourStr = hourStr[:hIndex]
        hourStr = hourStr.replace(' ', '')
        timeStr = dateStr + ' ' + hourStr + '+0'
        return timeStr

    #当前日期（精确到天）距离1970-01-01的秒数
    def getCurrentIntDate(self):
        t=time.localtime()
        s = datetime.datetime(t[0],t[1],t[2])
        return int(time.mktime(s.timetuple()))
    
    
    #根据秒数得到时间/日期的字符串
    #参数 seconds: 秒数
    def secondsToTimeStr(self,seconds,format='%Y-%m-%d %H:%M:%S'):
        try:
            return time.strftime(format, time.localtime(seconds))
        except:
            return False
        
    
    #将时间/日期的字符串转换成秒 
    #参数 str:时间字符串 如2014-12-10 13:20:45
    def timeStrToIntTime(self,timeStr):
        try:
            estr=re.compile(r"(\d{2,4})[^\d]+(\d{1,2})[^\d]+(\d{1,2})[^\d]+(\d{1,2})[^\d]+(\d{1,2})[^\d]+(\d{1,2})").findall(timeStr)
            if len(estr)==0:
                estr=re.compile(r"(\d{2,4})[^\d]+(\d{1,2})[^\d]+(\d{1,2})").findall(timeStr)
            estr=estr[0]
            if len(estr)==3:
                estr=estr[0],estr[1],estr[2],0,0,0
            s = datetime.datetime(int(estr[0]),int(estr[1]),int(estr[2]),int(estr[3]),int(estr[4]),int(estr[5]))
            strtime=time.mktime(s.timetuple())#convert a time tuple in local time to seconds since the Epoch
            return int(strtime)
        except:
            return False
    
    
    #根据zone得到新的时间。 
    #参数：timeStr  时间字符串
    def getTimeByNewZone(self,timeStr,formart='%Y-%m-%d %H:%M:%S',newZone=8):
        timeStr = timeStr.strip()
        if len(timeStr)<=19:#说明时间的字符串没有时区
            return timeStr
        newZone = int(newZone)#将+8变为8  以小时为单位
        oldZone = int(timeStr[19:])
        inttime=self.timeStrToIntTime(timeStr)
        subtime=(newZone - oldZone)*3600
        finalTime=inttime+subtime
        return time.strftime(formart, time.localtime(finalTime))
    
    
    #得到邮件接收时间
    def getEmailReceiveTime(self,timeObj):
        CST0_FORMAT = '%a, %d %b %Y %H:%M:%S -0700 (PDT)'
        dt1=datetime.datetime.strptime(timeObj, CST0_FORMAT)
        dt=time.strptime(str(dt1),'%Y-%m-%d %H:%M:%S')
        dt=time.mktime(datetime.datetime(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5]).timetuple())
        dt=time.strftime('%m/%d/%Y %I:%M:%S %p',time.gmtime(float(dt)))    
        return dt

    #得到周日的日期
    def getSundayDateWeeksAgo(self,weeksago=1,format='%Y-%m-%d'):
        week = int(time.strftime("%w"))
        return time.strftime(format,time.localtime(time.time()-(86400*week)-7*86400*(weeksago-1)))

if __name__=='__main__':
    timeutil = TimeUtil()
    #print timeutil.secondsToTimeStr(1409726252742)
    print timeutil.getSundayDateWeeksAgo()

