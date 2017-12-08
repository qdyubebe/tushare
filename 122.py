from urllib import request
from bs4 import BeautifulSoup as bs
import re
import jieba    #分词包
import pandas as pd
import numpy    #numpy计算包
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
# %matplotlib inline是jupyer notebook 的命令
# %matplotlib inline
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
resp = request.urlopen('https://movie.douban.com/nowplaying/hangzhou/')
html_data_comment = resp.read().decode('utf-8')
# 获取HTML页面内容
# print("豆瓣最新上映的电影页面内容：",html_data)
soup = bs(html_data_comment, 'html.parser')
# find_all 返回值是数组
nowplaying_movie = soup.find_all('div', id='nowplaying')
# 获取电影列表
nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')
# print("电影列表：\r\n",nowplaying_movie_list)
# 获取电影的id和名称。
nowplaying_list = []
for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id'] = item['data-subject']
        nowplaying_dict['name'] = item['data-title']
        # nowplaying_list.append(nowplaying_dict)
        # for tag_img_item in item.find_all('img'):
        #     nowplaying_dict['name'] = tag_img_item['alt']
        nowplaying_list.append(nowplaying_dict)
# print("电影的id和名称：\r\n",nowplaying_list)
# 网友对电影的评论
requrl = 'https://movie.douban.com/subject/' + nowplaying_list[5]['id'] + '/comments' +'?' +'start=0' + '&limit=20'
resp = request.urlopen(requrl)
html_data_comment = resp.read().decode('utf-8')
soup = bs(html_data_comment, 'html.parser')
comment_div_lits = soup.find_all('div', class_='comment')
# print("网友对电影-战狼的评论HTML内容：\r\n",comment_div_lits)
eachCommentList = [];
for item in comment_div_lits:
        if item.find_all('p')[0].string is not None:
            eachCommentList.append(item.find_all('p')[0].string)
# print("网友对电影-战狼的评论：",comment_div_lits)
# 为了方便进行数据进行清洗，我们将列表中的数据放在一个字符串数组中
comments = ''
for k in range(len(eachCommentList)):
    comments = comments + (str(eachCommentList[k])).strip()
# print("网友对电影-战狼的评论[数据清洗后]：\r\n",comments)
# /^(\w|-|[\u4E00-\u9FA5])*$/
# ^ 以后面的为开头
# $ 以前面的为结尾
# \w 数字，字母，下划线，.
# \u4E00-\u9FA5 中文
# * 代表前面出现0次或多次
# | 或者
# 所以整个的意思是匹配一个 数字，字母，下划线，-，.，中文组成的一个字串
# 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
pattern = re.compile(r'[\u4e00-\u9fa5]+')
filterdata = re.findall(pattern, comments)
cleaned_comments = ''.join(filterdata)
# print("网友对电影-战狼的评论[数据清洗后]：\r\n",cleaned_comments)
# 进行词频统计，先要进行中文分词操作。这里使用的是结巴分词
segment = jieba.lcut(cleaned_comments)
words_df=pd.DataFrame({'segment':segment})
# print("[分词之后的结果]：\r\n",words_df)
# 清除停用词
# 停用词放在一个stopwords.txt文件中，将我们的数据与停用词进行比对即可
#quoting=3全不引用
stopwords=pd.read_csv("stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='utf-8')
words_df=words_df[~words_df.segment.isin(stopwords.stopword)]
# print("[清除停用词后]：\r\n",words_df.head())
# 词频统计
words_stat=words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
words_stat=words_stat.reset_index().sort_values(by=["计数"],ascending=False)
# print("[词频统计后]：\r\n",words_stat.head())
# 用词云进行显示
backgroud_Image = plt.imread('man.jpg')
wordcloud = WordCloud(
    background_color='white',
    mask=backgroud_Image,
    font_path='C:\Windows\Fonts\STZHONGS.TTF',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
    max_words=2000,
    stopwords=STOPWORDS,
    max_font_size=150,
    random_state=30
)
word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}
print("[用词云进行显示--字典类型]：\r\n", word_frequence)
word_frequence_list = []
for key in word_frequence:
    temp = (key,word_frequence[key])
    word_frequence_list.append(temp)
