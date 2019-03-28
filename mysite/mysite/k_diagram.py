# -*- coding: UTF-8 -*-
import numpy as np
from .models import RobotTransactionInfo, RobotTransactionInfo2, RobotInformation, RobotRatio1Q, RobotRatio2Q\
    , RobotRatio3Q, RobotRatio1, RobotRatio2, RobotRatio3, RobotCategory, RobotTechnologyIndex,  RobotCashFlowsQ,  RobotPe,  RobotRatio4Q, RobotIncomeStatementQ

#from sklearn import preprocessing
#from sklearn.linear_model import LinearRegression
#import talib
from datetime import datetime, date

##########
import random

from deap import base
from deap import creator
from deap import tools






def k_diagram(id):
    plt.style.use('ggplot')

    date = np.array([])
    close = np.array([])

    data = Transaction_info.objects.filter(stock_id=id)
    for record in data:
        record.the_close = float(record.the_close)
        date = np.append(date, record.date)
        close = np.append(close, record.the_close)

    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    plt.plot_date(date, macd, '-', label='MACD Curve')
    plt.legend()
    plt.xticks(rotation=30)

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(8, 6)
    fig.savefig('static/png/macd.png', dpi=100)
    plt.cla()

def k_diagram_2(id):
    plt.style.use('ggplot')

    date = np.array([])
    high = np.array([])
    low = np.array([])
    close = np.array([])

    data = Transaction_info.objects.filter(stock_id=id)
    for record in data:
        record.high_price = float(record.high_price)
        record.low_price = float(record.low_price)
        record.the_close = float(record.the_close)
        date = np.append(date, record.date)
        high = np.append(high, record.high_price)
        low = np.append(low, record.low_price)
        close = np.append(close, record.the_close)

    slowk, slowd = talib.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    plt.plot_date(date, slowk, '-', label='K Curve')
    plt.plot_date(date, slowd, '-', label='D Curve')
    plt.legend()
    plt.xticks(rotation=30)

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(30, 8)
    fig.savefig('static/png/kd.png', dpi=100)
    plt.cla()

def k_diagram_3(id):
    plt.style.use('ggplot')

    date = np.array([])
    close = np.array([])

    data = Transaction_info.objects.filter(stock_id=id)
    for record in data:
        record.the_close = float(record.the_close)
        date = np.append(date, record.date)
        close = np.append(close, record.the_close)

    rsi = talib.RSI(close, timeperiod=14)
    plt.plot_date(date, rsi, '-', label='RSI Curve')
    plt.legend()
    plt.xticks(rotation=30)

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(30, 8)
    fig.savefig('static/png/rsi.png', dpi=100)
    plt.cla()

def k_diagram_4(id):
    plt.style.use('ggplot')

    date1 = datetime(2013, 1, 2)
    date2 = datetime(2016, 8, 26)
    quotes = quotes_historical_yahoo_ohlc(id+'.TW', date1, date2)

    dates = np.array([])
    volumns = np.array([])
    close = np.array([])

    for records in quotes:
        dates = np.append(dates, records[0])
        volumns = np.append(volumns, records[5])
        close = np.append(close, records[4])

    ma = talib.MA(close, timeperiod=30, matype=0)
    left, width = 0.1, 0.8
    rect_vol = [left, 0.1, width, 0.26]
    rect_min = [left, 0.4, width, 0.5]

    fig = plt.figure()
    ax_vol = fig.add_axes(rect_vol)
    ax_vol.fill_between(dates, volumns, color='y')
    ax_vol.xaxis_date()
    plt.setp(ax_vol.get_xticklabels(), rotation=30, horizontalalignment='right')

    ax_min = fig.add_axes(rect_min)
    candlestick_ohlc(ax_min, quotes, width=0.6, colorup='r', colordown='g')
    ax_min.plot_date(dates, ma, '-', label='MA Curve for 30 days')
    ax_min.axes.get_xaxis().set_visible(False)
    ax_min.legend()

    fig_2 = matplotlib.pyplot.gcf()
    fig_2.set_size_inches(30, 8)
    fig_2.savefig('static/png/k.png', dpi=100)
    fig.clear()

def predict_eps_season(stock):
     category = RobotInformation.objects.get(stock_id=stock).category
     cn = RobotCategory.objects.get(category_id=category).category_name
     search = RobotInformation.objects.get(stock_id=stock).co_name
     data = []
     target = []
     epss = []
     for i in RobotInformation.objects.filter(category=category):
         for d in RobotRatio1Q.objects.filter(stock_id=i.stock_id):
            if d.eps == '--':
                d.eps = 0.0
            else:
                d.eps = float(d.eps)
            epss.append(d.eps)
     avg = round(np.mean(epss), ndigits=2)
     std = round(np.std(epss), ndigits=2)
     set = []
     year = datetime.now().year
     for i in range(year, year-3, -1):
        for a in RobotRatio1Q.objects.filter(stock_id=stock, date__startswith=i).order_by('-date'):
            date = a.date
            b = RobotRatio3Q.objects.get(stock_id=stock, date=date)
            c = RobotRatio2Q.objects.get(stock_id=stock, date=date)
            a.eps = float(a.eps)
            if a.net_profit_margin == '--':
                a.net_profit_margin = 0.0
            if a.gross_margin == '--':
                a.gross_margin = 0.0
            if a.operating_profit_ratio == '--':
                a.operating_profit_ratio = 0.0
            if b.inventory_turnover_ratio == '--':
                b.inventory_turnover_ratio = 0.0
            if b.fixed_asset_turnover_ratio == '--':
                b.fixed_asset_turnover_ratio = 0.0
            if b.accounts_receivable_turnover_ratio == '--':
                b.accounts_receivable_turnover_ratio = 0.0
            if c.net_profit_growth_margin == '--':
                c.net_profit_growth_margin = 0.0
            if c.revenue_growth_ratio == '--':
                c.revenue_growth_ratio = 0.0
            a.net_profit_margin = float(a.net_profit_margin)
            a.gross_margin = float(a.gross_margin)
            a.operating_profit_ratio = float(a.operating_profit_ratio)
            b.inventory_turnover_ratio = float(b.inventory_turnover_ratio)
            b.fixed_asset_turnover_ratio = float(b.fixed_asset_turnover_ratio)
            b.accounts_receivable_turnover_ratio = float(b.accounts_receivable_turnover_ratio)
            c.net_profit_growth_margin = float(c.net_profit_growth_margin)
            c.revenue_growth_ratio = float(c.revenue_growth_ratio)
            data.append([a.net_profit_margin, a.gross_margin, a.operating_profit_ratio, b.fixed_asset_turnover_ratio, b.inventory_turnover_ratio, b.accounts_receivable_turnover_ratio, c.net_profit_growth_margin, c.revenue_growth_ratio])
            target.append(a.eps)
     # svr = LinearRegression()
     # svr.fit(data, target)
     predict = []
     # for i in range(5, -1, -1):
     #      predict.append(round(svr.predict(data)[i], ndigits=2))
     # score = round(svr.score(data, target), ndigits=2)
     year = str(year)
     past = RobotRatio1Q.objects.filter(stock_id=stock, date__startswith=year).order_by('date')
     year = int(year)
     year = str(year-1)
     past2 = RobotRatio1Q.objects.filter(stock_id=stock, date__startswith=year).order_by('date')
     for i in range(3):
         set.append(past2[i])
     for i in past:
         set.append(i)
     return predict, search, set, avg, std, cn, #score, round(svr.predict(data)[0], ndigits=2)-0.21

