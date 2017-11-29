# _*_coding:utf-8 -*-

import urllib
import  urllib.request
import urllib.parse
import  re
import urllib.error
import http.cookiejar

__author__ = "muzp"

page = 2
url = 'https://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
headers ={'User-Agent': user_agent}


try:

    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode("utf-8")

    pattern = re.compile('''<div class="author clearfix">.*?<h2>(.*?)</h2>'''+
                         '''.*?<a href="(.*?)"''' +
                         '''.*?<span>(.*?)</span>'''+
                         '''(.*?)</div>'''+
                         '''.*?<!-- 图片或gif -->(.*?)<div class="stats">''' +
                         '''.*?<i.*?number">(.*?)</i>''', re.S)

    items = re.findall(pattern, content)

    for item in items:
        haveImg = re.search("img", item[4])
        havere = re.search("查看全文",item[3])
        temp =""
        if havere:
            url1 ="https://www.qiushibaike.com"+item[1]
            print(url1)
            request1 = urllib.request.Request(url1, headers=headers)
            response1 = urllib.request.urlopen(request1)
            content1 = response1.read().decode("utf-8")
            pattern1 = re.compile('<div class="content">(.*?)</div>(.*?)</div>', re.S)
            items1 = re.findall(pattern1, content1)
            for item1 in items1:
                haveImg1 = re.search("img", item1[1])
                if not haveImg1:
                    haveImg = None
                    temp = item1[0]
                else:
                    haveImg = True




        if not haveImg:
            print("作者："+item[0].strip())
            if not havere:
                print("内容："+item[2].strip())
            else:
                print("内容：" + temp.strip())
            print("点赞数："+item[5].strip()+"\n")
except urllib.request.URLError as e:
    if(hasattr(e,"code")):
        print(e.code)
    if(hasattr(e,'reason')):
        print(e.reason)

