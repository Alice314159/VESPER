import EnumData.CONSTDEFINE as CONST
from ReadDataFromFile import readDataFromFile as RD
from AnalyStock import cal60Data as Cal60
from AnalyStock import calKDJ as CalKDJ
from AnalyStock import BuyORSell as BUYORSELL
from GetStockCode import getStockCodeInfo
from GetStockData import GetDataFromWeb as DownLoadData
from Common import Logger
import pandas as pd
from Common.Utils import GenerateRandomNum
from Common.Utils import GetJLineEarnRateFileName
from Common import Utils
from AnalyStock import Expression

logger = Logger.log()


# 3.读取股票列表信息，进行分析验证
def analyzeStock():
    stock_code_list = getStockCodeInfo.getAllStockCodeFromFile(logger)
    logger.info("begin to get stock info fro web{}".format(stock_code_list))

    for stock_code in stock_code_list:
        df_orignal = RD.readSingleStockData(logger, stock_code, CONST.STOCK_DATA_AFTER_FILE_NAME,
                                            CONST.STOCK_FOLDER_PATH)
        dict_trade_info = Cal60.getClosingPriceLowerMa60(stock_code, df_orignal)
        if len(dict_trade_info) > 0:
            money = BUYORSELL.VerifyStrategy(stock_code, dict_trade_info)
            print(stock_code, money)


def runForSingleCode():
    # # 1.获取所有的股票基础信息，并存储至文件
    getStockCodeInfo.getAllStockCodeFromWeb()

    # 2.读取股票信息，获取所有股票编码，并整理成适合计算的格式
    stock_code_list = getStockCodeInfo.getAllStockCodeFromFile(logger)
    logger.info("begin to get stock info fro web{}".format(stock_code_list))

    # 2.拉取数据
    for stock_code in stock_code_list:
        temp_list = [stock_code]
        # DownLoadData.getDayKline(temp_list, CONST.STOCK_DATA_PreStandardized)
        # DownLoadData.getDayKline(temp_list, CONST.STOCK_DATA_Original)
        DownLoadData.getDayKline(temp_list, CONST.STOCK_DATA_AfterStandardized)

        df_orignal = RD.readSingleStockData(logger, stock_code, CONST.STOCK_DATA_AFTER_FILE_NAME,
                                            CONST.STOCK_FOLDER_PATH)
        dict_trade_info = Cal60.getClosingPriceLowerMa60(stock_code, df_orignal)
        if len(dict_trade_info) > 0:
            money = BUYORSELL.VerifyStrategy(stock_code, dict_trade_info)
            print(stock_code, money)


def calKDJ():
    # 2.读取股票信息，获取所有股票编码，并整理成适合计算的格式
    stock_code_list = getStockCodeInfo.getAllStockCodeFromFile(logger)
    # logger.info("begin to get stock info fro web{}".format(stock_code_list))

    # 2.拉取数据
    for stock_code in stock_code_list:
        temp_list = [stock_code]
        DownLoadData.getDayKline(temp_list, CONST.STOCK_DATA_PreStandardized)
        DownLoadData.getDayKline(temp_list, CONST.STOCK_DATA_Original)
        DownLoadData.getDayKline(temp_list, CONST.STOCK_DATA_AfterStandardized)

        df_orignal = RD.readSingleStockData(logger, stock_code, CONST.STOCK_DATA_AFTER_FILE_NAME,
                                            CONST.STOCK_FOLDER_PATH)

        if df_orignal.empty:
            logger.warn("stock-{} data is wrong ,please check".format(stock_code))

        else:
            dict_trade_info = CalKDJ.CalDataByKDJ(stock_code, df_orignal)
            if len(dict_trade_info) > 0:
                money = BUYORSELL.VerifyStrategyForDataFrame(stock_code, dict_trade_info)


def calKDJTest():
    stock_code_list = getStockCodeInfo.getAllStockCodeFromFile(logger)

    for stock_code in stock_code_list:
        DownLoadData.getDayKline([stock_code], CONST.STOCK_DATA_PreStandardized)
        df_orignal = RD.readSingleStockData(logger, stock_code, CONST.STOCK_DATA_PRE_FILE_NAME,
                                            CONST.STOCK_FOLDER_PATH)

        if df_orignal.empty:
            logger.warn("stock-{} data is wrong ,please check".format(stock_code))
        else:
            # static = Statics.staticSingleStockForVolume(stock_code, df_orignal)
            df_orignal = df_orignal[df_orignal[CONST.STOCK_DATE_ENG] >= '2021-01-01']
            df_trade_info = CalKDJ.calJLine(stock_code, df_orignal)
            if df_trade_info.__sizeof__() >= 1:
                money = BUYORSELL.VerifyStrategyForDataFrame(stock_code, df_trade_info)
            else:
                logger.info('stock code {} trade data is not enough {}'.format(stock_code, df_trade_info))


