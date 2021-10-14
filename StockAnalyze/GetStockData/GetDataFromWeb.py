import baostock as bs
import pandas as pd
import datetime
import efinance as ef
from StockAnalyze.EnumData import CONSTDEFINE as CONST
from StockAnalyze.EnumData import EnumInfo as EnumData
from StockAnalyze.Common.Utils import getFileNameByAdjust
from StockAnalyze.Common.Utils import mkdir
from StockAnalyze.GetStockCode import getStockCodeInfo
from StockAnalyze.ReadDataFromFile import readDataFromFile as RD


# 输入股票的编号，获取数据的开始结束日期，获取的数据类型
def getDayKline(logger, stock_code_list, adjustflagList=[], frequencyData='d'):
    if len(adjustflagList) <= 0:
        adjustflagList = [CONST.STOCK_DATA_PreStandardized]

    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    if lg.error_code != '0':
        logger.error('login respond  error_msg:' + lg.error_msg)
        return

    for stock_code in stock_code_list:
        for adjustFlag in adjustflagList:
            getAndSaveSingleStockCodeData(logger, stock_code, adjustFlag, frequencyData)

    #### 登出系统 ####
    bs.logout()


# 输入单个股票编号，获取最新的数据
def getAndSaveSingleStockCodeData(logger, stock_code, adjustflagData, frequencyData='d'):
    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    folder_path = CONST.STOCK_DATA_FOLDER_PATH + "\\" + stock_code
    mkdir(folder_path)

    file_name = folder_path + "\\" + getFileNameByAdjust(adjustflagData)

    end_time = (datetime.date.today()).strftime("%Y-%m-%d")

    str_get_data_name = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"
    rs = bs.query_history_k_data_plus(stock_code, str_get_data_name,
                                      start_date='', end_date=end_time,
                                      frequency=frequencyData, adjustflag=adjustflagData)
    logger.info('query_history_k_data_plus code:{} respond error_code:{}'.format(stock_code, rs.error_code))
    if rs.error_code != '0':
        logger.warn('query_history_k_data_plus code:{} respond  error_msg:{}'.format(stock_code, rs.error_msg))

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        temp_data = rs.get_row_data()
        data_list.append(temp_data)
    result = pd.DataFrame(data_list, columns=rs.fields)

    final = result.drop_duplicates(subset=[CONST.STOCK_DATE_ENG], keep='last')
    final.to_excel(file_name, index=False)
    logger.info("write file:{} finished".format(file_name))


# 获取最新一个交易日的分钟级别股票行情数据,数据间隔时间为 1 分钟
def getRealTimeData(logger, freq=1, folder_path=CONST.STOCK_REAL_FOLDER_PATH):
    getStockCodeInfo.getAllStockCodeFromWeb(logger)
    stock_code_list = getStockCodeInfo.getAllStockCodeWithoutExFromFile(logger)
    mkdir(folder_path)
    for stock_code in stock_code_list:
        file_name = folder_path + '\\' + stock_code + '.xlsx'
        # 获取最新一个交易日的分钟级别股票行情数据
        df = ef.stock.get_quote_history(stock_code, klt=freq)
        # 将数据存储到 csv 文件中
        df.to_excel(file_name)
        logger.info('get real time data and save {} success'.format(file_name))


# 每个工作日执行一次，获取最新的数据并写入文件
def TimeToGetDataRunForEveryDay(logger, stock_type=EnumData.StockCodeType.StockTypeAll, endnum=""):
    # 1.获取所有的股票基础信息，并存储至文件
    stock_code_list = []
    if stock_type.value == EnumData.StockCodeType.StockTypeAll.value:
        getStockCodeInfo.getAllStockCodeFromWeb(logger)
        # 2.读取股票信息，获取所有股票编码，并整理成适合计算的格式
        stock_code_list = getStockCodeInfo.getAllStockCodeFromFile(logger)


    elif stock_type.value == EnumData.StockCodeType.StockHS300.value:
        stock_code_list = RD.ReadHS300StockCode(logger)

    else:
        logger.warning('unknown input code type: {}'.format(stock_type))

    logger.info("begin to get stock info fro web{}".format(stock_code_list))
    if endnum != "":
        if endnum.startswith("SZ"):
            stock_code_list = [strdata for strdata in stock_code_list if strdata.startswith(str(endnum))]
        elif endnum.startswith("SH"):
            stock_code_list = [strdata for strdata in stock_code_list if strdata.startswith(str(endnum))]
        elif endnum.startswith("BJ"):
            stock_code_list = [strdata for strdata in stock_code_list if strdata.startswith(str(endnum))]
        else:
            stock_code_list = [strdata for strdata in stock_code_list if strdata.endswith(str(endnum))]

    # 2.拉取数据
    adjustFlag = [CONST.STOCK_DATA_PreStandardized, CONST.STOCK_DATA_Original, CONST.STOCK_DATA_AfterStandardized]
    getDayKline(logger, stock_code_list, adjustFlag)


def TimeToGetDataRunForEveryMin(logger):
    getRealTimeData(logger)

    return


if __name__ == '__main__':
    stock_code_list = ['SZ.300059']
