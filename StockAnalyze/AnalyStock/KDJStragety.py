import pandas as pd

import StockAnalyze.EnumData.CONSTDEFINE as CONST
import StockAnalyze.EnumData.ConfigParam as PARAM
from StockAnalyze.ReadDataFromFile import readDataFromFile as RD
from StockAnalyze.AnalyStock import BuyORSell as BUYORSELL

from StockAnalyze.Common.Utils import GetJLineEarnRateFileName
from StockAnalyze.AnalyStock import ParamCal
from StockAnalyze.GetStockData import GetDataFromWeb as DownLoadData
from StockAnalyze.AnalyStock.BuyORSell import stockData2TradeInfo
from StockAnalyze.Common import ReadConfig

from StockAnalyze.AnalyStock import Expression

Config = ReadConfig.ReadConfig()

# 只根据J线判断是否需要进行买卖,根据
def calJLineStragety(stock_code, df_stock_data):
    df_j_data = ParamCal.calKDJLine(stock_code, df_stock_data)

    # 1.计算基础数据
    df_j_data[CONST.STOCK_20_MEAN_ENG] = df_j_data[CONST.STOCK_CLOSE_PRICE_ENG].rolling(window=20).mean()

    # 计算J线的下降数据,shift向上一条数据移动,定义临时变量，存储数据
    CONST_TEMP_JSlope = 'JSlope'
    df_j_data[CONST_TEMP_JSlope] = df_j_data[CONST.STOCK_J_LINE] - df_j_data[CONST.STOCK_J_LINE].shift(axis=0)

    # 计算10日内的最大收盘价
    df_j_data['Max10'] = df_j_data[CONST.STOCK_CLOSE_PRICE_ENG].rolling(window=10).max()

    # 2.买卖策略--买入
    # 2.1 J线小于10
    df_j_data['Lower10'] = df_j_data[CONST.STOCK_J_LINE] < Config.GetJlineBuyParm(PARAM.J_LINE_SMALLER_THRESHOLD)
    # 2.2当天收盘价比十日内的高点下跌超过8%
    df_j_data['DownAM'] = df_j_data[CONST.STOCK_CLOSE_PRICE_ENG] < Config.GetJlineBuyParm(PARAM.J_LINE_CLOSE_PRICE_DOWN) * df_j_data['Max10']
    # 2.3 J线呈减小趋势，且变化减缓,并在一定范围内
    df_j_data['JDown'] = df_j_data[CONST.STOCK_J_LINE] < df_j_data[CONST.STOCK_J_LINE].shift(axis=0)
    df_j_data['JDownSlower'] = (abs(df_j_data[CONST_TEMP_JSlope]) / abs(df_j_data[CONST_TEMP_JSlope].shift(axis=0)))<= Config.GetJlineBuyParm(PARAM.J_LINE_BUY_SLOPE)
    #2.4,20日斜率大于
    df_j_data['Diff20'] = (df_j_data[CONST.STOCK_20_MEAN_ENG] / df_j_data[CONST.STOCK_20_MEAN_ENG].shift(
        axis=0)) >= Config.GetJlineBuyParm(PARAM.J_LINE_CHANGE)


    sz_thresh = Config.GetJlineBuyParm(PARAM.SZ_J_LINE)
    df_j_data['SZ'] = df_j_data[CONST.STOCK_SZ_J_LINE] < sz_thresh
    # 买入点赋值
    df_j_data[CONST.STOCK_BUY_SECTION] = df_j_data['SZ'] & df_j_data['Lower10'] & df_j_data['DownAM'] & df_j_data['JDown'] & df_j_data['JDownSlower'] & df_j_data['Diff20']

    # 3.买卖策略--卖出策略
    # 3.1J线呈上升趋势，且变化减缓
    df_j_data['higher70'] = df_j_data[CONST.STOCK_J_LINE] > Config.GetJlineSellParm(PARAM.J_LINE_BIGGER_THRESHOLD)
    df_j_data['JUP'] = df_j_data[CONST.STOCK_J_LINE] > df_j_data[CONST.STOCK_J_LINE].shift(axis=0)
    df_j_data['JUPSlower'] = (abs(df_j_data[CONST_TEMP_JSlope]) / abs(df_j_data[CONST_TEMP_JSlope].shift(axis=0)))<= Config.GetJlineSellParm(PARAM.J_LINE_SELL_SLOPE)
    # 3.2 J值超过90，直接卖掉
    df_j_data['Jbigger90'] = df_j_data[CONST.STOCK_J_LINE] > Config.GetJlineSellParm(PARAM.J_LINE_SELL_THRESHOLD_90)
    #3.3 J线变小，且大于50，直接卖出
    df_j_data['Jbigger50AndSmaller'] = (df_j_data[CONST.STOCK_J_LINE] > Config.GetJlineSellParm(PARAM.J_LINE_SELL_THRESHOLD_50)) & (df_j_data[CONST.STOCK_J_LINE] <= df_j_data[CONST.STOCK_J_LINE].shift(1))


    # 卖出点赋值,满足J线变大，并且变缓，同时J大于90则直接卖出
    df_j_data[CONST.STOCK_SELL_SECTION] = (df_j_data['Jbigger90'] &df_j_data['JUP']  & df_j_data['JUPSlower']) | df_j_data['Jbigger50AndSmaller']
    #df_j_data[CONST.STOCK_SELL_SECTION] = df_j_data['Jbigger90']


    # #若满足J线变大，并且变缓，则在收益大于5%的情况下卖出，收益条件在买卖中进行计算。
    df_j_data[CONST.STOCK_SELL_IF_SECTION] = (df_j_data['higher70'] & df_j_data['JUP'] & df_j_data['JUPSlower'])
    #df_j_data[CONST.STOCK_SELL_IF_SECTION] = False

    df_j_data = df_j_data.loc[:, [CONST.STOCK_DATE_ENG,CONST.STOCK_CLOSE_PRICE_ENG,CONST.STOCK_BUY_SECTION,CONST.STOCK_SELL_SECTION,CONST.STOCK_SELL_IF_SECTION, CONST.STOCK_J_LINE]]


    df_j_data.to_excel(CONST.STOCK_TEMP_TRADE_PATH + '\\' + stock_code + '.xlsx')

    #获取买卖数据
    df_trade_data = stockData2TradeInfo(stock_code, df_j_data,Config)

    return df_trade_data





