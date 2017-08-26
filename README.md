# SpidyPractice



## 糗事百科爬取
- 抓取页面内容
```
import urllib
import urllib2

page=1;
url="https://www.qiushibaike.com/8hr/page/"+str(page)
//加入header
user_agent='Mzilla/4.0(compatiable;MSIE 5.5;Windows NT)'
headers={'User-Agent':user_agent}
//创建request对象
request=urllib2.Request(url,headers=headers)
response=urllib2.urlopen(request)
//读取对象
print response.read()
```
>【raise BadStatusLine(line)】
出现此问题一般为Headers验证
- 分析html获取段子

正则表达式的说明

1）.*?是固定搭配，代表匹配任意字符

2）（.*?)代表一个分组

3)re.compile(string[,flag]),flag代表匹配模式，取值可以用|表示同时生效，如re.I|re.M
> re.S点任意匹配模式

4）re.findAll(pattern,string[,flags])搜索String以列表形式返回全部能匹配的子串。

5）```re.compile(r'<div.*?class="author.*?>.*?<h2>(.*?)</h2>.*?<div.*?class="content".*?span>(.*?)</span.*?div>.*?class="number">(.*?)</i>',re.S)```

```【解释】.*?=不知道是什么的一大堆东西（.*?需要的一大堆东西）```

6）去掉中间的部分re.sub('<br/>','\n',item[1])


- 逻辑设计（面向对象）

1)初始化

post数据需要headers

传入爬取页数pageIndex

程序是否在运行（运行加载下一页&&且未看段子少于2）则加载下一页enable

存取段子，看完删掉得到上述所说看了与未看段子数stories
```
    def __init__(self):
        self.pageIndex=1
        self.enable=False
        self.stories=[]
        self.user_agent='Mzilla/4.0(compatiable;MSIE 5.5;Windows NT)'
        self.headers={'User-Agent':self.user_agent}
```

2）传入索引代码

获取源代码
```
    def getPage(self,pageIndex):
        url="https://www.qiushibaike.com/8hr/page/text/"+str(pageIndex)
        request=urllib2.Request(url,headers=self.headers)
        response=urllib2.urlopen(request)
        content=response.read().decode('utf-8')
        return content
 ```
 
 3)提取内容

```
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
   ```
       
 
 4)一页结束加载并提取页面的内容
 
 ```
      def loadPage(self):
        if self.enable==True:
            if len(self.stories)<2:
                #获取新一页
                pageStories=self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex+=1
```
 
 

5)每次敲回车输出一个段子

```
     def getOneStory(self,pageStories,page):
        for story in pageStories:
            input=raw_input()
            self.loadPage()
            if input=="Q":
                self.enable=False
                return
            print u"第%d页\t发布人:%s\t赞:%s\n%s"%(page,story[0],story[2],story[1])
```
