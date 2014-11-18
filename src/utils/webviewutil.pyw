#-*- coding: UTF-8 -*-
import sys,sip
sip.setapi('QString',2)
from PyQt4 import QtCore,QtGui,QtWebKit,QtNetwork

class Browser():
    def __init__(self,urlToVisit):
        self.urlToVisit = urlToVisit
        '''
        QtWebKit provides a Web browser engine that makes it easy to embed content from the World Wide Web into your Qt application. At the same time Web content can be enhanced with native controls.
        QtWebKit provides HTML,XHTML,Scalable Vector Graphics (SVG) documents,CSS, and JavaScript
        
        The QWebView class provides a widget that is used to view and edit web documents.
        QWebView is the main widget component of the QtWebKit web browsing module. It can be used in various applications to display web content live from the Internet.
        '''
        self.webView = QtWebKit.QWebView()
        self.webView.setGeometry(100, 100, 1200, 850)
        #self.webView.setWindowState(QtCore.Qt.WindowMaximized)
        '''To ignore ssl certificate'''
        self.network_manager = QtNetwork.QNetworkAccessManager()#QNetworkAccessManager类允许应用程序发送网络请求和接收网络应答
        self.network_manager.sslErrors.connect(self.onSslErrors)
        '''
        The QWebPage class provides an object to view and edit web documents.
        QWebPage holds a main frame responsible for web content, settings, the history of navigated links and actions. This class can be used, together with QWebFrame, to provide functionality like QWebView in a widget-less environment.
        '''
        self.webPage = self.webView.page()
        self.webPage.setNetworkAccessManager(self.network_manager)#Sets the QNetworkAccessManager manager responsible for serving network requests for this QWebPage.
        
        self.webView.load(QtCore.QUrl(self.urlToVisit))
        '''
        In order to customize the user agent sent by the webkit browser you can override userAgentForUrl 
                    重写userAgentForUrl这个函数    url是参数    return 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
        This function is called when a user agent for HTTP requests is needed.
        '''
        self.webPage.userAgentForUrl=lambda url: 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
        
        self.webPage.setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)#通过接收linkClicked信号来代理链接点击事件
        self.webPage.linkClicked.connect(self.linkClickes)#linkClicked这个信号与linkClickes这个槽关联起来
        '''
        The QWebFrame class represents a frame in a web page.
        QWebFrame represents a frame inside a web page. Each QWebPage object contains at least one frame, the main frame, obtained using QWebPage::mainFrame(). Additional frames will be created for HTML <frame> or <iframe> elements.
        In frame, we can evaluate javascript
        '''
        self.webFrame = self.webPage.mainFrame()#Returns the main frame of the page. The main frame provides access to the hierarchy of sub-frames and is also needed if you want to explicitly render a web page into a given painter.
        url = self.webFrame.url().toString()
        #print 'url is: ' + str(url)
        '''
                    每次执行一个连接，都出发single()这个方法
        '''
        #self.webView.loadFinished.connect(self.callsSlot)#This signal is emitted when a load of the page is finished. ok will indicate whether the load was successful or any error occurred. 这句代码的另外一种写法是   QtCore.QObject.connect(self.webView,QtCore.SIGNAL("loadFinished(bool)"),self.callsSlot)
        self.callsSlot()
        self.webView.show()
        
    #linkClicked这个信号对应的槽
    #url是QUrl类型
    def linkClickes(self, url):
        self.webView.load(url)
    
    #忽略 ssl certificate
    def onSslErrors(self, reply, errors):
        url = unicode(reply.url().toString())
        reply.ignoreSslErrors()
        print "SSL certificate error ignored: %s" % url
    
    
    #loadFinished（页面完全加载后发出）这个信号对应的槽
    def callsSlot(self):
        '''
        The QTimer class provides repetitive and single-shot timers.
        '''
        self.ctimer =  QtCore.QTimer()
        self.timesleep=6000#以毫秒为单位
        self.ctimer.singleShot(self.timesleep,self.loginTaobao)


    #登录淘宝（提交表单登录）
    def loginTaobao(self):
        js = '''
        function initView()
        {
            alert(document.readyState)
       }
       initView()
        '''
        js="frm=document.forms[0];frm.TPL_username.value='15010658102';frm.TPL_password.value='fen';frm.submit();"
        self.webFrame.evaluateJavaScript(js)
        
    #登录淘宝（点击按钮登录）
    def loginTaobao2(self):
        js="frm=document.forms[0];var count=0;for (count=0;count<=5;count++){frm.TPL_username.value='15010658102';frm.TPL_password.value='feng'+count;document.getElementById('J_SubmitStatic').click();alert('hehe');} "
        self.webFrame.evaluateJavaScript(js)
    
    #获取元素的位置
    def getElementLocation(self):
        #如果引入了jquery，就这样获取：
        #elementWidth = int(self.webFrame.evaluateJavaScript('''$("#J_Promo").width()''').toString())
        #elementHeight = int(self.webFrame.evaluateJavaScript('''$("#J_Promo").height()''').toString())
        #elementLeft = int(self.webFrame.evaluateJavaScript('''$("#J_Promo").offset().left''').toString())
        #elementTop = int(self.webFrame.evaluateJavaScript('''$("#J_Promo").offset().top''').toString())
        
        #如果没有引入jquery，就这样获取：
        elementWidth = int(self.webFrame.evaluateJavaScript('''document.getElementById("J_Promo").offsetWidth''').toString())
        elementHeight = int(self.webFrame.evaluateJavaScript('''document.getElementById("J_Promo").offsetHeight''').toString())
        elementLeft = int(self.webFrame.evaluateJavaScript('''document.getElementById("J_Promo").offsetTop''').toString())
        elementTop = int(self.webFrame.evaluateJavaScript('''document.getElementById("J_Promo").offsetLeft''').toString())
        #box=(elementLeft,elementTop,elementLeft+elementWidth,elementTop+elementHeight)
        print elementWidth
        print elementHeight
        print elementLeft
        print elementTop
           
    #模拟鼠标点击超链接
    def mouseClick(self):
        aa = self.webFrame.findAllElements("a[href]")
        a = aa.at(10)
        a.evaluateJavaScript("var evObj = document.createEvent('MouseEvents');evObj.initEvent( 'click', true, true );this.dispatchEvent(evObj);")
    
    #搜索商品
    def searchGood(self):
        js = '''
        fm = document.getElementById("J_TSearchForm");fm.q.value='MCM';fm.submit();
        '''
        self.webFrame.evaluateJavaScript(js)
        
    #得到网页缩略图
    def getThumbnail(self):
        size = self.webFrame.contentsSize()#This property holds the size of the contents in this frame.
        contentWidth = size.width()
        contentHeight = size.height()
        
        '''
        How to get a thumbnail of a page
        1. We begin by setting the viewportSize 
        2. then we instantiate a QImage object, image, with the same size as our viewportSize. 
        3. This image is then sent as a parameter to painter. 
        4. Next, we render the contents of the main frame and its subframes into painter. 
        5. Finally, we save the scaled image.
        '''
        self.webPage.setViewportSize(size)
                
        '''
        The QImage class provides a hardware-independent image representation that allows direct access to the pixel data, and can be used as a paint device.
        '''
        image   = QtGui.QImage(QtCore.QSize(contentWidth,contentHeight), QtGui.QImage.Format_ARGB32)#The image is stored using a 32-bit ARGB format (0xAARRGGBB).
        '''
        The QPainter class performs low-level painting on widgets and other paint devices.
        QPainter provides highly optimized functions to do most of the drawing GUI programs require. It can draw everything from simple lines to complex shapes like pies and chords. It can also draw aligned text and pixmaps. Normally, it draws in a "natural" coordinate system, but it can also do view and world transformation. QPainter can operate on any object that inherits the QPaintDevice class.
        '''
        painter = QtGui.QPainter(image)
        '''The render() function shows how we can paint a thumbnail using a QWebPage object.'''
        self.webFrame.render(painter)#Render the frame into painter clipping to clip.
        painter.end()#Ends painting. Any resources used while painting are released. You don't normally need to call this since it is called by the destructor.
        image.save("yuanyuan2.jpg")
        self.quit()
     
    #退出程序    
    def quit(self):
        self.webView.thread().exit()
        self.webView.thread().quit()
        self.webView.close()
        self.webView.destroy()
        sys.exit()
        

        
app = QtGui.QApplication(sys.argv)
urlToVisit = 'https://login.taobao.com/member/login.jhtml'
s=Browser(urlToVisit)
sys.exit(app.exec_())
