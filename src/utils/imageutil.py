#-*- coding: UTF-8 -*-
from PIL import Image,ImageFilter,ImageEnhance
#参考网址：http://onlypython.group.iteye.com/group/wiki/1371-python-graphics-library-pil-python-image-library-introduction
#参考网址：
###############相关操作##############
#得到图片的宽度和高度
#得到图片格式
#得到图片模式
#截图
#旋转图片
#合成图片
#分离图片的通道
#重定义图片尺寸
#增强图片
#层叠图片
#转换图片模式
#将一个图片写入到原图片的透明通道中，而不影响原图片的正常显示

class ImageUtil:
    def __init__(self,imageName):
        self.im = Image.open(imageName)
        self.im.load()#PIL is sometimes 'lazy' and 'forgets' to load after opening
        self.imageName = imageName
    
    #得到图片的宽度和高度
    def getImageSize(self):
        width = self.im.size[0]
        height = self.im.size[1]
        print 'width ',width,'height',height
        
    #得到图片格式
    #即使把jpeg扩展名重命名为png扩展名，也是jpeg格式。
    #常用的格式为JPEG,PNG,GIF
    def getImageFormat(self):
        print self.im.format
    
    
    #得到图片模式
    #1     1位像素，黑和白，存成8位的像素
    #L     8位像素，黑白
    #jpg图片是RGB(3×8位像素，真彩)
    #png图片是RGBA(有时也写成ARGB。分别表示红、绿、蓝和 Alpha.The alpha channel is normally used as an opacity channel.4×8位像素，真彩+透明通道)
    #gif图片是P(8位像素，使用调色板映射到任何其他模式)
    #CMYK(4×8位像素，颜色隔离)
    #YCbCr(3×8位像素，彩色视频格式)
    #I(32位整型像素)
    #F(32位浮点型像素)
    def getImageMode(self):
        print self.im.mode

    #截图
    #比如，截一个70*20像素的图片
    def cutImage(self,newImageName):
        box = (10,30,80,50)#设置要拷贝的区域。box变量是一个四元组(左，上，右，下)。  
        region = self.im.crop(box)
        region.save(newImageName)
 
    #旋转图片
    #逆时针旋转90° = 0   逆时针旋转180° = 1   逆时针旋转270° = 2左右翻转 = 3   上下翻转 = 4
    def rotateImage(self,newImageName,rotateMode=1):
        if rotateMode==0:
            out = self.im.rotate(90)#逆时针旋转90度
        elif rotateMode==1:
            out = self.im.rotate(180)
        elif rotateMode==2:
            out = self.im.rotate(270)
        elif rotateMode==3:
            out = self.im.transpose(Image.FLIP_LEFT_RIGHT) 
        elif rotateMode==4:
            out = self.im.transpose(Image.FLIP_TOP_BOTTOM) 
        out.save(newImageName)
    
    #合成图片
    def composeImage(self,baseImage,upperImage):
        baseIm = Image.open(baseImage)
        baseIm.load()
        upperImage = Image.open(upperImage)
        upperImage.load()
        box = (10,10,50,50)#设置要粘贴的区域
        region = upperImage.crop(box)
        baseIm.paste(region,box)
        baseIm.save(baseImage)
            
    #分离图片的通道
    #每一个RGB都是由三个通道的灰度图叠加的
    def separateImage(self,newImageName):
        r,g,b = self.im.split()#分割成三个通道
        out = Image.merge("RGB", (b, g, r))#将b,r两个通道进行翻转。
        out.save(newImageName)
    
    #重定义图片尺寸
    def resizeImage(self,width,height,newImageName):
        out = self.im.resize((width, height))#resize成128*128像素大小。 
        out.save(newImageName)
    
    #增强图片
    def enhanceImage(self,newImageName):
        out = self.im.point(lambda i : i * 1.2)#注意这里用到一个匿名函数(那个可以把i的1.2倍返回的函数)
        out.save(newImageName)
       
    #层叠图片
    #alpha是一个介于[0,1]的浮点数，如果为0，效果为img1，如果为1.0，效果为img2
    #两张图片大小必须相同，模式更要相似
    def blendImage(self,img1Name,img2Name,alpha,newImageName):
        img1 = Image.open(img1Name)
        img2 = Image.open(img2Name)
        out = Image.blend(img1, img2, alpha)
        out.save(newImageName)
    
    #转换图片模式
    def transferImageMode(self):
        out = self.im.convert("RGBA")
        print out.mode
        
    #将一个图片写入到原图片的透明通道中，而不影响原图片的正常显示(与原图尺寸相同)
    #可以用于信息隐藏哦。当然，前提是原始图片有透明通道
    def hideInfoInImage(self,hideImgName,newImageName):
        hideImg = Image.open(hideImgName)
        if hideImg.mode != "L" and hideImg.mode != "1":  
            hideImg = hideImg.convert("L")  
        self.im.putalpha(hideImg)
        self.im.save(newImageName)
    
    
    
if __name__=='__main__':
    #imageName = 'E:/project/reed_framework/src/utils/ppu.gif'
    imageName = 'E:/project/reed_framework/src/utils/at.jpg'
    #imageName = 'E:/project/reed_framework/src/utils/globe.png'
    imageutil = ImageUtil(imageName)
    img1Name = 'E:/project/reed_framework/src/utils/at.jpg'
    img2Name = 'E:/project/reed_framework/src/utils/Finra_logo.jpg'
    #imageutil.blendImage(img1Name,img2Name,0.8,'luwei.jpg')
    imageutil.hideInfoInImage(img2Name,'weiwei.png')
