#使用import导入requests和jieba模块
import requests
import jieba

#将想要获取的B站视频评论URL地址，赋值给变量url
url = "https://www.bilibili.com/video/BV197XhYjEH8/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=07f75161237cbb111aa63eec3ff41dc3"

#将User-Agent以字典键对形式赋值给headers
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"}

#将字典headers传递给headers参数，添加进requests.get()中，赋值给response
response=requests.get(url,headers=headers)

#使用.text属性获取网页内容，并赋值给html
#若是想限制爬取数量可以这样写html=response.text[:1000]如此会提取前1000个字符
html=response.text
from bs4 import BeautifulSoup
#使用lxml解析html并赋值给soup
soup=BeautifulSoup(html,"lxml")
#用find_all()查询节点
content_all=soup.find_all('p')
#用string提取内容以及列表合并
word_list=[]
for content in content_all:
    contentString=content.string
    words=jieba.lcut(contentString)
    word_list +=words
#词频统计
word_dict={}
for word in word_list:
    if len(word)>1:
        if word not in word_dict.keys():
            word_dict[word] =1
        else:
            word_dict[word] +=1
print(word_dict)
#导入os库
import os
#将变量 output_dir 赋值为 "."，在文件路径中，. 代表当前工作目录，也就是代码文件所在的目录
output_dir="."
#检查指定的路径是否存在，如果指定的目录路径不存在，它会创建该目录及其所有必要的父目录。
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
#到了这里评论就基本结束了，下面代码的功能是将提取的评论生成为词云图，感兴趣的可以看一看
#生成词云图
from pyecharts.charts import WordCloud
#创建一个 WordCloud 类的实例对象，赋值给变量 wd。WordCloud 类是 pyecharts 库中用于生成词云图的类
wd=WordCloud()
#设置参数，series_name 表示系列名称，这里将其赋值为空字符串 ""，data_pair 是一个包含词云数据的列表，这里用items先将字典转换为元组，再用list将元组转化为列表，word_size_range用来设定词云图大小
wd.add(series_name="",data_pair=list(word_dict.items()),word_size_range=[20,80])
#设置文件路径
output_path=os.path.join(output_dir,"first_net_content.html")
#将生成的词云图渲染并保存为 HTML 文件
wd.render(output_path)
print("success")