def predict_eps_year(stock):
     category = RobotInformation.objects.get(stock_id=stock).category
     cn = RobotCategory.objects.get(category_id=category).category_name
     search = RobotInformation.objects.get(stock_id=stock).co_name
     data = []
     target = []
     epss = []
     for i in RobotInformation.objects.filter(category=category):
         for d in RobotRatio1.objects.filter(stock_id=i.stock_id):
            if d.eps == '--':
                d.eps = 0.0
            else:
                d.eps = float(d.eps)
            epss.append(d.eps)
     avg = round(np.mean(epss), ndigits=2)
     std = round(np.std(epss), ndigits=2)
     year = datetime.now().year
     for i in range(year-1, year-4, -1):
        for a in RobotRatio1.objects.filter(stock_id=stock, date__startswith=i).order_by('-date'):
            date = a.date
            b = RobotRatio3.objects.get(stock_id=stock, date=date)
            c = RobotRatio2.objects.get(stock_id=stock, date=date)
            a.eps = float(a.eps)
            if a.net_profit_margin == '--':
                a.net_profit_margin = 0.0
            if a.gross_margin == '--':
                a.gross_margin = 0.0
            if a.operating_profit_ratio == '--':
                a.operating_profit_ratio = 0.0
            if b.inventory_turnover_ratio == '--':
                b.inventory_turnover_ratio = 0.0
            if b.fixed_asset_turnover_ratio == '--':
                b.fixed_asset_turnover_ratio = 0.0
            if b.accounts_receivable_turnover_ratio == '--':
                b.accounts_receivable_turnover_ratio = 0.0
            if c.net_profit_growth_margin == '--':
                c.net_profit_growth_margin = 0.0
            if c.revenue_growth_ratio == '--':
                c.revenue_growth_ratio = 0.0
            a.net_profit_margin = float(a.net_profit_margin)
            a.gross_margin = float(a.gross_margin)
            a.operating_profit_ratio = float(a.operating_profit_ratio)
            b.inventory_turnover_ratio = float(b.inventory_turnover_ratio)
            b.fixed_asset_turnover_ratio = float(b.fixed_asset_turnover_ratio)
            b.accounts_receivable_turnover_ratio = float(b.accounts_receivable_turnover_ratio)
            c.net_profit_growth_margin = float(c.net_profit_growth_margin)
            c.revenue_growth_ratio = float(c.revenue_growth_ratio)
            data.append([a.net_profit_margin, a.gross_margin, a.operating_profit_ratio, b.fixed_asset_turnover_ratio, b.inventory_turnover_ratio, b.accounts_receivable_turnover_ratio, c.net_profit_growth_margin, c.revenue_growth_ratio])
            target.append(a.eps)
     # svr = LinearRegression()
     # svr.fit(data, target)
     predict = []
     # for i in range(2, -1, -1):
     #     predict.append(round(svr.predict(data)[i], ndigits=2))
     # score = round(svr.score(data, target), ndigits=2)
     past = RobotRatio1.objects.filter(stock_id=stock).order_by('date')[6:]
     return predict, search, past, avg, std, cn, #score, svr.predict(data)[0]


def predict_eps_season2(stock):
     #category = Information.objects.get(stock_id=stock).category_id
     cn = RobotCategory.objects.get(category_name='半導體業').category_id
     #search = Information.objects.get(stock_id=stock).co_name

     epss = []
     for i in RobotInformation.objects.filter(category=cn):
         for d in RobotRatio1Q.objects.filter(stock_id=i.stock_id):
            if d.eps == '--':
                d.eps = 0.0
            else:
                d.eps = float(d.eps)
            epss.append(d.eps)
     avg = round(np.mean(epss), ndigits=2)
     std = round(np.std(epss), ndigits=2)
     set = []
     year = datetime.now().year
     for i2 in stock:
         data = []
         target = []
         for i in range(year, year-3, -1):
            for a in RobotRatio1Q.objects.filter(stock_id=i2, date__startswith=i).order_by('-date'):
                date = a.date
                b = RobotRatio3Q.objects.get(stock_id=i2, date=date)
                c = RobotRatio2Q.objects.get(stock_id=i2, date=date)
                a.eps = float(a.eps)
                if a.net_profit_margin == '--':
                    a.net_profit_margin = 0.0
                if a.gross_margin == '--':
                    a.gross_margin = 0.0
                if a.operating_profit_ratio == '--':
                    a.operating_profit_ratio = 0.0
                if b.inventory_turnover_ratio == '--':
                    b.inventory_turnover_ratio = 0.0
                if b.fixed_asset_turnover_ratio == '--':
                    b.fixed_asset_turnover_ratio = 0.0
                if b.accounts_receivable_turnover_ratio == '--':
                    b.accounts_receivable_turnover_ratio = 0.0
                if c.net_profit_growth_margin == '--':
                    c.net_profit_growth_margin = 0.0
                if c.revenue_growth_ratio == '--':
                    c.revenue_growth_ratio = 0.0
                a.net_profit_margin = float(a.net_profit_margin)
                a.gross_margin = float(a.gross_margin)
                a.operating_profit_ratio = float(a.operating_profit_ratio)
                b.inventory_turnover_ratio = float(b.inventory_turnover_ratio)
                b.fixed_asset_turnover_ratio = float(b.fixed_asset_turnover_ratio)
                b.accounts_receivable_turnover_ratio = float(b.accounts_receivable_turnover_ratio)
                c.net_profit_growth_margin = float(c.net_profit_growth_margin)
                c.revenue_growth_ratio = float(c.revenue_growth_ratio)
                data.append([a.net_profit_margin, a.gross_margin, a.operating_profit_ratio, b.fixed_asset_turnover_ratio, b.inventory_turnover_ratio, b.accounts_receivable_turnover_ratio, c.net_profit_growth_margin, c.revenue_growth_ratio])
                target.append(a.eps)
         # svr = LinearRegression()
         # svr.fit(data, target)
         # if svr.predict(data)[0] > avg:
         #    set.append(1)
         else:
            set.append(0)
     return set

