#-*- coding: UTF-8 -*-

import lxml.etree
from fileutil import FileUtil

#http://lxml.de/lxmlhtml.html
#http://www.cnblogs.com/descusr/archive/2012/06/20/2557075.html
#http://docs.python-guide.org/en/latest/scenarios/scrape/

    
if __name__=='__main__':
    fileutil = FileUtil()
    content = fileutil.readLocalFile('./example.html')
    page = lxml.etree.HTML(content.decode('UTF-8'), parser=None, base_url=None)


    
    
    
    
    
    
    
    
    
    
    '''
    for image in images:
        imageDict = image.attrib
        try:
            print imageDict['href']
        except Exception, e:
            print 'fail'
    '''
    '''
    buyers = doc.xpath('//div[@title="buyer-name"]/text()')
    prices = doc.xpath('//span[@class="item-price"]/text()')
    print buyers
    print prices
    '''
    
