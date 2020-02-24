# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
class qiushibaike:
#初始化
    def __init__(self):
        self.pageIndex=1
        self.enable=False
        self.stories=[]
        self.user_agent='Mzilla/4.0(compatiable;MSIE 5.5;Windows NT)'
        self.headers={'User-Agent':self.user_agent}
    #传入索引代码
    def getPage(self,pageIndex):
        url="https://www.qiushibaike.com/8hr/page/text/"+str(pageIndex)
        request=urllib2.Request(url,headers=self.headers)
        response=urllib2.urlopen(request)
        content=response.read().decode('utf-8')
        return content

    #传入某一页代码返回内容
    def getPageItems(self, pageIndex):
        pageCode=self.getPage(pageIndex)
        if not pageCode:
            print "loding failed"
            return None
        pattern=re.compile(r'<div.*?class="author.*?>.*?<h2>(.*?)</h2>.*?<div.*?class="content".*?span>(.*?)</span.*?div>.*?class="number">(.*?)</i>',re.S)
        items = re.findall(pattern, pageCode)
        pageStories=[];
        for item in items:
            replaceBR=re.compile('<br/>')
            text=re.sub(replaceBR,'\n',item[1])
            pageStories.append(([item[0].strip(),text.strip(),item[2].strip()]))
        return pageStories

    #加载并提取页面的内容
    def loadPage(self):
        if self.enable==True:
            if len(self.stories)<2:
                #获取新一页
                pageStories=self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex+=1

    #每次敲回车输出一个段子
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input=raw_input()
            self.loadPage()
            if input=="Q":
                self.enable=False
                return
            print u"第%d页\t发布人:%s\t赞:%s\n%s"%(page,story[0],story[2],story[1])

    #开始方法
    def start(self):
        print u"正在读取段子，回车查看新段子，Q退出"
        self.enable=True
        self.loadPage()
        nowPage=0
        while self.enable:
            if len(self.stories)>0:
                pageStories=self.stories[0]
                nowPage+=1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)
spider=qiushibaike()
spider.start()
