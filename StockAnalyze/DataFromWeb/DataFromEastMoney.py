#导入需要使用到的模块
import urllib
import re
import requests
import pandas as pd
import pymysql
import os

# #爬虫抓取网页函数
# def getHtml(url):
#     html = requests.get(url)
#     return html.text
#
# #抓取网页股票代码函数
# def getStackCode(html):
#     s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
#     pat = re.compile(s)
#     code = pat.findall(html)
#     return code
#
#
# Url = 'http://quote.eastmoney.com/stocklist.html'#东方财富网股票数据连接地址
filepath = 'D:\\data\\'#定义数据文件保存路径
# #实施抓取
# code = getStackCode(getHtml(Url))
# #获取所有股票代码（以6开头的，应该是沪市数据）集合
# CodeList = []
# for item in code:
#     if item[0]=='6':
#         CodeList.append(item)
#抓取数据并保存到本地csv文件
CodeList = ['600000']
for code in CodeList:
    print('正在获取股票%s数据'%code)
    url1 = 'https://quote.eastmoney.com/center/gridlist.html#hs_a_board'

    url2 = 'http://quotes.money.163.com/service/chddata.html?code=0'+code+\
        '&end=20161231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    url3 = 'http://quote.eastmoney.com/center/hszs.html'
    url4= 'http://quote.eastmoney.com/zs000688.html'

    url5 = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=0.000006&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&lmt=58&klt=101&fqt=1&end=30000101&ut=fa5fd1943c7b386f172d6893dbfba10b&cb=cb_1631872070467_98520225&cb_1631872070467_98520225=cb_1631872070467_98520225'


    url6 = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg=0&end=20500101&ut=fa5fd1943c7b386f172d6893dbfba10b&rtntype=6&secid=0.000001&klt=101&fqt=1&cb=jsonp1631873125527'

    #沪深300成分股
    url7 ='http://data.eastmoney.com/other/index/hs300.html'


    html1 = requests.get(url7)
    print(html1.text)


    url8 = 'http://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123012478129716691644_1631928122122&sortColumns=SECURITY_CODE&sortTypes=-1&pageSize=50&pageNumber=1&reportName=RPT_INDEX_TS_COMPONENT&columns=SECUCODE%2CSECURITY_CODE%2CTYPE%2CSECURITY_NAME_ABBR%2CCLOSE_PRICE%2CINDUSTRY%2CREGION%2CWEIGHT%2CEPS%2CBPS%2CROE%2CTOTAL_SHARES%2CFREE_SHARES%2CFREE_CAP&quoteColumns=f2%2Cf3&source=WEB&client=WEB&filter=(TYPE%3D%222%22)'

    HS300 ='http://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112309785194520764149_1632298068749&sortColumns=SECURITY_CODE&sortTypes=1&pageSize=50&pageNumber=1&reportName=RPT_INDEX_TS_COMPONENT&columns=SECUCODE,SECURITY_CODE,TYPE,SECURITY_NAME_ABBR,CLOSE_PRICE,INDUSTRY,REGION,WEIGHT,EPS,BPS,ROE,TOTAL_SHARES,FREE_SHARES,FREE_CAP&quoteColumns=f2,f3&source=WEB&client=WEB&filter=(TYPE="1")'
    html = requests.get(HS300)
    print(html.text)
