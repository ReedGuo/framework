#-*- coding: UTF-8 -*-

import ConfigParser

class Config:
    
    def __init__(self, configName):
        self.configName = configName
        self.cp = ConfigParser.ConfigParser()
        self.cp.read(configName)


#############如果只有一个配置，就叫Config########################
    def config(self):
        config = {}
        items = self.cp.items("Config")
        for item in items:
            config[item[0]] = item[1]
        return config
    
    #修改配置文件的值
    def set(self, key, value):
        self.cp.set("Config", key, value)
        self.cp.write(open(self.configName, 'w'))
      

############如果有多个配置，就要提供名字############
    def configByItem(self, itemName):
        config = {}#要返回的字典
        items = self.cp.items(itemName)#该配置下的所有项
        for item in items:#item[0]是字段名，item[1]是字段值
            config[item[0]] = item[1]
        return config
    
    #修改配置文件的值
    def setByItem(self, itemName, key, value):
        self.cp.set(itemName, key, value)
        self.cp.write(open(self.configName, 'w'))


if __name__ == '__main__':
    x = Config('config.ini')
    commonConfig = x.configByItem('COMMON')
    x.setByItem('COMMON','retry','3')