######################
# 原版 第二季(有錯> <)
def evalOneMax2(individual, stock_idlist, type, mo):
    fitness=0
    count=0
    price=0
    stock_count=""
    invest=0
    #print(individual)  染色體(50種投資組合)

    for j in range(0,len(individual), 5):
        print(individual[j])
        print(stock_idlist[int(j/5)])
        if individual[j] == 0 or stock_idlist[int(j/5)] == '4552':
            continue
        if individual[j] == 1 and individual[j+1] == 0 and individual[j+2] == 0 and individual[j+3] == 0 and individual[j+4] == 0:
            continue
        elif individual[j] == 1: # 2015第一期 # 2015第二期
            stock_id=stock_idlist[int(j/5)]
            stock_count=str(individual[j+1])+str(individual[j+2])+str(individual[j+3])+str(individual[j+4])
            stock_count=int(stock_count,2)
            count=count+1
            # price = float(Transaction_info.objects.get(date='20150105', stock_id=stock_id).the_close)*1000 #股價
            price = float(Transaction_info.objects.get(date='20150401', stock_id=stock_id).the_close)*1000 #股價
            invest_t=stock_count*price
            invest=invest+invest_t
            g1 = float(Ratio1_Q.objects.get(date='201501', stock_id=stock_id).eps)
            g2 = Ratio2_Q.objects.get(date='201501', stock_id=stock_id).operating_profit_growth_ratio
            g3 = Ratio4_Q.objects.get(date='201501', stock_id=stock_id).debt_ratio
            g4 = Ratio1_Q.objects.get(date='201501', stock_id=stock_id).ROE
            g5 = Ratio2_Q.objects.get(date='201501', stock_id=stock_id).revenue_growth_ratio
            g6 = Ratio3_Q.objects.get(date='201501', stock_id=stock_id).accounts_receivable_turnover_ratio
            g7 = PE.objects.get(date='2015Q1', stock_id=stock_id).pe_for_four_season
            if g7 == '--':
                g7 = 0.0
            else:
                g7 = float(g7)
            if g4 == '--':
                g4 = 0.0
            else:
                g4 = float(g4)
            if g5 == '--':
                g5 = 0.0
            else:
                g5 = float(g5)
            if g2 == '--':
                g2 = 0.0
            else:
                g2 = float(g2)
            if g6 == '--':
                g6 = 0.0
            else:
                g6 = float(g6)
            if g3 == '--':
                g3 = 0.0
            else:
                g3 = float(g3)
            if g1 > 1.0:
                g1 = 50
            else:
                g1 = -50
            if g2 > 10.0:
                g2 = 100
            else:
                g2 = -100
            if g3 < 55.0:
                g3 = 50
            else:
                g3 = -50
            if g4 > 5.0:
                g4 = 100
            else:
                g4 = -100
            if g5 > 10.0:
                g5 = 50
            else:
                g5 = -50
            if g6 > 1.5:
                g6 = 100
            else:
                g6 = -100
            if g7 < 20.0:
                g7 = 50
            else:
                g7 = -50

            type = int(type)
            g8 = 0
            if type > 3:
                '''pe_for_four_season = PE.objects.get(date='2015Q1', stock_id=stock_id).pe_for_four_season
                if pe_for_four_season == '--':
                    pe_for_four_season = 0.0
                else:
                    pe_for_four_season = float(pe_for_four_season)'''
                # evl = float(Cash_Flows_Q.objects.get(date='201501', stock_id=stock_id).free_cash_flows)*0.45 + pe_for_four_season*0.55
                if PE.objects.get(date='2015Q2', stock_id=stock_id).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=stock_id).eps == '--':
                    evl = (float(Transaction_info.objects.get(date='20150401', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=stock_id).the_close))/3.0
                else:
                    evl = float(PE.objects.get(date='2015Q2', stock_id=stock_id).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=stock_id).eps) #本月(季)本益比*下月(季)每股盈餘
                #a = Share(stock_id+'.TW').get_price()
                a = Transaction_info.objects.filter(date__startswith='201502', stock_id=stock_id).order_by('date')[0].the_close
                if a == '--':
                    a = 0.0
                else:
                    a = float(a)
                # model = (evl-a)/evl
                model = (a-evl)/evl
                if model >= 0.25:
                    g8 = -350
                elif model >= 0.1 and model < 0.25:
                    g8 = -150
                elif model >= -0.1 and model < 0.1:
                    g8 = 0
                elif model >= -0.25 and model < -0.1:
                    g8 = 150
                else:
                    g8 = 350
                macd1 = Technology_Index.objects.get(date='20150401', stock_id=stock_id).day_MACD
                macd2 = Technology_Index.objects.get(date='20150402', stock_id=stock_id).day_MACD
                macd3 = Technology_Index.objects.get(date='20150407', stock_id=stock_id).day_MACD
                if macd1 == '--':
                    macd1 = 0.0
                else:
                    macd1 = float(macd1)
                if macd2 == '--':
                    macd2 = 0.0
                else:
                    macd2 = float(macd2)
                if macd3 == '--':
                    macd3 = 0.0
                else:
                    macd3 = float(macd3)
                if macd2 > macd1 and macd3 > macd2:
                    g8 = g8 + 50
                elif macd3 > macd2:
                    g8 = g8 - 20
                else:
                    g8 = g8 - 50
                k = Technology_Index.objects.get(date='20150401', stock_id=stock_id).day_K
                d = Technology_Index.objects.get(date='20150401', stock_id=stock_id).day_D
                if k == '--':
                    kd = 0.0
                else:
                    k = float(k)
                if d == '--':
                    d = 0.0
                else:
                    d = float(d)
                if k > d:
                    g8 = g8 + 50
                elif k < d:
                    g8 = g8 - 50
            elif type < 3:
                pe_for_four_season = PE.objects.get(date='2015Q1', stock_id=stock_id).pe_for_four_season
                if pe_for_four_season == '--':
                    pe_for_four_season = 0.0
                else:
                    pe_for_four_season = float(pe_for_four_season)
                #evl = float(Cash_Flows_Q.objects.get(date='201501', stock_id=stock_id).free_cash_flows)*0.45 + pe_for_four_season*0.55
                if PE.objects.get(date='2015Q2', stock_id=stock_id).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=stock_id).eps == '--':
                    evl = (float(Transaction_info.objects.get(date='20150401', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=stock_id).the_close))/3.0
                else:
                    evl = float(PE.objects.get(date='2015Q2', stock_id=stock_id).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=stock_id).eps) #本月(季)本益比*下月(季)每股盈餘
                #a = Share(stock_id+'.TW').get_price()
                a = Transaction_info.objects.filter(date__startswith='201502', stock_id=stock_id).order_by('date')[0].the_close
                if a == '--':
                    a = 0.0
                else:
                    a = float(a)
                #model = (evl-a)/evl
                model = (a-evl)/evl
                if model >= 0.25:
                    g8 = -400
                elif model >= 0.1 and model < 0.25:
                    g8 = -200
                elif model >= -0.1 and model < 0.1:
                    g8 = 0
                elif model >= -0.25 and model < -0.1:
                    g8 = 200
                else:
                    g8 = 400
                macd1 = Technology_Index.objects.get(date='20150401', stock_id=stock_id).month_MACD
                macd2 = Technology_Index.objects.get(date='20150402', stock_id=stock_id).month_MACD
                macd3 = Technology_Index.objects.get(date='20150407', stock_id=stock_id).month_MACD
                if macd1 == '--':
                    macd1 = 0.0
                else:
                    macd1 = float(macd1)
                if macd2 == '--':
                    macd2 = 0.0
                else:
                    macd2 = float(macd2)
                if macd3 == '--':
                    macd3 = 0.0
                else:
                    macd3 = float(macd3)
                if macd2 > macd1 and macd3 > macd2:
                    g8 = g8 + 50
                else:
                    g8 = g8 - 50
                k = Technology_Index.objects.get(date='20150401', stock_id=stock_id).month_K
                d = Technology_Index.objects.get(date='20150401', stock_id=stock_id).month_D
                if k == '--':
                    kd = 0.0
                else:
                    k = float(k)
                if d == '--':
                    d = 0.0
                else:
                    d = float(d)
                if k > d:
                    g8 = g8 + 50
                elif k < d:
                    g8 = g8 - 50
            g9 = 0
            pe_for_four_season = PE.objects.get(date='2015Q1', stock_id=stock_id).pe_for_four_season
            if pe_for_four_season == '--':
                pe_for_four_season = 0.0
            else:
                pe_for_four_season = float(pe_for_four_season)
            #evl = float(Cash_Flows_Q.objects.get(date='201501', stock_id=stock_id).free_cash_flows)*0.45 + pe_for_four_season*0.55
            if PE.objects.get(date='2015Q2', stock_id=stock_id).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=stock_id).eps == '--':
                    evl = (float(Transaction_info.objects.get(date='20150401', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=stock_id).the_close))/3.0
            else:
                    evl = float(PE.objects.get(date='2015Q2', stock_id=stock_id).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=stock_id).eps) #本月(季)本益比*下月(季)每股盈餘
            #a = Share(stock_id+'.TW').get_price()
            #if a is None:
            #    a = 0.0
            a = Transaction_info.objects.filter(date__startswith='201502', stock_id=stock_id).order_by('date')[0].the_close
            if a == '--':
                a = 0.0
            else:
                a = float(a)
            r = (a-evl)/evl
            if r >= 0.25:
                g9 = -400
            elif r >= 0.1 and r < 0.25:
                g9 = -200
            elif r >= -0.1 and r < 0.1:
                g9 = 0
            elif r >= -0.25 and r < -0.1:
                g9 = 200
            else:
                g9 = 400

            fitness = g1 + g2 + g3 + g4 + g5 + g6 + g7 + g8 + g9
    g10 = 0
    money = int(mo)*10000 #500(萬)
    invest = int(invest)
    #if invest <= money*1.05 and invest >= money*0.95 and count >= 8 and count <=10:
        #g10 = 78000
    if invest > money*3:
        g10 = -40000
    elif invest >= money*2:
        if count >= 12:
            g10 = -35000
        elif count >= 10 and count < 12:
            g10 = -30000
        elif count < 10 and count > 8:
            g10 = -20000
        else:
            g10 = -30000
    elif invest >= money*1.5 and invest < money*2 : #500(萬)
        if count >= 12:
            g10 = -30000
        elif count >= 10 and count < 12:
            g10 = -25000#35000
        elif count < 10 and count > 8:
            g10 = -20000#40000
        else:
            g10 = -25000#20000
    elif invest >= money*1.2 and invest < money*1.5 : #500(萬)
        if count >= 12:
            g10 = -20000
        elif count >= 10 and count < 12:
            g10 = 25000#35000
        elif count < 10 and count > 8:
            g10 = 30000#40000
        else:
            g10 = 10000#20000
    elif invest >= money and invest < money*1.2 : #500(萬)
        if count >= 12:
            g10 = -10000
        elif count >= 10 and count < 12:
            g10 = 65000#35000
        elif count < 10 and count > 8:
            g10 = 70000#40000
        else:
            g10 = 60000#20000
    elif invest >= money*0.95 and invest < money:
        if count >= 12:
            g10 = -5000
        elif count >= 10 and count < 12:
            g10 = 70000
        elif count < 10 and count > 8:
            g10 = 75000
        else:
            g10 = 60000
    elif invest >= money*0.8 and invest < money*0.95:
        if count >= 12:
            g10 = -6000
        elif count >= 10 and count < 12:
            g10 = 60000
        elif count < 10 and count > 8:
            g10 = 65000
        else:
            g10 = 55000
    else:
        g10 = 0
    fitness = fitness + g10
    '''if fitness < 0:
        fitness = 0
        return fitness,
    else:'''
    return fitness,

