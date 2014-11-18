#-*- coding: UTF-8 -*-

############################获取参数############################################################
import sys
from optparse import OptionParser 

parser = OptionParser() 

#加入选项
#action是有store，store_true，store_false等，默认是’store ‘，表示将命令行参数值保存在 options 对象里。dest是存储的变量，default是缺省值，help是帮助提示
parser.add_option("-s", "", action="store", 
                  dest="SqlFile", 
                  default=False, 
                  help="A file stored sql statement") 

parser.add_option("-d", "", action="store", 
                  dest="DownFile", 
                  default=False, 
                  help="Download the file path stored") 

parser.add_option("-v", action="store_true", 
                  dest="Reed", 
                  default=False, 
                  help="Reed is true or false") 

(options, args) = parser.parse_args()
Errparser="Please enter the full parameter such as:\n\t"+' ./obiee -s /home/InstallBase.sql -d /home/InstallBase_%Y%m%d.csv'
if not options.SqlFile or not options.DownFile:
    print Errparser
    sys.exit()

print options.SqlFile
print options.DownFile
print options.Reed





##################################获取配置文件######################################################
from configRead import Config
x = Config('config.ini')
commonConfig = x.configByItem('COMMON')
dsConfig = x.configByItem("EMC")