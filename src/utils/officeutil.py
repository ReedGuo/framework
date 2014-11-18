#-*- coding: UTF-8 -*-

#参考         http://blog.csdn.net/lzl001/article/details/8435048
#参考         http://3y.uu456.com/bp-d6sd36728e99s1e79b892737-1.html

from win32com.client import Dispatch
import csv

tableRow = 18#表格为18行
tableCol = 7#表格为7列

#把多个字符串生成list
def createValueList(str1,str2,str3,str4,str5,str6,str7):
    valueList = []
    valueList.append(str1)
    valueList.append(str2)
    valueList.append(str3)
    valueList.append(str4)
    valueList.append(str5)
    valueList.append(str6)
    valueList.append(str7)
    return valueList

#处理老师信息
def createTableFixedCellText(teacher_type):
    cellsTextList = []
    daikeSelect = u'□'
    youerSelect = u'□'
    dengjiSelect = u'□'
    if teacher_type=='daike':
        daikeSelect = u'□√'
    elif teacher_type=='youer':
        youerSelect = u'□√'
    elif teacher_type=='dengji':
        dengjiSelect = u'□√'
    
    #以下是第一行
    name = u'姓名'
    nameValue = 'valueList_0'
    gender = u'性别'
    genderValue = 'valueList_1'
    birth = u'出生日期'
    birthValue = 'valueList_2'
    photo = u'小二寸近期免冠照片'
    valueList = createValueList(name,nameValue,gender,genderValue,birth,birthValue,photo)
    cellsTextList.append(valueList)
    
    
    #以下是第二行
    teacherTypeTitle = u'类别'
    teacherType = u'农村原民办教师'
    teacherTypeValue = u'□'
    teacherBegin = u'任教起始时间'
    teacherBeginValue = 'valueList_3'
    emptyValue = ''
    emptyValue = ''
    valueList = createValueList(teacherTypeTitle,teacherType,teacherTypeValue,teacherBegin,teacherBeginValue,emptyValue,emptyValue)
    cellsTextList.append(valueList)
    
    #以下是第三行
    emptyValue = ''
    teacherType = u'农村原代课教师'
    teacherTypeValue = daikeSelect
    emptyValue = ''
    emptyValue = ''
    emptyValue = ''
    emptyValue = ''
    valueList = createValueList(emptyValue,teacherType,teacherTypeValue,emptyValue,emptyValue,emptyValue,emptyValue)
    cellsTextList.append(valueList)
    
    #以下是第四行
    emptyValue = ''
    teacherType = u'农村原幼儿教师'
    teacherTypeValue = youerSelect
    teacherEnd = u'离岗时间'
    teacherEndValue = 'valueList_4'
    emptyValue = ''
    emptyValue = ''
    valueList = createValueList(emptyValue,teacherType,teacherTypeValue,teacherEnd,teacherEndValue,emptyValue,emptyValue)
    cellsTextList.append(valueList)
    
    #以下是第五行
    emptyValue = ''
    teacherType = u'85登记造册民师'
    teacherTypeValue = dengjiSelect
    emptyValue = ''
    emptyValue = ''
    emptyValue = ''
    emptyValue = ''
    valueList = createValueList(emptyValue,teacherType,teacherTypeValue,emptyValue,emptyValue,emptyValue,emptyValue)
    cellsTextList.append(valueList)
    
    #以下是第六行
    emptyValue = ''
    teacherType = u'中小学代课教师'
    teacherTypeValue = u'□'
    emptyValue = ''
    emptyValue = ''
    emptyValue = ''
    emptyValue = ''
    valueList = createValueList(emptyValue,teacherType,teacherTypeValue,emptyValue,emptyValue,emptyValue,emptyValue)
    cellsTextList.append(valueList)
    
    #以下是第七行
    familyAddress = u'家庭住址'
    familyAddressValue = 'valueList_5'
    emptyValue = ''
    emptyValue = ''
    telephone = u'联系电话'
    telephoneValue = 'valueList_6'
    emptyValue = ''
    valueList = createValueList(familyAddress,familyAddressValue,emptyValue,emptyValue,telephone,telephoneValue,emptyValue)
    cellsTextList.append(valueList)
    
    #以下是第八行
    identityCard = u'身份证号'
    identityCardValue = 'valueList_7'
    emptyValue = ''
    emptyValue = ''
    residenceType = u'是否农村户口'
    residenceTypeValue = 'valueList_8'
    emptyValue = ''
    valueList = createValueList(identityCard,identityCardValue,emptyValue,emptyValue,residenceType,residenceTypeValue,emptyValue)
    cellsTextList.append(valueList)
    
    #以下是第九行
    experience = u'任教详细经历'
    experienceDate = u'任 教 时 间'
    emptyValue = ''
    originalSchool = u'原 任 教 学 校'
    emptyValue = ''
    evidence = u'证 明 人'
    emptyValue = ''
    valueList = createValueList(experience,experienceDate,emptyValue,originalSchool,emptyValue,evidence,emptyValue)
    cellsTextList.append(valueList)
    
    
    
    #以下是第十行
    emptyValue = ''
    teacherLast = 'valueList_13'
    emptyValue = ''
    originalSchoolValue = 'valueList_14'
    emptyValue = ''
    emptyValue = ''
    emptyValue = ''
    valueList = createValueList(emptyValue,teacherLast,emptyValue,originalSchoolValue,emptyValue,emptyValue,emptyValue)
    cellsTextList.append(valueList)
    #以下是第十一行
    valueList = createValueList('','','','','','','')
    cellsTextList.append(valueList)
    #以下是第十二行
    valueList = createValueList('','','','','','','')
    cellsTextList.append(valueList)
    #以下是第十三行
    valueList = createValueList('','','','','','','')
    cellsTextList.append(valueList)
    
    
    
    
    
    #以下是第十四行
    crime = u'刑事犯罪情况'
    crimeValue = 'valueList_9'
    birthRestrict = u'违反计划 生育情况'
    birthRestrictValue = 'valueList_10'
    assurance = u'养老保险缴纳情况'
    assuranceValue = 'valueList_11'
    emptyValue = ''
    valueList = createValueList(crime,crimeValue,birthRestrict,birthRestrictValue,assurance,assuranceValue,emptyValue)
    cellsTextList.append(valueList)
    
    #以下是第十五行
    totalYears = u'累计任教年限'
    totalYearsValue = 'valueList_12'
    emptyValue = ''
    handPrint = u'本人签字：（手印）        2014年 4月 29 日'
    emptyValue = ''
    emptyValue = ''
    emptyValue = ''
    valueList = createValueList(totalYears,totalYearsValue,emptyValue,handPrint,emptyValue,emptyValue,emptyValue)
    cellsTextList.append(valueList)
    
    #以下是第十六行
    opinion = u'镇、街道认定小组初审意见'
    opinionValue = u'情况属实\r\n\r\n2014年5月1 日\r\n盖章：\r\n\r\n'
    firstResult = u'第一次公示结果'
    secondResult = u'第二次公示结果'
    thirdResult = u'第三次公示结果'
    emptyValue = ''
    emptyValue = ''
    valueList = createValueList(opinion,opinionValue,firstResult,secondResult,thirdResult,emptyValue,emptyValue)
    cellsTextList.append(valueList)
    
    #以下是第十七行
    emptyValue = ''
    emptyValue = ''
    firstResultValue = u'无异议\r\n\r\n2014年5月8日盖章：\r\n\r\n'
    secondResultValue = u'无异议\r\n\r\n2014年5月26日盖章：\r\n\r\n'
    thirdResultValue = u'无异议\r\n\r\n2014年6月18日盖章：\r\n\r\n'
    emptyValue = ''
    emptyValue = ''
    valueList = createValueList(emptyValue,emptyValue,firstResultValue,secondResultValue,thirdResultValue,emptyValue,emptyValue)
    cellsTextList.append(valueList)
    
    #以下是第十八行
    groupOpinion = u'县区专项工作领导小组认定意见'
    groupOpinionValue = u'\r\n\r\n 年  月  日盖章：\r\n\r\n'
    emptyValue = ''
    emptyValue = ''
    emptyValue = ''
    emptyValue = ''
    emptyValue = ''
    valueList = createValueList(groupOpinion,groupOpinionValue,emptyValue,emptyValue,emptyValue,emptyValue,emptyValue)
    cellsTextList.append(valueList)
    
    return cellsTextList
    
    