# 第三季
def evalOneMax3(individual, stock_idlist, type, mo):
    fitness=0
    count=0
    price=0
    stock_count=""
    invest=0
    #print(individual)  染色體(50種投資組合)

    for j in range(0,len(individual), 5):
        print(individual[j])
        print(stock_idlist[int(j/5)])
        if individual[j] == 0 or stock_idlist[int(j/5)] == '4552':
            continue
        if individual[j] == 1 and individual[j+1] == 0 and individual[j+2] == 0 and individual[j+3] == 0 and individual[j+4] == 0:
            continue
        elif individual[j] == 1: # 2015第一期 # 2015第二期
            stock_id=stock_idlist[int(j/5)]
            stock_count=str(individual[j+1])+str(individual[j+2])+str(individual[j+3])+str(individual[j+4])
            stock_count=int(stock_count,2)
            count=count+1
            # price = float(Transaction_info.objects.get(date='20150105', stock_id=stock_id).the_close)*1000 #股價
            price = float(Transaction_info.objects.get(date='20150701', stock_id=stock_id).the_close)*1000 #股價
            invest_t=stock_count*price
            invest=invest+invest_t
            g1 = float(Ratio1_Q.objects.get(date='201503', stock_id=stock_id).eps)
            g2 = Ratio2_Q.objects.get(date='201503', stock_id=stock_id).operating_profit_growth_ratio
            g3 = Ratio4_Q.objects.get(date='201503', stock_id=stock_id).debt_ratio
            g4 = Ratio1_Q.objects.get(date='201503', stock_id=stock_id).ROE
            g5 = Ratio2_Q.objects.get(date='201503', stock_id=stock_id).revenue_growth_ratio
            g6 = Ratio3_Q.objects.get(date='201503', stock_id=stock_id).accounts_receivable_turnover_ratio
            g7 = PE.objects.get(date='2015Q3', stock_id=stock_id).pe_for_four_season
            if g7 == '--':
                g7 = 0.0
            else:
                g7 = float(g7)
            if g4 == '--':
                g4 = 0.0
            else:
                g4 = float(g4)
            if g5 == '--':
                g5 = 0.0
            else:
                g5 = float(g5)
            if g2 == '--':
                g2 = 0.0
            else:
                g2 = float(g2)
            if g6 == '--':
                g6 = 0.0
            else:
                g6 = float(g6)
            if g3 == '--':
                g3 = 0.0
            else:
                g3 = float(g3)
            if g1 > 1.0:
                g1 = 50
            else:
                g1 = -50
            if g2 > 10.0:
                g2 = 100
            else:
                g2 = -100
            if g3 < 55.0:
                g3 = 50
            else:
                g3 = -50
            if g4 > 5.0:
                g4 = 100
            else:
                g4 = -100
            if g5 > 10.0:
                g5 = 50
            else:
                g5 = -50
            if g6 > 1.5:
                g6 = 100
            else:
                g6 = -100
            if g7 < 20.0:
                g7 = 50
            else:
                g7 = -50

            type = int(type)
            g8 = 0
            if type > 3:
                pe_for_four_season = PE.objects.get(date='2015Q3', stock_id=stock_id).pe_for_four_season
                if pe_for_four_season == '--':
                    pe_for_four_season = 0.0
                else:
                    pe_for_four_season = float(pe_for_four_season)
                evl = float(Cash_Flows_Q.objects.get(date='201503', stock_id=stock_id).free_cash_flows)*0.45 + pe_for_four_season*0.55
                '''if PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps == '--':
                    evl = (float(Transaction_info.objects.get(date='20150701', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150702', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150703', stock_id=stock_id).the_close))/3.0
                else:
                    evl = float(PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps) #本月(季)本益比*下月(季)每股盈餘
                '''
                #a = Share(stock_id+'.TW').get_price()
                a = Transaction_info.objects.filter(date__startswith='201507', stock_id=stock_id).order_by('date')[0].the_close
                if a == '--':
                    a = 0.0
                else:
                    a = float(a)
                model = (evl-a)/evl
                #model = (a-evl)/evl
                if model >= 0.25:
                    g8 = -350
                elif model >= 0.1 and model < 0.25:
                    g8 = -150
                elif model >= -0.1 and model < 0.1:
                    g8 = 0
                elif model >= -0.25 and model < -0.1:
                    g8 = 150
                else:
                    g8 = 350
                macd1 = Technology_Index.objects.get(date='20150701', stock_id=stock_id).day_MACD
                macd2 = Technology_Index.objects.get(date='20150702', stock_id=stock_id).day_MACD
                macd3 = Technology_Index.objects.get(date='20150703', stock_id=stock_id).day_MACD
                if macd1 == '--':
                    macd1 = 0.0
                else:
                    macd1 = float(macd1)
                if macd2 == '--':
                    macd2 = 0.0
                else:
                    macd2 = float(macd2)
                if macd3 == '--':
                    macd3 = 0.0
                else:
                    macd3 = float(macd3)
                if macd2 > macd1 and macd3 > macd2:
                    g8 = g8 + 50
                elif macd3 > macd2:
                    g8 = g8 - 20
                else:
                    g8 = g8 - 50
                k = Technology_Index.objects.get(date='20150701', stock_id=stock_id).day_K
                d = Technology_Index.objects.get(date='20150701', stock_id=stock_id).day_D
                if k == '--':
                    kd = 0.0
                else:
                    k = float(k)
                if d == '--':
                    d = 0.0
                else:
                    d = float(d)
                if k > d:
                    g8 = g8 + 50
                elif k < d:
                    g8 = g8 - 50
            elif type < 3:
                pe_for_four_season = PE.objects.get(date='2015Q3', stock_id=stock_id).pe_for_four_season
                if pe_for_four_season == '--':
                    pe_for_four_season = 0.0
                else:
                    pe_for_four_season = float(pe_for_four_season)
                evl = float(Cash_Flows_Q.objects.get(date='201503', stock_id=stock_id).free_cash_flows)*0.45 + pe_for_four_season*0.55
                '''if PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps == '--':
                    evl = (float(Transaction_info.objects.get(date='20150701', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150702', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150703', stock_id=stock_id).the_close))/3.0
                else:
                    evl = float(PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps) #本月(季)本益比*下月(季)每股盈餘
                '''
                #a = Share(stock_id+'.TW').get_price()
                a = Transaction_info.objects.filter(date__startswith='201507', stock_id=stock_id).order_by('date')[0].the_close
                if a == '--':
                    a = 0.0
                else:
                    a = float(a)
                model = (evl-a)/evl
                #model = (a-evl)/evl
                if model >= 0.25:
                    g8 = -400
                elif model >= 0.1 and model < 0.25:
                    g8 = -200
                elif model >= -0.1 and model < 0.1:
                    g8 = 0
                elif model >= -0.25 and model < -0.1:
                    g8 = 200
                else:
                    g8 = 400
                macd1 = Technology_Index.objects.get(date='20150701', stock_id=stock_id).month_MACD
                macd2 = Technology_Index.objects.get(date='20150702', stock_id=stock_id).month_MACD
                macd3 = Technology_Index.objects.get(date='20150703', stock_id=stock_id).month_MACD
                if macd1 == '--':
                    macd1 = 0.0
                else:
                    macd1 = float(macd1)
                if macd2 == '--':
                    macd2 = 0.0
                else:
                    macd2 = float(macd2)
                if macd3 == '--':
                    macd3 = 0.0
                else:
                    macd3 = float(macd3)
                if macd2 > macd1 and macd3 > macd2:
                    g8 = g8 + 50
                else:
                    g8 = g8 - 50
                k = Technology_Index.objects.get(date='20150701', stock_id=stock_id).month_K
                d = Technology_Index.objects.get(date='20150701', stock_id=stock_id).month_D
                if k == '--':
                    kd = 0.0
                else:
                    k = float(k)
                if d == '--':
                    d = 0.0
                else:
                    d = float(d)
                if k > d:
                    g8 = g8 + 50
                elif k < d:
                    g8 = g8 - 50
            g9 = 0
            pe_for_four_season = PE.objects.get(date='2015Q3', stock_id=stock_id).pe_for_four_season
            if pe_for_four_season == '--':
                pe_for_four_season = 0.0
            else:
                pe_for_four_season = float(pe_for_four_season)
            evl = float(Cash_Flows_Q.objects.get(date='201503', stock_id=stock_id).free_cash_flows)*0.45 + pe_for_four_season*0.55
            '''if PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps == '--':
                    evl = (float(Transaction_info.objects.get(date='20150701', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150702', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150703', stock_id=stock_id).the_close))/3.0
            else:
                    evl = float(PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps) #本月(季)本益比*下月(季)每股盈餘
            '''
            #a = Share(stock_id+'.TW').get_price()
            #if a is None:
            #    a = 0.0
            a = Transaction_info.objects.filter(date__startswith='201503', stock_id=stock_id).order_by('date')[0].the_close
            if a == '--':
                a = 0.0
            else:
                a = float(a)
            #r = (a-evl)/evl
            r = (evl-a)/evl
            if r >= 0.25:
                g9 = -400
            elif r >= 0.1 and r < 0.25:
                g9 = -200
            elif r >= -0.1 and r < 0.1:
                g9 = 0
            elif r >= -0.25 and r < -0.1:
                g9 = 200
            else:
                g9 = 400

            fitness = g1 + g2 + g3 + g4 + g5 + g6 + g7 + g8 + g9
    g10 = 0
    money = int(mo)*10000 #500(萬)
    invest = int(invest)
    #if invest <= money*1.05 and invest >= money*0.95 and count >= 8 and count <=10:
        #g10 = 78000
    if invest > money*3:
        g10 = -40000
    elif invest >= money*2:
        if count >= 12:
            g10 = -35000
        elif count >= 10 and count < 12:
            g10 = -30000
        elif count < 10 and count > 8:
            g10 = -20000
        else:
            g10 = -30000
    elif invest >= money*1.5 and invest < money*2 : #500(萬)
        if count >= 12:
            g10 = -30000
        elif count >= 10 and count < 12:
            g10 = -25000#35000
        elif count < 10 and count > 8:
            g10 = -20000#40000
        else:
            g10 = -25000#20000
    elif invest >= money*1.2 and invest < money*1.5 : #500(萬)
        if count >= 12:
            g10 = -20000
        elif count >= 10 and count < 12:
            g10 = 25000#35000
        elif count < 10 and count > 8:
            g10 = 30000#40000
        else:
            g10 = 10000#20000
    elif invest >= money and invest < money*1.2 : #500(萬)
        if count >= 12:
            g10 = -10000
        elif count >= 10 and count < 12:
            g10 = 65000#35000
        elif count < 10 and count > 8:
            g10 = 70000#40000
        else:
            g10 = 60000#20000
    elif invest >= money*0.95 and invest < money:
        if count >= 12:
            g10 = -5000
        elif count >= 10 and count < 12:
            g10 = 70000
        elif count < 10 and count > 8:
            g10 = 75000
        else:
            g10 = 60000
    elif invest >= money*0.8 and invest < money*0.95:
        if count >= 12:
            g10 = -6000
        elif count >= 10 and count < 12:
            g10 = 60000
        elif count < 10 and count > 8:
            g10 = 65000
        else:
            g10 = 55000
    else:
        g10 = 0
    fitness = fitness + g10
    '''if fitness < 0:
        fitness = 0
        return fitness,
    else:'''
    return fitness,

