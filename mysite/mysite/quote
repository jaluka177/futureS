# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import urllib.request
from time import strptime
from datetime import datetime
from bs4 import BeautifulSoup
import time


TXF_NAME = '臺指期' #u指unicode的意思
TE_NAME = '電子期'
TF_NAME = '金融期'

targets = set() #set() 函数创建一个无序不重复元素集，可进行关系测试，删除重复数据，还可以计算交集、差集、并集等。
targets.add(TXF_NAME)
targets.add(TE_NAME)
targets.add(TF_NAME)
list1=[i for i in targets]
quotes = dict() #dict是字典

url = 'http://info512.taifex.com.tw/Future/FusaQuote_Norl.aspx'

#while True:

    # 應該要限制在有交易的時間內執行，但為了示範起見，使用無窮迴圈。

html_data = urllib.request.urlopen(url).read()
#使用urllib.request模块的urlopen（）获取页面 #urlopen返回对象可以使用read()#read() , readline() ,readlines() , fileno() , close() ：這些是对HTTPResponse类型数据进行操作
soup = BeautifulSoup(html_data, 'html.parser')
# print(soup.prettify())
rows = soup.find_all('tr', {"class": "custDataGridRow"})
# print(soup.get_text()) 可以看看html裡面的文字內容
for row in rows:
    items = row.find_all('td')
    name = items[0].a.text.strip()#strip是去前後空格

    if list1[0] or list1[1] or list1[2] in name: #如果excel(name)裡有臺指期、電子期、金融期(targets)

        class Quote(object):
            # 继承了object对象，拥有了好多可操作对象，这些都是类中的高级特性。
            # 实际上在python 3 中已经默认就帮你加载了object了（即便你没有写上object）。
            def __init__(self):  # 因為有object 才可以定義__init__#self的意思看這個網站https://blog.csdn.net/CLHugh/article/details/75000104
                self.name = None
                self.trade_time = None
                self.trade_price = None
                self.change = None
                self.open = None
                self.high = None
                self.low = None
            def __str__(self):
                res = list()
                res.append(self.name)
                res.append(self.trade_time)
                res.append(self.trade_price)
                res.append(self.change)
                res.append(self.open)
                res.append(self.high)
                res.append(self.low)
                return str(res)
        quote = Quote()#新定義的quote=Quote(Object)
        quote.name = name
        if items[6].font.text == '成交價':
            quote.trade_price = items[6].font.text.replace(',', '')
        elif items[6].font.text == '--':
            quote.trade_price = None
        else:
            quote.trade_price = float(items[6].font.text.replace(',', ''))

        if items[7].font.text == '漲跌':
            quote.change = items[7].font.text
        elif items[7].font.text == '--':
            quote.change = None
        else:
            quote.change = float(items[7].font.text)

        if items[14].font.text == '時間':
            quote.trade_time = items[14].font.text
        elif items[14].font.text == '':
            quote.trade_time = None
        else:
            quote.trade_time = datetime.strptime(items[14].font.text, '%H:%M:%S')

        if items[10].font.text.replace(',', '') == '開盤':
            quote.open = items[10].font.text.replace(',', '')
        elif items[10].font.text == '':
            quote.open = None
        else:
            quote.open = float(items[10].font.text.replace(',', ''))

        if items[11].font.text.replace(',', '') == '最高':
            quote.high = items[11].font.text.replace(',', '')
        elif items[11].font.text == '':
            quote.high = None
        else:
            quote.high = float(items[11].font.text.replace(',', ''))

        if items[12].font.text.replace(',', '') == '最低':
            quote.low = items[12].font.text.replace(',', '')
        elif items[12].font.text == '':
            quote.low = None
        else:
            quote.low = float(items[12].font.text.replace(',', ''))
        #quotes[name] = quote#dictionary的quote的name=excel裡面的name
        print(quote)

    # 根據取得的報價判斷條件，條件自訂。
    #
    # 條件符合時通知使用者，如何通知？
time.sleep(5)

