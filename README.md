# 小型网站爬虫
针对某一学校新闻页面（特定网站）的小型网站爬虫
## 一，目标分析  
### 1选取目标  
华东交大“交大要闻”新闻页面  
https://xw.ecjtu.edu.cn/  
https://xw.ecjtu.edu.cn/jdyw/684.htm  
![image](https://user-images.githubusercontent.com/58925720/138362655-fe0745c0-cd10-4c23-8665-3365cbdebd32.png)

### 2网页结构分析  
#### （1）页面目录  
##### a,文章目录  
第1页：https://xw.ecjtu.edu.cn/jdyw.htm  
第2页：https://xw.ecjtu.edu.cn/jdyw/684.htm  
第3页：https://xw.ecjtu.edu.cn/jdyw/683.htm  
第4页：https://xw.ecjtu.edu.cn/jdyw/682.htm  
第5页：https://xw.ecjtu.edu.cn/jdyw/681.htm  
……  
第685页：https://xw.ecjtu.edu.cn/jdyw/1.htm  
##### b,文章页面  
经过总结如右侧：https://xw.ecjtu.edu.cn/info/1041/xxxxx.htm  
#### （2）同页结构  
![image](https://user-images.githubusercontent.com/58925720/138362690-4a61b831-0d12-4a35-8bd6-38c2b885d82f.png)
结构在list fl，"a"标签下  
#### （3）文章页面结构  
![image](https://user-images.githubusercontent.com/58925720/138362706-2b8598b4-9953-4b34-a46a-c59f2abb60a0.png)
结构在content-con，"p"标签下  
其他情况下存在渲染等非预期字符，故需要考虑白名单过滤汉字。  
![image](https://user-images.githubusercontent.com/58925720/138362766-8f6c82b0-bed6-4b94-b438-063b162a969c.png)
## 二，爬虫关键代码  
### 1调用bs4库  
from urllib.request import urlopen  
from bs4 import BeautifulSoup  

html = urlopen('url')  
bs = BeautifulSoup(html.read(), 'html.parser')  
#print(bs)
### 2爬取并截获文章内容  
#爬取content-title的标题  
nameList=bs.findAll('div',{'class':'content-title'})  
h3_txt=[]  
for i in nameList:  
    h3_txt.append(str(i.findAll('h3')))  

#爬取文章内容(p)  
nameList=bs.findAll('div',{'class':'v_news_content'})  
p_txt=[]  
for i in nameList:#由于tag的属性get_text需要针对每一个变量  
    for j in i.findAll('span'):  
        p_txt.append(str(j.get_text()))  

### 3处理文章内容，并保存到列表  
nameList=bs.findAll('h3')#标签爬取  

strlist=[]  
pattern = re.compile(r'[\u4e00-\u9fa5]+')#白名单过滤中文字符  
for i in nameList:  
    p = re.findall(pattern, str(i))  
    if str(p)!='[]':#过滤为空的情况  
        strlist.append(p)  
    else:  
        continue  
print(strlist)  
### 4爬取第一页url  
import re  
from urllib.request import urlopen  
from bs4 import BeautifulSoup  
  
html = urlopen('https://xw.ecjtu.edu.cn/jdyw.htm')#每页15篇文章内容  
bs = BeautifulSoup(html.read(), 'html.parser')  
  
#爬取第一页url  
url_txt=[]  
nameList=bs.findAll('div',{'class':'list fl'})  
for i in nameList:  
    for link in i.findAll('a'):  
        if 'href' and 'target' in link.attrs:#根据基本格式抓取文章URL  
            url_txt.append(link.attrs['href'])#保存到列表  
  
print(url_txt)  

## 三，词云关键代码  
def img_grearte():  
    mask = imread("xin.jpeg")  
    with open("txt_save.txt", "r") as file:  
        txt = file.read()  
    word = WordCloud(background_color="white",  
                     width=800,  
                     height=800,  
                     font_path='simhei.ttf',  
                     mask=mask,  
                     stopwords=['的','是','和','要','了','有','与','也','将','就','对','在','到','也','人','为','等','我']  
                     ).generate(txt)  
    word.to_file('test.png')  
    print("词云图片已保存")  
  
## 四，其他记录  
### 1 python requirement  
需要安装以下库  
Bs4,Re,wordcloud,imageio  
### 2遇到安装wordcloud库的问题  
解决方式： https://blog.csdn.net/DCclient/article/details/89818315
### 3 遇到from scipy.misc import imread 报错  
使用词云脚本的时候发生的错误  
解决方式： https://www.cnblogs.com/Yanjy-OnlyOne/p/12032030.html
### 4 处理../的意外情况  
for i in nameList:  
    for link in i.findAll('a'):  
        if 'href' and 'target' in link.attrs:  # 根据基本格式抓取文章URL  
            if '..' in link.attrs['href']:#处理../的意外情况  
                url=link.attrs['href'].replace('..','https://xw.ecjtu.edu.cn')  
                url_txt.append(url)# 保存到列表  
            else:  
                url_txt.append(link.attrs['href'])  
### 5最终结果  
简单调用同目录下的两个脚本  
import小型网站爬虫.连续页面爬虫  
import小型网站爬虫.词云脚本  
  
if__name__=="__main__":  
小型网站爬虫.连续页面爬虫  
小型网站爬虫.词云脚本  
![image](https://user-images.githubusercontent.com/58925720/138362813-e5f11431-733c-4311-b1e2-ab818de5eced.png)

## 五，脚本分析  
### 1连续页面爬取.py  
修改爬取页数：  
 ![image](https://user-images.githubusercontent.com/58925720/138362831-e53549dc-d9ec-4a24-8159-eabe2ebae74f.png)
### 2词语脚本.py  
修改禁用词：  
![image](https://user-images.githubusercontent.com/58925720/138362846-09cb6c4d-24c8-4a23-8096-a453749bb803.png)