# 第四季
def evalOneMax4(individual, stock_idlist, type, mo):
    fitness=0
    count=0
    price=0
    stock_count=""
    invest=0
    #print(individual)  染色體(50種投資組合)

    for j in range(0,len(individual), 5):
        print(individual[j])
        print(stock_idlist[int(j/5)])
        if individual[j] == 0 or stock_idlist[int(j/5)] == '4552':
            continue
        if individual[j] == 1 and individual[j+1] == 0 and individual[j+2] == 0 and individual[j+3] == 0 and individual[j+4] == 0:
            continue
        elif individual[j] == 1: # 2015第一期 # 2015第二期
            stock_id=stock_idlist[int(j/5)]
            stock_count=str(individual[j+1])+str(individual[j+2])+str(individual[j+3])+str(individual[j+4])
            stock_count=int(stock_count,2)
            count=count+1
            # price = float(Transaction_info.objects.get(date='20150105', stock_id=stock_id).the_close)*1000 #股價
            price = float(Transaction_info.objects.get(date='20150701', stock_id=stock_id).the_close)*1000 #股價
            invest_t=stock_count*price
            invest=invest+invest_t
            g1 = float(Ratio1_Q.objects.get(date='201504', stock_id=stock_id).eps)
            g2 = Ratio2_Q.objects.get(date='201504', stock_id=stock_id).operating_profit_growth_ratio
            g3 = Ratio4_Q.objects.get(date='201504', stock_id=stock_id).debt_ratio
            g4 = Ratio1_Q.objects.get(date='201504', stock_id=stock_id).ROE
            g5 = Ratio2_Q.objects.get(date='201504', stock_id=stock_id).revenue_growth_ratio
            g6 = Ratio3_Q.objects.get(date='201504', stock_id=stock_id).accounts_receivable_turnover_ratio
            g7 = PE.objects.get(date='2015Q4', stock_id=stock_id).pe_for_four_season
            if g7 == '--':
                g7 = 0.0
            else:
                g7 = float(g7)
            if g4 == '--':
                g4 = 0.0
            else:
                g4 = float(g4)
            if g5 == '--':
                g5 = 0.0
            else:
                g5 = float(g5)
            if g2 == '--':
                g2 = 0.0
            else:
                g2 = float(g2)
            if g6 == '--':
                g6 = 0.0
            else:
                g6 = float(g6)
            if g3 == '--':
                g3 = 0.0
            else:
                g3 = float(g3)
            if g1 > 1.0:
                g1 = 50
            else:
                g1 = -50
            if g2 > 10.0:
                g2 = 100
            else:
                g2 = -100
            if g3 < 55.0:
                g3 = 50
            else:
                g3 = -50
            if g4 > 5.0:
                g4 = 100
            else:
                g4 = -100
            if g5 > 10.0:
                g5 = 50
            else:
                g5 = -50
            if g6 > 1.5:
                g6 = 100
            else:
                g6 = -100
            if g7 < 20.0:
                g7 = 50
            else:
                g7 = -50

            type = int(type)
            g8 = 0
            if type > 3:
                pe_for_four_season = PE.objects.get(date='2015Q4', stock_id=stock_id).pe_for_four_season
                if pe_for_four_season == '--':
                    pe_for_four_season = 0.0
                else:
                    pe_for_four_season = float(pe_for_four_season)
                evl = float(Cash_Flows_Q.objects.get(date='201504', stock_id=stock_id).free_cash_flows)*0.45 + pe_for_four_season*0.55
                '''if PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps == '--':
                    evl = (float(Transaction_info.objects.get(date='20150701', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150702', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150703', stock_id=stock_id).the_close))/3.0
                else:
                    evl = float(PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps) #本月(季)本益比*下月(季)每股盈餘
                '''
                #a = Share(stock_id+'.TW').get_price()
                a = Transaction_info.objects.filter(date__startswith='201510', stock_id=stock_id).order_by('date')[0].the_close
                if a == '--':
                    a = 0.0
                else:
                    a = float(a)
                model = (evl-a)/evl
                #model = (a-evl)/evl
                if model >= 0.25:
                    g8 = -350
                elif model >= 0.1 and model < 0.25:
                    g8 = -150
                elif model >= -0.1 and model < 0.1:
                    g8 = 0
                elif model >= -0.25 and model < -0.1:
                    g8 = 150
                else:
                    g8 = 350
                macd1 = Technology_Index.objects.get(date='20151001', stock_id=stock_id).day_MACD
                macd2 = Technology_Index.objects.get(date='20151002', stock_id=stock_id).day_MACD
                macd3 = Technology_Index.objects.get(date='20151005', stock_id=stock_id).day_MACD
                if macd1 == '--':
                    macd1 = 0.0
                else:
                    macd1 = float(macd1)
                if macd2 == '--':
                    macd2 = 0.0
                else:
                    macd2 = float(macd2)
                if macd3 == '--':
                    macd3 = 0.0
                else:
                    macd3 = float(macd3)
                if macd2 > macd1 and macd3 > macd2:
                    g8 = g8 + 50
                elif macd3 > macd2:
                    g8 = g8 - 20
                else:
                    g8 = g8 - 50
                k = Technology_Index.objects.get(date='20151001', stock_id=stock_id).day_K
                d = Technology_Index.objects.get(date='20151002', stock_id=stock_id).day_D
                if k == '--':
                    kd = 0.0
                else:
                    k = float(k)
                if d == '--':
                    d = 0.0
                else:
                    d = float(d)
                if k > d:
                    g8 = g8 + 50
                elif k < d:
                    g8 = g8 - 50
            elif type < 3:
                pe_for_four_season = PE.objects.get(date='2015Q4', stock_id=stock_id).pe_for_four_season
                if pe_for_four_season == '--':
                    pe_for_four_season = 0.0
                else:
                    pe_for_four_season = float(pe_for_four_season)
                evl = float(Cash_Flows_Q.objects.get(date='201504', stock_id=stock_id).free_cash_flows)*0.45 + pe_for_four_season*0.55
                '''if PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps == '--':
                    evl = (float(Transaction_info.objects.get(date='20150701', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150702', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150703', stock_id=stock_id).the_close))/3.0
                else:
                    evl = float(PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps) #本月(季)本益比*下月(季)每股盈餘
                '''
                #a = Share(stock_id+'.TW').get_price()
                a = Transaction_info.objects.filter(date__startswith='201510', stock_id=stock_id).order_by('date')[0].the_close
                if a == '--':
                    a = 0.0
                else:
                    a = float(a)
                model = (evl-a)/evl
                #model = (a-evl)/evl
                if model >= 0.25:
                    g8 = -400
                elif model >= 0.1 and model < 0.25:
                    g8 = -200
                elif model >= -0.1 and model < 0.1:
                    g8 = 0
                elif model >= -0.25 and model < -0.1:
                    g8 = 200
                else:
                    g8 = 400
                macd1 = Technology_Index.objects.get(date='20151001', stock_id=stock_id).month_MACD
                macd2 = Technology_Index.objects.get(date='20151002', stock_id=stock_id).month_MACD
                macd3 = Technology_Index.objects.get(date='20151005', stock_id=stock_id).month_MACD
                if macd1 == '--':
                    macd1 = 0.0
                else:
                    macd1 = float(macd1)
                if macd2 == '--':
                    macd2 = 0.0
                else:
                    macd2 = float(macd2)
                if macd3 == '--':
                    macd3 = 0.0
                else:
                    macd3 = float(macd3)
                if macd2 > macd1 and macd3 > macd2:
                    g8 = g8 + 50
                else:
                    g8 = g8 - 50
                k = Technology_Index.objects.get(date='20151001', stock_id=stock_id).month_K
                d = Technology_Index.objects.get(date='20151001', stock_id=stock_id).month_D
                if k == '--':
                    kd = 0.0
                else:
                    k = float(k)
                if d == '--':
                    d = 0.0
                else:
                    d = float(d)
                if k > d:
                    g8 = g8 + 50
                elif k < d:
                    g8 = g8 - 50
            g9 = 0
            pe_for_four_season = PE.objects.get(date='2015Q4', stock_id=stock_id).pe_for_four_season
            if pe_for_four_season == '--':
                pe_for_four_season = 0.0
            else:
                pe_for_four_season = float(pe_for_four_season)
            evl = float(Cash_Flows_Q.objects.get(date='201504', stock_id=stock_id).free_cash_flows)*0.45 + pe_for_four_season*0.55
            '''if PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps == '--':
                    evl = (float(Transaction_info.objects.get(date='20150701', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150702', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150703', stock_id=stock_id).the_close))/3.0
            else:
                    evl = float(PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps) #本月(季)本益比*下月(季)每股盈餘
            '''
            #a = Share(stock_id+'.TW').get_price()
            #if a is None:
            #    a = 0.0
            a = Transaction_info.objects.filter(date__startswith='201510', stock_id=stock_id).order_by('date')[0].the_close
            if a == '--':
                a = 0.0
            else:
                a = float(a)
            #r = (a-evl)/evl
            r = (evl-a)/evl
            if r >= 0.25:
                g9 = -400
            elif r >= 0.1 and r < 0.25:
                g9 = -200
            elif r >= -0.1 and r < 0.1:
                g9 = 0
            elif r >= -0.25 and r < -0.1:
                g9 = 200
            else:
                g9 = 400

            fitness = g1 + g2 + g3 + g4 + g5 + g6 + g7 + g8 + g9
    g10 = 0
    money = int(mo)*10000 #500(萬)
    invest = int(invest)
    #if invest <= money*1.05 and invest >= money*0.95 and count >= 8 and count <=10:
        #g10 = 78000
    if invest > money*3:
        g10 = -40000
    elif invest >= money*2:
        if count >= 12:
            g10 = -35000
        elif count >= 10 and count < 12:
            g10 = -30000
        elif count < 10 and count > 8:
            g10 = -20000
        else:
            g10 = -30000
    elif invest >= money*1.5 and invest < money*2 : #500(萬)
        if count >= 12:
            g10 = -30000
        elif count >= 10 and count < 12:
            g10 = -25000#35000
        elif count < 10 and count > 8:
            g10 = -20000#40000
        else:
            g10 = -25000#20000
    elif invest >= money*1.2 and invest < money*1.5 : #500(萬)
        if count >= 12:
            g10 = -20000
        elif count >= 10 and count < 12:
            g10 = 25000#35000
        elif count < 10 and count > 8:
            g10 = 30000#40000
        else:
            g10 = 10000#20000
    elif invest >= money and invest < money*1.2 : #500(萬)
        if count >= 12:
            g10 = -10000
        elif count >= 10 and count < 12:
            g10 = 65000#35000
        elif count < 10 and count > 8:
            g10 = 70000#40000
        else:
            g10 = 60000#20000
    elif invest >= money*0.95 and invest < money:
        if count >= 12:
            g10 = -5000
        elif count >= 10 and count < 12:
            g10 = 70000
        elif count < 10 and count > 8:
            g10 = 75000
        else:
            g10 = 60000
    elif invest >= money*0.8 and invest < money*0.95:
        if count >= 12:
            g10 = -6000
        elif count >= 10 and count < 12:
            g10 = 60000
        elif count < 10 and count > 8:
            g10 = 65000
        else:
            g10 = 55000
    else:
        g10 = 0
    fitness = fitness + g10
    '''if fitness < 0:
        fitness = 0
        return fitness,
    else:'''
    return fitness,

