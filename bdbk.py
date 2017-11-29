#-*-coding?utf-8 -*-
import urllib.request
import urllib.parse
import re

class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()
class BDTB:
    def __init__(self,baseUrl,seeLz,floorTag):
        self.baseURL = baseUrl
        self.seeLz = '?see_lz='+str(seeLz)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.defaultTitle = u"百度贴吧"
        self.floorTag = floorTag
    def getPage(self,pageNum):
        try:
            url = self.baseURL+self.seeLz+'&pn='+str(pageNum)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            #print(response.read())
            return response.read().decode('utf-8')
        except urllib.request.URLError as e:
            if hasattr(e,'reason'):
                print('link BDTB error')
                return None

    def getTitle(self,page):
        pattern = re.compile('<h3 class="core_title_txt.*?title="(.*?)" style',re.S)
        result = re.search(pattern,page)
        if result:
            print(result.group(1))
            return result.group(1).strip()
        else:
            return None
    def getNum(self,page):
        pattern = re.compile('<li class="l_reply_num".*?margin-right:3px">.*?</span>.*?<span class="red">(.*?)</span>',re.S)
        result = re.search(pattern , page)
        if result:
            print(result.group(1))
            return result.group(1).strip()
        else:
            return None

    def getContent(self,page):
        pattern = re.compile('<cc>.*?<div id=.*?j_d_post_content ">(.*?)</div>',re.S)
        result = re.findall(pattern,page)
        contents = []
        if result:

            for line in result:
                temp = "\n" + self.tool.replace(line.strip()) + "\n"
                print(self.tool.replace(line.strip()))
                contents.append(temp)
            return contents
        else:
            return None

    def setFileTitle(self,title):
        if title is not None:
            self.file = open(title + ".txt" , "w+")
        else:
            self.file = open(self.defaultTitle+".txt", "w+")

    def writeData(self,contents):
        for item in contents:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) + u"-----------------------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum =self.getNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print("找不到")
            return
        try:
            print("该帖子共有"+str(pageNum)+"页")
            for i in range(1,int(pageNum)+1):
                print("正在写入第" + str(i) + "页数据")
                page = self.getPage(i)
                contents =self.getContent(page)
                self.writeData(contents)
        except IOError as e:
            print("异常")
        finally:
            print("下载结束")

print("请输入帖子代号：")
baseURL = 'http://tieba.baidu.com/p/'+str(input(u'http://tieba.baidu.com/p/'))
seeLz = input("是否只获取楼主发言，是输入1，否输入0\n")
floorTag = input("是否写入楼层信息，是输入1，否输入0\n")
dbtb = BDTB(baseURL,seeLz,floorTag)
dbtb.start()