print("[用词云进行显示--LIST]：\r\n", word_frequence_list)
# fit_words(frequencies)  //根据词频生成词云
# generate(text)  //根据文本生成词云
# generate_from_frequencies(frequencies[, ...])   //根据词频生成词云
# generate_from_text(text)    //根据文本生成词云
# word_frequence 为字典类型，可以直接传入wordcloud.fit_words()
# word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}
# wordcloud = wordcloud.fit_words(word_frequence)
# def fit_words(self, frequencies):
#     """Create a word_cloud from words and frequencies.
#
#     Alias to generate_from_frequencies.
#
#     Parameters
#     ----------
#     frequencies : dict from string to float
#         A contains words and associated frequency.
#
#     Returns
#     -------
#     self
#     """
#     return self.generate_from_frequencies(frequencies)
wordcloud=wordcloud.fit_words(word_frequence)
plt.imshow(wordcloud)
plt.show()
#coding:utf-8
__author__ = 'hang'
import warnings
warnings.filterwarnings("ignore")
import jieba    #分词包
import numpy    #numpy计算包
import codecs   #codecs提供的open方法来指定打开的文件的语言编码，它会在读取的时候自动转换为内部unicode
import re
import pandas as pd
import matplotlib.pyplot as plt
from urllib import request
from bs4 import BeautifulSoup as bs
# %matplotlib inline
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator#词云包
#分析网页函数
def getNowPlayingMovie_list():
    resp = request.urlopen('https://movie.douban.com/nowplaying/hangzhou/')
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    nowplaying_movie = soup.find_all('div', id='nowplaying')
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')
    nowplaying_list = []
    for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id'] = item['data-subject']
        for tag_img_item in item.find_all('img'):
            nowplaying_dict['name'] = tag_img_item['alt']
            nowplaying_list.append(nowplaying_dict)
    return nowplaying_list
#爬取评论函数
def getCommentsById(movieId, pageNum):
    eachCommentList = [];
    if pageNum>0:
         start = (pageNum-1) * 20
    else:
        return False
    requrl = 'https://movie.douban.com/subject/' + movieId + '/comments' +'?' +'start=' + str(start) + '&limit=20'
    print(requrl)
    resp = request.urlopen(requrl)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    comment_div_lits = soup.find_all('div', class_='comment')
    for item in comment_div_lits:
        if item.find_all('p')[0].string is not None:
            eachCommentList.append(item.find_all('p')[0].string)
    return eachCommentList
def main():
    #循环获取第一个电影的前10页评论
    commentList = []
    NowPlayingMovie_list = getNowPlayingMovie_list()
    for i in range(10):
        num = i + 1
        commentList_temp = getCommentsById(NowPlayingMovie_list[0]['id'], num)
        commentList.append(commentList_temp)
    #将列表中的数据转换为字符串
    comments = ''
    for k in range(len(commentList)):
        comments = comments + (str(commentList[k])).strip()
    #使用正则表达式去除标点符号
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, comments)
    cleaned_comments = ''.join(filterdata)
    #使用结巴分词进行中文分词
    segment = jieba.lcut(cleaned_comments)
    words_df=pd.DataFrame({'segment':segment})
    #去掉停用词
    stopwords=pd.read_csv("stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='utf-8')#quoting=3全不引用
    words_df=words_df[~words_df.segment.isin(stopwords.stopword)]
    #统计词频
    words_stat=words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
    words_stat=words_stat.reset_index().sort_values(by=["计数"],ascending=False)
    # 用词云进行显示
    backgroud_Image = plt.imread('man.jpg')
    wordcloud = WordCloud(
        background_color='white',
        mask=backgroud_Image,
        font_path='C:\Windows\Fonts\STZHONGS.TTF',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
        max_words=2000,
        stopwords=STOPWORDS,
        max_font_size=150,
        random_state=30
    )
    word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}
    print("[用词云进行显示--字典类型]：\r\n", word_frequence)
    word_frequence_list = []
    for key in word_frequence:
        temp = (key, word_frequence[key])
        word_frequence_list.append(temp)
    print("[用词云进行显示--LIST]：\r\n", word_frequence_list)
    # fit_words(frequencies)  //根据词频生成词云
    # generate(text)  //根据文本生成词云
    # generate_from_frequencies(frequencies[, ...])   //根据词频生成词云
    # generate_from_text(text)    //根据文本生成词云
    # word_frequence 为字典类型，可以直接传入wordcloud.fit_words()
    # def fit_words(self, frequencies):
    #     """Create a word_cloud from words and frequencies.
    #
    #     Alias to generate_from_frequencies.
    #
    #     Parameters
    #     ----------
    #     frequencies : dict from string to float
    #         A contains words and associated frequency.
    #
    #     Returns
    #     -------
    #     self
    #     """
    #     return self.generate_from_frequencies(frequencies)
    wordcloud = wordcloud.fit_words(word_frequence)
    img_colors = ImageColorGenerator(backgroud_Image)
    wordcloud.recolor(color_func=img_colors)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    print('display success!')
#主函数
main()
