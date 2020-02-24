#coding=utf-8
__author__='kon'
import urllib
import urllib2
import re

class Tool:
    #去除图片
    removeImg=re.compile('<img.*?>|</img>')
    #去除a
    removeAddr=re.compile('<a.*?>|</a>')
    #换行换成\n
    replaceLine=re.compile('<tr>|<div>|</div>|</p>')
    #<td>换成\t
    replaceTD=re.compile('<td>')
    #段落开头空格\n加空两格
    replacePara=re.compile('<p.*?>')
    #换行符置换
    replaceBR=re.compile('<br><br>|<br>')
    #其余标签剔除
    removeExtraTag=re.compile('<.*?>')
    def replace(self,x):
        x=re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()


class BDTB:
    def __init__(self,baseUrl,seeLZ,floorTag):
        self.baseUrl=baseUrl;
        self.seeLZ='?see_lz='+str(seeLZ)
        self.tool=Tool()
        #全局file变量文件写入对象
        self.file = None
        self.floor = 1
        self.defaultTitle = u"kon's"
        self.floorTag = floorTag



    def getPage(self,pageNum):
        stripUrl=baseUrl.strip()

        url=stripUrl+self.seeLZ+'&pn='+str(pageNum)
        print url
        request=urllib2.Request(url)
        response=urllib2.urlopen(request)
        return response.read().decode('utf-8')

    def getTitle(self,page):

        pattern=re.compile('<h1 class="core_title_txt .*?>(.*?)</h1>',re.S)
        result=re.search(pattern,page)
        if result:

            # m.group(N)
            # 返回第N组括号匹配的字符。
            # 而m.group() == m.group(0) == 所有匹配的字符，与括号无关，这个是API规定的。
            #
            # m.groups()
            # 返回所有括号匹配的字符，以tuple格式。
            # m.groups() == (m.group(0), m.group(1), ...)

            return result.group(1)
        else:
            None

    def getPageNum(self,page):
        page=self.getPage(1)
        pattern=re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result=re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getContent(self,page):
        pattern=re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items=re.findall(pattern,page)
        floor=1
        for item in items:
            print floor,u"楼------------------------------------------------------------------------------------------\n"
            print self.tool.replace(item)
            floor+=1
            print "\n"
    #写入文件，主要是file=open("tb.txt","w"),file=writelines(obj)
    def setFileTitle(self,title):
        if title is not None:
            self.file=open(title+".txt","w+")
        else:
            self.file=open(self.defaultTitle+".txt","w+")

    def writeData(self,contents):
        for item in contents:
            if self.floorTag=='1':
                floorLine="\n"+str(self.floor)+u"-----------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor+=1;

    def start(self):
        indexPage=self.getPage(1)
        pageNum=self.getPageNum(indexPage)
        title=self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum==None:
            print 'URL失效'
            return
        print "该贴子共有"+str(pageNum)+"页"
        for i in range(1,int(pageNum)+1):
            print "正在写入第"+str(i)+"页数据"
            page=self.getPage(i)
            contents=self.getContent(page)
            self.writeData(contents)

print u"输入帖子代号"
baseUrl='http://tieba.baidu.com/p/'+str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ=raw_input("是否只获取楼主发言，是输入1，否输入0\n")
floorTag=raw_input("是否输入楼层信息。是输入1，否输入0\n")
bdtb=BDTB(baseUrl,seeLZ,floorTag)
bdtb.start()