# 2016第一季
def evalOneMax(individual, stock_idlist, type, mo):
    fitness=0
    count=0
    price=0
    stock_count=""
    invest=0
    #print(individual)  染色體(50種投資組合)

    for j in range(0,len(individual), 5):
        print(individual[j])
        print(stock_idlist[int(j/5)])
        if individual[j] == 0 or stock_idlist[int(j/5)] == '4552':
            continue
        if individual[j] == 1 and individual[j+1] == 0 and individual[j+2] == 0 and individual[j+3] == 0 and individual[j+4] == 0:
            continue
        elif individual[j] == 1: # 2015第一期 # 2015第二期
            stock_id=stock_idlist[int(j/5)]
            stock_count=str(individual[j+1])+str(individual[j+2])+str(individual[j+3])+str(individual[j+4])
            stock_count=int(stock_count,2)
            count=count+1
            # price = float(Transaction_info.objects.get(date='20150105', stock_id=stock_id).the_close)*1000 #股價
            price = float(Transaction_info.objects.get(date='20160104', stock_id=stock_id).the_close)*1000 #股價
            invest_t=stock_count*price
            invest=invest+invest_t
            g1 = float(Ratio1_Q.objects.get(date='201601', stock_id=stock_id).eps)
            g2 = Ratio2_Q.objects.get(date='201601', stock_id=stock_id).operating_profit_growth_ratio
            g3 = Ratio4_Q.objects.get(date='201601', stock_id=stock_id).debt_ratio
            g4 = Ratio1_Q.objects.get(date='201601', stock_id=stock_id).ROE
            g5 = Ratio2_Q.objects.get(date='201601', stock_id=stock_id).revenue_growth_ratio
            g6 = Ratio3_Q.objects.get(date='201601', stock_id=stock_id).accounts_receivable_turnover_ratio
            g7 = PE.objects.get(date='2016Q1', stock_id=stock_id).pe_for_four_season
            if g7 == '--':
                g7 = 0.0
            else:
                g7 = float(g7)
            if g4 == '--':
                g4 = 0.0
            else:
                g4 = float(g4)
            if g5 == '--':
                g5 = 0.0
            else:
                g5 = float(g5)
            if g2 == '--':
                g2 = 0.0
            else:
                g2 = float(g2)
            if g6 == '--':
                g6 = 0.0
            else:
                g6 = float(g6)
            if g3 == '--':
                g3 = 0.0
            else:
                g3 = float(g3)
            if g1 > 1.0:
                g1 = 50
            else:
                g1 = -50
            if g2 > 10.0:
                g2 = 100
            else:
                g2 = -100
            if g3 < 55.0:
                g3 = 50
            else:
                g3 = -50
            if g4 > 5.0:
                g4 = 100
            else:
                g4 = -100
            if g5 > 10.0:
                g5 = 50
            else:
                g5 = -50
            if g6 > 1.5:
                g6 = 100
            else:
                g6 = -100
            if g7 < 20.0:
                g7 = 50
            else:
                g7 = -50

            type = int(type)
            g8 = 0
            if type > 3:
                pe_for_four_season = PE.objects.get(date='2016Q1', stock_id=stock_id).pe_for_four_season
                if pe_for_four_season == '--':
                    pe_for_four_season = 0.0
                else:
                    pe_for_four_season = float(pe_for_four_season)
                evl = float(Cash_Flows_Q.objects.get(date='201601', stock_id=stock_id).free_cash_flows)*0.45 + pe_for_four_season*0.55
                '''if PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps == '--':
                    evl = (float(Transaction_info.objects.get(date='20150701', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150702', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150703', stock_id=stock_id).the_close))/3.0
                else:
                    evl = float(PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps) #本月(季)本益比*下月(季)每股盈餘
                '''
                #a = Share(stock_id+'.TW').get_price()
                a = Transaction_info.objects.filter(date__startswith='201601', stock_id=stock_id).order_by('date')[0].the_close
                if a == '--':
                    a = 0.0
                else:
                    a = float(a)
                model = (evl-a)/evl
                #model = (a-evl)/evl
                if model >= 0.25:
                    g8 = -350
                elif model >= 0.1 and model < 0.25:
                    g8 = -150
                elif model >= -0.1 and model < 0.1:
                    g8 = 0
                elif model >= -0.25 and model < -0.1:
                    g8 = 150
                else:
                    g8 = 350
                macd1 = Technology_Index.objects.get(date='20160104', stock_id=stock_id).day_MACD
                macd2 = Technology_Index.objects.get(date='20160105', stock_id=stock_id).day_MACD
                macd3 = Technology_Index.objects.get(date='20160106', stock_id=stock_id).day_MACD
                if macd1 == '--':
                    macd1 = 0.0
                else:
                    macd1 = float(macd1)
                if macd2 == '--':
                    macd2 = 0.0
                else:
                    macd2 = float(macd2)
                if macd3 == '--':
                    macd3 = 0.0
                else:
                    macd3 = float(macd3)
                if macd2 > macd1 and macd3 > macd2:
                    g8 = g8 + 50
                elif macd3 > macd2:
                    g8 = g8 - 20
                else:
                    g8 = g8 - 50
                k = Technology_Index.objects.get(date='20160104', stock_id=stock_id).day_K
                d = Technology_Index.objects.get(date='20160104', stock_id=stock_id).day_D
                if k == '--':
                    kd = 0.0
                else:
                    k = float(k)
                if d == '--':
                    d = 0.0
                else:
                    d = float(d)
                if k > d:
                    g8 = g8 + 50
                elif k < d:
                    g8 = g8 - 50
            elif type < 3:
                pe_for_four_season = PE.objects.get(date='2016Q1', stock_id=stock_id).pe_for_four_season
                if pe_for_four_season == '--':
                    pe_for_four_season = 0.0
                else:
                    pe_for_four_season = float(pe_for_four_season)
                evl = float(Cash_Flows_Q.objects.get(date='201601', stock_id=stock_id).free_cash_flows)*0.45 + pe_for_four_season*0.55
                '''if PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps == '--':
                    evl = (float(Transaction_info.objects.get(date='20150701', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150702', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150703', stock_id=stock_id).the_close))/3.0
                else:
                    evl = float(PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps) #本月(季)本益比*下月(季)每股盈餘
                '''
                #a = Share(stock_id+'.TW').get_price()
                a = Transaction_info.objects.filter(date__startswith='201601', stock_id=stock_id).order_by('date')[0].the_close
                if a == '--':
                    a = 0.0
                else:
                    a = float(a)
                model = (evl-a)/evl
                #model = (a-evl)/evl
                if model >= 0.25:
                    g8 = -400
                elif model >= 0.1 and model < 0.25:
                    g8 = -200
                elif model >= -0.1 and model < 0.1:
                    g8 = 0
                elif model >= -0.25 and model < -0.1:
                    g8 = 200
                else:
                    g8 = 400
                macd1 = Technology_Index.objects.get(date='20160104', stock_id=stock_id).month_MACD
                macd2 = Technology_Index.objects.get(date='20160105', stock_id=stock_id).month_MACD
                macd3 = Technology_Index.objects.get(date='20160106', stock_id=stock_id).month_MACD
                if macd1 == '--':
                    macd1 = 0.0
                else:
                    macd1 = float(macd1)
                if macd2 == '--':
                    macd2 = 0.0
                else:
                    macd2 = float(macd2)
                if macd3 == '--':
                    macd3 = 0.0
                else:
                    macd3 = float(macd3)
                if macd2 > macd1 and macd3 > macd2:
                    g8 = g8 + 50
                else:
                    g8 = g8 - 50
                k = Technology_Index.objects.get(date='20160104', stock_id=stock_id).month_K
                d = Technology_Index.objects.get(date='20160104', stock_id=stock_id).month_D
                if k == '--':
                    kd = 0.0
                else:
                    k = float(k)
                if d == '--':
                    d = 0.0
                else:
                    d = float(d)
                if k > d:
                    g8 = g8 + 50
                elif k < d:
                    g8 = g8 - 50
            g9 = 0
            pe_for_four_season = PE.objects.get(date='2016Q1', stock_id=stock_id).pe_for_four_season
            if pe_for_four_season == '--':
                pe_for_four_season = 0.0
            else:
                pe_for_four_season = float(pe_for_four_season)
            evl = float(Cash_Flows_Q.objects.get(date='201601', stock_id=stock_id).free_cash_flows)*0.45 + pe_for_four_season*0.55
            '''if PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps == '--':
                    evl = (float(Transaction_info.objects.get(date='20150701', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150702', stock_id=stock_id).the_close)+float(Transaction_info.objects.get(date='20150703', stock_id=stock_id).the_close))/3.0
            else:
                    evl = float(PE.objects.get(date='2015Q3', stock_id=stock_id).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201503', stock_id=stock_id).eps) #本月(季)本益比*下月(季)每股盈餘
            '''
            #a = Share(stock_id+'.TW').get_price()
            #if a is None:
            #    a = 0.0
            a = Transaction_info.objects.filter(date__startswith='201601', stock_id=stock_id).order_by('date')[0].the_close
            if a == '--':
                a = 0.0
            else:
                a = float(a)
            #r = (a-evl)/evl
            r = (evl-a)/evl
            if r >= 0.25:
                g9 = -400
            elif r >= 0.1 and r < 0.25:
                g9 = -200
            elif r >= -0.1 and r < 0.1:
                g9 = 0
            elif r >= -0.25 and r < -0.1:
                g9 = 200
            else:
                g9 = 400

            fitness = g1 + g2 + g3 + g4 + g5 + g6 + g7 + g8 + g9
    g10 = 0
    money = int(mo)*10000 #500(萬)
    invest = int(invest)
    #if invest <= money*1.05 and invest >= money*0.95 and count >= 8 and count <=10:
        #g10 = 78000
    if invest > money*3:
        g10 = -40000
    elif invest >= money*2:
        if count >= 12:
            g10 = -35000
        elif count >= 10 and count < 12:
            g10 = -30000
        elif count < 10 and count > 8:
            g10 = -20000
        else:
            g10 = -30000
    elif invest >= money*1.5 and invest < money*2 : #500(萬)
        if count >= 12:
            g10 = -30000
        elif count >= 10 and count < 12:
            g10 = -25000#35000
        elif count < 10 and count > 8:
            g10 = -20000#40000
        else:
            g10 = -25000#20000
    elif invest >= money*1.2 and invest < money*1.5 : #500(萬)
        if count >= 12:
            g10 = -20000
        elif count >= 10 and count < 12:
            g10 = 25000#35000
        elif count < 10 and count > 8:
            g10 = 30000#40000
        else:
            g10 = 10000#20000
    elif invest >= money and invest < money*1.2 : #500(萬)
        if count >= 12:
            g10 = -10000
        elif count >= 10 and count < 12:
            g10 = 65000#35000
        elif count < 10 and count > 8:
            g10 = 70000#40000
        else:
            g10 = 60000#20000
    elif invest >= money*0.95 and invest < money:
        if count >= 12:
            g10 = -5000
        elif count >= 10 and count < 12:
            g10 = 70000
        elif count < 10 and count > 8:
            g10 = 75000
        else:
            g10 = 60000
    elif invest >= money*0.8 and invest < money*0.95:
        if count >= 12:
            g10 = -6000
        elif count >= 10 and count < 12:
            g10 = 60000
        elif count < 10 and count > 8:
            g10 = 65000
        else:
            g10 = 55000
    else:
        g10 = 0
    fitness = fitness + g10
    '''if fitness < 0:
        fitness = 0
        return fitness,
    else:'''
    return fitness,
