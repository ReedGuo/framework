#-*- coding: UTF-8 -*-
from PIL import Image,ImageFilter,ImageEnhance,ImageDraw
from commonutil import CommonUtil
commonutil = CommonUtil()
#参考网址：                          http://onlypython.group.iteye.com/group/wiki/1371-python-graphics-library-pil-python-image-library-introduction
#参考网址：                          http://tech.seety.org/python/python_imaging.html
#参考网址：                          http://abruzzi.iteye.com/blog/346498
#参考网址：                          http://abruzzi.iteye.com/blog/342865
#参考网址(生成验证码)：  http://qinxuye.me/article/create-validate-code-image-with-pil/
###############只涉及一张图片####################
#得到图片的宽度和高度
#得到图片格式
#得到图片模式
#截图
#旋转图片
#分离图片的通道
#重定义图片尺寸
#增强图片
#转换图片模式
#保存图片
#模糊图片
#画一张新图像
#绘制干扰线
#绘制干扰点
#图片扭曲（用于验证码）
#生成验证码

###############涉及多张图片####################
#合成图片
#层叠图片
#将一个图片写入到原图片的透明通道中，而不影响原图片的正常显示


class ImageUtil:
    def __init__(self,imageName):
        self.imageName = imageName
    
    def getImageObject(self):
        self.img = Image.open(self.imageName)
        self.img.load()#PIL is sometimes 'lazy' and 'forgets' to load after opening
        return self.img
    
    ###############只涉及一张图片####################
    #得到图片的宽度和高度
    def getImageSize(self,img):
        width = img.size[0]
        height = img.size[1]
        print 'width ',width,'height',height
        
    #得到图片格式
    #即使把jpeg扩展名重命名为png扩展名，也是jpeg格式。
    #常用的格式为JPEG,PNG,GIF
    def getImageFormat(self,img):
        print img.format
    
    
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
    def getImageMode(self,img):
        print img.mode

    #截图
    #比如，截一个70*20像素的图片
    def cutImage(self,img):
        box = (10,30,80,50)#设置要拷贝的区域。box变量是一个四元组(左，上，右，下)。  
        region = img.crop(box)
        return region
 
    #旋转图片
    #逆时针旋转90° = 0   逆时针旋转180° = 1   逆时针旋转270° = 2左右翻转 = 3   上下翻转 = 4
    #用rotate方法会出现黑边，而transpose方法不会
    def rotateImage(self,img,rotateMode=0):
        if rotateMode==0:
            #out = img.rotate(90,Image.BILINEAR)#逆时针旋转90度
            out = img.transpose(Image.ROTATE_90)
        elif rotateMode==1:
            #out = img.rotate(180,Image.BILINEAR)
            out = img.transpose(Image.ROTATE_180)
        elif rotateMode==2:
            #out = img.rotate(270,Image.BILINEAR)
            out = img.transpose(Image.ROTATE_270)
        elif rotateMode==3:
            out = img.transpose(Image.FLIP_LEFT_RIGHT) 
        elif rotateMode==4:
            out = img.transpose(Image.FLIP_TOP_BOTTOM) 
        return out
    
    #分离图片的通道
    #每一个RGB都是由三个通道的灰度图叠加的
    def separateImage(self,img):
        r,g,b = img.split()#分割成三个通道
        out = Image.merge("RGB", (b, g, r))#将b,r两个通道进行翻转。
        return out
    
    #重定义图片尺寸
    def resizeImage(self,img,width):
        originalWidth = img.size[0]
        originalHeight = img.size[1]
        ratio = float(originalHeight)/originalWidth
        height = int(width * ratio)
        out = img.resize((width, height),Image.BILINEAR)
        return out
    
    #增强图片
    def enhanceImage(self,img):
        out = img.point(lambda i : i * 1.2)#注意这里用到一个匿名函数(那个可以把i的1.2倍返回的函数)
        return out
    
    #转换图片模式
    def transferImageMode(self,img):
        out = img.convert("RGBA")
        print out.mode
        
    #保存图片
    #只是更改了一下扩展名，并没有改变图片模式
    def saveImage(self,img,newImageName):
        img.save(newImageName)
    
    #模糊图片
    #PIL 中支援的濾鏡名稱，目前有：CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
    def blurImage(self,img,blueCount=1):
        tempImg = img
        for i in range(blueCount):
            tempImg = tempImg.filter(ImageFilter.BLUR)
        return tempImg
    
    #画一张新图像
    #mode 模式
    #size 画布大小
    #bgColor 背景色
    #fgColor 前景色
    def drawNewImage(self,mode,size,bgColor,fgColor):
        img = Image.new(mode, size,bgColor)#创建宽400高300的画布
        draw = ImageDraw.Draw(img)
        '''
        #画两条线
        draw.line((0, 0) + im.size, fill=255)#画了一条对角线
        draw.line((0, im.size[1], im.size[0], 0), fill=255) 
        '''
        #写一个单词
        draw.ink = fgColor[0] + fgColor[1]*256 + fgColor[2]*256*256
        draw.text( (20,20), "Reed Guo")
        return img,draw
    
    #绘制干扰线
    #参数 lineNum 干扰线的条数
    def generateRandomLines(self,lineNum,imageSize,draw,*fgColor):
        for i in range(lineNum):
            beginCoord = (commonutil.generateRandomNumber(0,imageSize[0]), commonutil.generateRandomNumber(0,imageSize[1]))# 起始点
            endCoord = (commonutil.generateRandomNumber(0,imageSize[0]), commonutil.generateRandomNumber(0,imageSize[1]))#结束点
            draw.line([beginCoord, endCoord], fill=fgColor)
            
    #绘制干扰点
    def generateRandomPoints(self):
        chance = min(100, max(0, int(point_chance))) # 大小限制在[0, 100]
         
        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))
                    
    #图片扭曲（用于验证码）
    def warpImage(self):
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲
     
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）
    
    #生成验证码
    def createValidateImage(self):
        pass    
        
        
        
        
        
        
        
        
        
        
    ###############涉及多张图片####################
    
    #合成图片
    def composeImage(self,baseImageName,upperImageName):
        baseIm = Image.open(baseImageName)
        baseIm.load()
        upperImage = Image.open(upperImageName)
        upperImage.load()
        box = (10,10,50,50)#设置要粘贴的区域
        region = upperImage.crop(box)
        baseIm.paste(region,box)
        return baseIm
            
    
    #层叠图片
    #alpha是一个介于[0,1]的浮点数，如果为0，效果为img1，如果为1.0，效果为img2
    #两张图片大小必须相同，模式更要相似
    def blendImage(self,img1Name,img2Name,alpha):
        img1 = Image.open(img1Name)
        img2 = Image.open(img2Name)
        out = Image.blend(img1, img2, alpha)
        return out
    
    #将一个图片写入到原图片的透明通道中，而不影响原图片的正常显示(与原图尺寸相同)
    #可以用于信息隐藏哦。当然，前提是原始图片有透明通道
    def hideInfoInImage(self,baseImgName,hideImgName):
        baseImg = Image.open(baseImgName)
        hideImg = Image.open(hideImgName)
        if hideImg.mode != "L" and hideImg.mode != "1":  
            hideImg = hideImg.convert("L")  
        baseImg.putalpha(hideImg)
        return baseImg
    
    
if __name__=='__main__':
    #imageName = 'E:/project/reed_framework/src/utils/ppu.gif'
    imageName = 'E:/project/reed_framework/src/utils/at.jpg'
    #imageName = 'E:/project/reed_framework/src/utils/xiaowei.png'
    imageutil = ImageUtil(imageName)
    img1Name = 'E:/project/reed_framework/src/utils/at.jpg'
    img2Name = 'E:/project/reed_framework/src/utils/Finra_logo.jpg'
    #imageutil.blendImage(img1Name,img2Name,0.8,'luwei.jpg')
    #imageutil.hideInfoInImage(img2Name,'weiwei.png')
    #imageutil.blurImage('woaiweiwei.jpg')
    imageutil.drawNewImage('RGB',(120,40),(125,0,0),(0,0,255),'xiaoluwei.gif')