def testRandmonStockEarnMoney():
    stock_num = 300
    list_stock_pos = GenerateRandomNum(stock_num)
    stock_code_list = getStockCodeInfo.getAllStockCodeFromFile(logger)
    list_stock_money = []
    for i in list_stock_pos:
        stock_code = stock_code_list[i]
        # DownLoadData.getDayKline([stock_code], CONST.STOCK_DATA_PreStandardized)
        df_orignal = RD.readSingleStockData(logger, stock_code, CONST.STOCK_DATA_PRE_FILE_NAME,
                                            CONST.STOCK_FOLDER_PATH)

        if df_orignal.empty:
            logger.warn("stock-{} data is wrong ,please check".format(stock_code))

        else:
            df_orignal = df_orignal[df_orignal[CONST.STOCK_DATE_ENG] >= '2021-01-01']
            df_trade_info = CalKDJ.calJLine(stock_code, df_orignal)
            if df_trade_info.__sizeof__() >= 1:
                money = BUYORSELL.VerifyStrategyForDataFrame(stock_code, df_trade_info)
                list_stock_money.append([stock_code, money])
            else:
                logger.info('stock code {} trade data is not enough {}'.format(stock_code, df_trade_info))

    df_earn_money = pd.DataFrame(list_stock_money, columns=['stock', 'money'])

    earn_money = round(df_earn_money['money'].sum() / stock_num, 2)

    df_earn_money.loc[df_earn_money.index.max() + 1] = earn_money
    df_earn_money.loc[df_earn_money.index.max(), 'stock'] = 'statics'

    file_name = GetJLineEarnRateFileName()
    df_earn_money.to_excel(file_name)
    logger.info('total stock num : {} ,ave_earn_money ={}'.format(stock_num, earn_money))


def testCertainStockEarnMoney():
    stock_code_list1 = getStockCodeInfo.getAllStockCodeFromFile(logger)
    stock_code_list = stock_code_list1[0:50]
    #stock_code_list = ['SZ.300015']
    list_stock_money = []
    stock_num = len(stock_code_list)

    begin_date = '2021-01-01'

    # 获取上证综合指数数据
    df_SZ_data = RD.getCompositeIndexFileData(logger, CONST.SZ_INDEX_CODE, CONST.STOCK_DATA_ORIGNAL_FILE_NAME,
                                              CONST.STOCK_FOLDER_PATH)

    df_SZ_data = Utils.CalKDJLine(CONST.SZ_INDEX_CODE, df_SZ_data)
    df_SZ_KDJ_data = df_SZ_data[df_SZ_data[CONST.STOCK_DATE_ENG] >= begin_date]
    list_buy_date = Expression.GetCompositeIndexDateList(logger,df_SZ_KDJ_data,15,CONST.STOCK_J_LINE,CONST.ExPression_Smaller)

    for stock_code in stock_code_list:

        df_orignal = RD.readSingleStockData(logger, stock_code, CONST.STOCK_DATA_PRE_FILE_NAME,
                                            CONST.STOCK_FOLDER_PATH)

        if df_orignal.empty:
            logger.warning("stock-{} data is wrong ,please check".format(stock_code))

        else:
            date_stock_begin_temp = df_orignal[CONST.STOCK_DATE_ENG].min()
            begin_date = max(date_stock_begin_temp, begin_date)

            df_orignal = df_orignal[df_orignal[CONST.STOCK_DATE_ENG] >= begin_date]
            df_trade_info = CalKDJ.calJLineStragety(stock_code, df_orignal)

            if df_trade_info.__sizeof__() >= 1:
                money = BUYORSELL.VerifyStrategyForDataFrame(stock_code, df_trade_info,list_buy_date)
                list_stock_money.append([stock_code, money])
            else:
                logger.info('stock code {} trade data is not enough {}'.format(stock_code, df_trade_info))

    df_earn_money2 = pd.DataFrame(list_stock_money, columns=['stock', 'money'])

    df_earn_money = df_earn_money2[(df_earn_money2['money'] != 10000) & (df_earn_money2['money'] > 0)]
    count = len(df_earn_money)
    if count >0:
        earn_money = round(df_earn_money['money'].sum() / count, 2)

        df_earn_money.loc[df_earn_money.index.max() + 1] = earn_money
        df_earn_money.loc[df_earn_money.index.max(), 'stock'] = 'statics'

        file_name = GetJLineEarnRateFileName()
        df_earn_money.to_excel('../param/' + file_name)
        logger.info('total stock num : {} ,sell num:{},ave_earn_money ={}'.format(stock_num, count, earn_money))
    else:
        logger.warning('total stock num : {} ,sell num:{}'.format(stock_num, count))

if __name__ == '__main__':
    # runForSingleCode()
    # calKDJTest()
    testCertainStockEarnMoney()
    #GetStockData.GetDataFromWeb.TimeToGetDataRunForEveryMin(logger)