toolbox = base.Toolbox()
toolbox.register("evaluate", evalOneMax)
#toolbox.register("evaluate2", evalOneMax2)
#toolbox.register("evaluate3", evalOneMax3)
#toolbox.register("evaluate4", evalOneMax4)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def func(num):
    list1=creator.Individual()
    i=0
    j=1
    while i<5*num:
        if i%5==0:
            list1.append(random.randint(0, 1))
            j=list1[i]
            i=i+1
            continue
        elif i%5!=0 and j==0:
            for j in range(4):
                list1.append(0)
            i=i+4
            continue
        elif i%5!=0 and j!=0:
            for k in range(4):
                list1.append(random.randint(0, 1))
            i=i+4
            continue
    return list1



##################演算法
def main(sc, id, mt, count, mo):
   #random.seed(64)
   # Fitness类提供了weight属性。最小化问题使用负值的的weight,最大化问题用正值。
   creator.create("FitnessMax", base.Fitness, weights=(1.0,))
   creator.create("Individual", list, fitness=creator.FitnessMax)

      #base是个很基本的类啊！！！看来很重要
   #toolbox.register("attr_bool", random.randint, 0, 1)
   #toolbox.register("individual", tools.initRepeat, creator.Individual,
   #toolbox.attr_bool, 5*sc)     #IND_SIZE = 5
   toolbox.register("individual", func,num=sc)
   toolbox.register("population", tools.initRepeat, list, toolbox.individual)

   pop = toolbox.population(n=10)    #定义了500个个体的种群！！！
   CXPB, MUTPB, NGEN = 0.6, 0.005, 25  #0.0001
   #(individual, stock_id, type, count, invest)
   stock_idlist=[]
   for i in range(10):
       stock_idlist.append(id)
   typelist=[]
   for i in range(10):
       typelist.append(mt)
   moneylist=[]
   for i in range(10):
       moneylist.append(mo)
   fitnesses = list(map(toolbox.evaluate, pop, stock_idlist,typelist, moneylist))
   for ind, ide, fit in zip(pop, id, fitnesses):
       ind.fitness.values = fit
       #ind.stock_id = ide

   for g in range(NGEN):
       # Select the next generation individuals
       offspring = toolbox.select(pop, len(pop))
       # Clone the selected individuals
       offspring = list(map(toolbox.clone, offspring))

       # Apply crossover and mutation on the offspring
       for child1, child2 in zip(offspring[::2], offspring[1::2]):

           if random.random() < CXPB:
               toolbox.mate(child1, child2)
               del child1.fitness.values
               del child2.fitness.values
               #del child1.stock_id
               #del child2.stock_id



       for mutant in offspring:
           if random.random() < MUTPB:
               toolbox.mutate(mutant)
               del mutant.fitness.values
               #del mutant.stock_id

       # Evaluate the individuals with an invalid fitness
       invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
       fitnesses = list(map(toolbox.evaluate, pop, stock_idlist,typelist, moneylist))
       for ind, fit in zip(invalid_ind,fitnesses):
           ind.fitness.values = fit
           #ind.stock_id = ide2

       print("  Evaluated %i individuals" % len(invalid_ind))

       # The population is entirely replaced by the offspring
       pop[:] = offspring
       print(pop)
       # Gather all the fitnesses in one list and print the stats
       fits = [ind.fitness.values[0] for ind in pop]
       print(fits)

       length = len(pop)
       mean = sum(fits) / length
       sum2 = sum(x*x for x in fits)
       std = abs(sum2 / length - mean**2)**0.5


       print("  Min %s" % min(fits))
       print("  Max %s" % max(fits))
       print("  Avg %s" % mean)
       print("  Std %s" % std)

   print("-- End of (successful) evolution --")

   best_ind = tools.selBest(pop, 1)
   stock, history, string2, n, stock_invest, sum3 = [], [], '', [], [], 0.0
   for i in best_ind:
       print("individual is %s, %s" % (i, i.fitness.values))
       for j in range(0, len(i), 5):
           if i[j] == 1:
                stock_count=str(i[j+1])+str(i[j+2])+str(i[j+3])+str(i[j+4]) #stock_idlist[int(j/5)]
                stock_count=int(stock_count,2)
                index = j//5
                price = Transaction_info.objects.filter(date__startswith='2015', stock_id=id[index]).order_by('date')[0].the_close  # 2015交易第一天
                price = float(price)*1000 # 股價一張
                stock_invest.append(price*stock_count) #這支股票的投入金額
                stock.append(id[index])  # 有購買的股票
                n.append(stock_count)  # 購買的股票張數
   sum3 = sum(stock_invest)  # 總投入金額

   print(stock)
   print(stock_invest)
   print(n)
   print('sum3='+str(sum3))

   for i in stock: # 計算資金比例
       p = float(stock_invest[stock.index(i)])/sum3 * 100
       p = round(p, ndigits=1)
       p = str(p)
       name = Information.objects.get(stock_id=i).co_name
       string2 = string2 + name + '(' + p + '%) '
       print(string2)

   history.append({'season':'2016Q1', 'invest':string2, 'initial':str(sum3)})
   return history, stock, n, sum3  # 投資組合、id、張數





