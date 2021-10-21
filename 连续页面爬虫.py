import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

def page_go(page_url):
    # 词云存储
    cloud_word_str = ''
    html = urlopen(page_url)  # 每页15篇文章内容
    bs = BeautifulSoup(html.read(), 'html.parser')

    # 爬取第一页url
    url_txt = []
    nameList = bs.findAll('div', {'class': 'list fl'})
    for i in nameList:
        for link in i.findAll('a'):
            if 'href' and 'target' in link.attrs:  # 根据基本格式抓取文章URL
                if '..' in link.attrs['href']:  # 处理../的意外情况
                    url = link.attrs['href'].replace('..', 'https://xw.ecjtu.edu.cn')
                    url_txt.append(url)  # 保存到列表
                else:
                    url_txt.append(link.attrs['href'])

    # print(url_txt)
    for url in url_txt:
        html = urlopen(url)
        bs = BeautifulSoup(html.read(), 'html.parser')

        # 爬取content-title的标题
        nameList = bs.findAll('div', {'class': 'content-title'})
        h3_txt = []
        for i in nameList:
            h3_txt.append(str(i.findAll('h3')))

        # 爬取文章内容(p)
        nameList = bs.findAll('div', {'class': 'v_news_content'})
        span_txt = []
        # 由于该方法提高了时间复杂度，故未多次使用，而是使用白名单做最终过滤
        for i in nameList:  # 由于tag的属性get_text需要针对每一个变量
            for j in i.findAll('span'):
                span_txt.append(str(j.get_text()))

            # 合并字符列表
        content_txt = h3_txt + span_txt

        # 处理文章内容，并保存到列表
        strlist = []
        pattern = re.compile(r'[\u4e00-\u9fa5]+')  # 白名单过滤中文字符
        for i in content_txt:
            p = re.findall(pattern, str(i))
            if str(p) != '[]':  # 过滤为空的情况
                strlist.append(p)
            else:
                continue
        #print(strlist)
        strlist_str = str(strlist).replace("[", "").replace("]", "").replace(", ", "").replace("'", "")
        cloud_word_str = strlist_str + cloud_word_str  # 将表填入

    return  cloud_word_str

#循环爬取指定页数的所有内容

for i in range(5):#指定页数为5页
    url="https://xw.ecjtu.edu.cn/jdyw/"+str(684-i)+".htm"
    f = open("C:\\Users\\qte\\Desktop\\python\\BeautifulSoup\\小型网站爬虫\\test.txt", "a",encoding='utf8')
    #print(url)
    f.write(page_go(url))
    f.close()
    print("******************爬完了第",i+1,"页的15篇******************")