#读csv
def readCSVFile(fileName,delimiter='\t',quotechar='"'):
    contentList = []
    index = 0
    with open(fileName,'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for row in reader:
            index += 1
            if index == 1:
                continue
            valueList = []
            no = row[0].decode('utf-8')#序号
            profileNo = row[1].decode('utf-8')#档案编号
            name = row[2].decode('utf-8')#姓名
            gender = row[3].decode('utf-8')#性别
            birth = row[4].decode('utf-8')#出生日期
            identityCard = row[5].decode('utf-8')#身份证号
            town = row[6].decode('utf-8')#户口所在地
            townType = row[7].decode('utf-8')#户籍类型
            teacherType = row[8].decode('utf-8')#任教身份
            originalSchool = row[9].decode('utf-8')#原任教学校
            employer = row[10].decode('utf-8')#聘用主体
            teacherBeginEnd = row[11].decode('utf-8')#原任教起止时间
            dateArray = teacherBeginEnd.split('-')
            arrayCount = len(dateArray)
            teacherBegin = dateArray[0]
            teacherEnd = dateArray[arrayCount-1]
            totalYears = row[12].decode('utf-8')#累积任教年限
            teacherAge = row[13].decode('utf-8')#累积教龄
            assurance = row[14].decode('utf-8')#缴纳养老保险情况
            birthRestrict = row[15].decode('utf-8')#违反计划生育情况
            crime = row[16].decode('utf-8')#刑事犯罪情况
            familyAddress = row[17].decode('utf-8')#家庭住址
            telephone = row[18].decode('utf-8')#联系电话
            extra = row[19].decode('utf-8')#备注
            
            #add to list
            valueList.append(name)#0
            valueList.append(gender)
            valueList.append(birth)#2
            valueList.append(teacherBegin)
            valueList.append(teacherEnd)#4
            valueList.append(familyAddress)
            valueList.append(telephone)#6
            valueList.append(identityCard)
            if townType=='农':
                townType = u'是□√  否□'
            elif townType=='城镇':
                townType = u'是□  否□√'
            else:
                townType = u'户籍不明'
            valueList.append(townType)#8
            valueList.append(crime)
            valueList.append(birthRestrict)#10
            valueList.append(assurance)
            valueList.append(totalYears)#12
            valueList.append(teacherBeginEnd)
            valueList.append(originalSchool)#14
            
            contentList.append(valueList)
    return contentList


#设置头部信息                
def setHeadline(selection):
    selection.ParagraphFormat.Alignment = 0#居左
    selection.Font.Size = 12#字号
    selection.TypeText(u"附件6")
    selection.TypeParagraph()#输入换行
    
    selection.ParagraphFormat.Alignment = 1#居中
    selection.Font.Size = 18#字号
    selection.TypeText(u"邹平县农村原民办代课教师身份和教龄认定表")
    selection.TypeParagraph()#输入换行
    
    selection.ParagraphFormat.Alignment = 2#居右
    selection.Font.Size = 10#字号
    selection.TypeText(u"2014年 4月  28日 ")
    selection.TypeParagraph()#输入换行
    
    #表格内的格式
    selection.ParagraphFormat.Alignment = 1#居中
    selection.Font.Size = 12#表格字体字号

#设置尾部信息
def setEndline(selection):
    selection.Font.Size = 10#字号
    selection.TypeText(u"备注：请在类别中选择一个最长的任教类型，并在□内打“√”，一式3份上报。")#输入汉字
    selection.TypeParagraph()#输入换行
    selection.TypeParagraph()#输入换行

#预处理表格    
def beginTable(selection):
    setHeadline(selection)
    table = doc.Tables.Add(selection.Range, tableRow, tableCol)#插入tableRow行tableCol列的表格
    table.Columns(1).SetWidth(35, 0)#设置第一列的宽度
    table.Columns(2).SetWidth(110, 0)#设置第二列的宽度
    table.Columns(3).SetWidth(35, 0)#设置第三列的宽度
    table.Columns(4).SetWidth(70, 0)#设置第四列的宽度
    table.Columns(5).SetWidth(35, 0)#设置第五列的宽度
    table.Columns(6).SetWidth(110, 0)#设置第六列的宽度
    table.Columns(7).SetWidth(70, 0)#设置第七列的宽度
    return table

#处理表格
def executeTable(table,cellsTextList,valueList):
    cellsTextListCount = len(cellsTextList)
    if cellsTextListCount!=tableRow:
        print 'cellsTextListCount!=tableRow'
        raise Exception('cellsTextListCount!=tableRow')
    for i in range(tableRow):
        lineOfcellsTextList = cellsTextList[i]
        firstColumnText = lineOfcellsTextList[0]
        if firstColumnText.count('valueList_')>0:
            firstColumnText = valueList[int(firstColumnText[10:])]
        secondColumnText = lineOfcellsTextList[1]
        if secondColumnText.count('valueList_')>0:
            secondColumnText = valueList[int(secondColumnText[10:])]
        thirdColumnText = lineOfcellsTextList[2]
        if thirdColumnText.count('valueList_')>0:
            thirdColumnText = valueList[int(thirdColumnText[10:])]
        forthColumnText = lineOfcellsTextList[3]
        if forthColumnText.count('valueList_')>0:
            forthColumnText = valueList[int(forthColumnText[10:])]
        fifthColumnText = lineOfcellsTextList[4]
        if fifthColumnText.count('valueList_')>0:
            fifthColumnText = valueList[int(fifthColumnText[10:])]
        sixthColumnText = lineOfcellsTextList[5]
        if sixthColumnText.count('valueList_')>0:
            sixthColumnText = valueList[int(sixthColumnText[10:])]
        seventhColumnText = lineOfcellsTextList[6]
        if seventhColumnText.count('valueList_')>0:
            seventhColumnText = valueList[int(seventhColumnText[10:])]
            
        table.Cell((i+1),1).Range.Text = firstColumnText#向单元格中添加文字
        table.Cell((i+1),2).Range.Text = secondColumnText
        table.Cell((i+1),3).Range.Text = thirdColumnText
        table.Cell((i+1),4).Range.Text = forthColumnText
        table.Cell((i+1),5).Range.Text = fifthColumnText
        table.Cell((i+1),6).Range.Text = sixthColumnText
        table.Cell((i+1),7).Range.Text = seventhColumnText
        i+=1

#结束处理表格   
def endTable(selection):
    selection.MoveDown(5, 100)#插入n行表格之后必须使用MoveDown(tableCol,n)移动到表格之后才能进行其它操作
    setEndline(selection)
    

    
if __name__ == '__main__':
    try:
        #teacher_type = 'daike'#51人
        #teacher_type = 'youer'#39人
        #teacher_type = 'dengji'#4人
        teacher_type = 'qita'#1人
        
        if teacher_type=='daike':
            print u'处理代课'
            csvFileName = 'yuandaike.csv'
        elif teacher_type=='youer':
            print u'处理幼儿'
            csvFileName = 'yuanyouer.csv'
        elif teacher_type=='dengji':
            print u'处理登记'
            csvFileName = 'dengji.csv'
        elif teacher_type=='qita':
            print u'处理其它'
            csvFileName = 'qita.csv'
        
        wordApp = Dispatch('Word.Application')#创建一个word进程
        wordApp.Visible = 1 #这个至少在调试阶段建议打开，否则如果等待时间长的话，它至少给你耐心。。。
        doc = wordApp.Documents.Add()#新建一个word文档
        
        selection = wordApp.Selection#得到光标对象
        #selection.Font.Name = "宋体"
        
        contentList = readCSVFile(csvFileName)
        listTotalCount = len(contentList)
        print 'There are altogether ' + str(listTotalCount) + ' people.'
        
        #开始循环每个人的信息
        for i in range(listTotalCount):
            valueList = contentList[i]
            print 'Now processing ' + valueList[0] + ' , ' + str(i+1) + ' of ' + str(listTotalCount) + '.'
            cellsTextList = createTableFixedCellText(teacher_type)
            table = beginTable(selection)
            executeTable(table,cellsTextList,valueList)
            endTable(selection)
            i+=1
        
        
        #doc.Close()#关闭文档
        #wordApp.Quit()#关闭word进程
    except Exception, msg:
        print 'error occured. The reason is: ' + str(msg)