#获取单个股票的基础数据，并计算JDK数据
def getSingleCodeDataWithKDJ(logger,stock_code):
    df_orignal = RD.readSingleStockData(logger, stock_code, CONST.STOCK_DATA_PRE_FILE_NAME,
                                        CONST.STOCK_DATA_FOLDER_PATH)

    if df_orignal.empty :
        logger.warning("stock-{} data is wrong ,please check".format(stock_code))

    elif df_orignal.count() < 5:
        logger.warning("stock-{} data is not enough ,please wait".format(stock_code))
    else:
        df_orignal = ParamCal.calKDJLine(stock_code, df_orignal)

    return df_orignal

#根据计算的结果筛选满足买卖条件的股票，统计收益
def staticStockTrade(logger,stock_num,df_earn_money):
    df_earn_money = df_earn_money[(df_earn_money['money'] != 10000) & (df_earn_money['money'] > 0)]
    count = len(df_earn_money)
    file_name = GetJLineEarnRateFileName()
    if count > 0:
        earn_money = round(df_earn_money['money'].sum() / count, 2)

        df_earn_money.loc[df_earn_money.index.max() + 1] = earn_money
        df_earn_money.loc[df_earn_money.index.max(), 'stock'] = 'statics'

        file_name = GetJLineEarnRateFileName(earn_money)
        df_earn_money.to_excel(file_name)
        logger.info('total stock num : {} ,sell num:{},ave_earn_money ={},param:{}'.format(stock_num, count, earn_money,file_name))
    else:
        logger.warning('param:{},total stock num : {} ,sell num:{}'.format(file_name,stock_num, count))



#K调用主函数
def KDJStragetyStockEarnMoney(logger,stock_list):

    # 获取上证综合指数数据
    df_SZ_data = ParamCal.calCompositeIndexKDJ(logger)
    list_stock_money =[]
    for stock_code in stock_list:
        #数据不存在的情况下，需要下载数据
        #DownLoadData.getDayKline(logger,[stock_code], [CONST.STOCK_DATA_PreStandardized])

        df_orignal_data = getSingleCodeDataWithKDJ(logger,stock_code)

        if df_orignal_data.empty:
            logger.warning("stock-{} data is wrong ,please check".format(stock_code))

        else:
            df_union = ParamCal.paramUnion(df_orignal_data, df_SZ_data)

            df_trade_info = calJLineStragety(stock_code, df_union)

            if df_trade_info.__sizeof__() >= 1:
                money = BUYORSELL.VerifyStrategyForDataFrame(stock_code, df_trade_info)
                list_stock_money.append([stock_code, money])
            else:
                logger.info('stock code {} trade data is not enough {}'.format(stock_code, df_trade_info))

    df_earn_money2 = pd.DataFrame(list_stock_money, columns=['stock', 'money'])

    staticStockTrade(logger,len(stock_list),df_earn_money2)


def KDJStragetyBasedFilter(logger,stock_code):
    #获取原始数据
    df_orign = RD.readSingleStockData(logger ,stock_code)

    #计算KDJ数据
    df_orign_KDJ = ParamCal.calKDJLine(stock_code,df_orign)

    #JT<10
    df_JT1 = Expression.GetJlineBiggerThreshold(logger,stock_code,df_orign_KDJ)

    #JT<JT-1
    df_JT2 = Expression.GetJlineVariationTrend(logger, stock_code, df_orign_KDJ)

    #(JT - JT-1)/(JT-1 - JT-2) <= 0.8

    return
