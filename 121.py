import re
import requests
from bs4 import BeautifulSoup
# 是获得html网页数据
def getHTMLText(url):
    try:
        r = requests.get(url)
        # 响应返回404，故使用以下语句会抛出异常：
        # 如果是返回200，则raise_for_status()并不会抛出异常。
        r.raise_for_status()
        #  apparent_encoding通过调用chardet.detect()来识别文本编码. 但是需要注意的是，这有些消耗计算资源
        # r.encoding：猜测的编码，从 headers 中的 charset 中获得，但并非所有的服务器都会对其相关资源的编码进行规定和要求；
        # 如果 headers 中不存在charset，则认为（猜测）其编码为ISO-8859-1
        # r.apparent_encoding：根据内容分析出的编码方式，备选编码；
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
# 股票代码
def getStockList(lst, stockURL):
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r"[s][hz]\d{6}", href)[0])
        except:
            continue
    print("【股票代码列表】：\r\n", lst)
# 股票的信息
def getStockInfo(lst, stockURL, fpath):
    count = 0
    for stock in lst:
        url = stockURL + stock + ".html"
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class': 'stock-bets'})
            name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]
            """
            1、split()函数
            语法：str.split(str="",num=string.count(str))[n]
            参数说明：
            str:表示为分隔符，默认为空格，但是不能为空('')。若字符串中没有分隔符，则把整个字符串作为列表的一个元素
            num:表示分割次数。如果存在参数num，则仅分隔成 num+1 个子字符串，并且每一个子字符串可以赋给新的变量
            [n]:表示选取第n个分片
            注意：当使用空格作为分隔符时，对于中间为空的项会自动忽略
           """
            infoDict.update({'股票名称': name.text.split()[0]})
            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val
            with open(fpath, 'a', encoding='utf-8') as f:
                f.write(str(infoDict) + '\n')
                count = count + 1
                print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
        except:
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
            continue
def main():
    # 股票代码--爬取的网站
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    # 股票信息--爬取的网站
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    # 输出文件
    output_file = 'D:/BaiduStockInfo.txt'
    # 股票信息--字典
    slist = []
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)
# 程序入口
main()
