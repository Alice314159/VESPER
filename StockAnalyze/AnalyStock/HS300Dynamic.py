# 沪深300成分股动量策略
import StockAnalyze.EnumData.CONSTDEFINE as CONST
import numpy as np
import pandas as pd
from StockAnalyze.ReadDataFromFile import readDataFromFile as RD
from StockAnalyze.Common import ReadConfig
from StockAnalyze.Common import Utils

Config = ReadConfig.ReadConfig()

PRICE_RAISE_60 = 'priceRaise60'
SELL_PRICE = 'sellPrice'
SELL_DATE = 'sellDate'


# 从沪深300成分股里，选取近60日涨幅最大的5只股票.
def HS300Dynamic(logger, buydate='', selectedDays=60, stock_nums=5, period=20):
    # 获取沪深300成分股的所有股票
    stock_list = RD.ReadHS300StockCode(logger)
    # 获取沪深300的开收盘及并计算60日涨幅数据
    df_data = getStockListDataWithDynamicParam(logger, stock_list)

    print(df_data)
    # 获取涨幅最高的股票
    if buydate == '':
        buydate = df_data[CONST.STOCK_DATE_ENG].max()
    df_data_high = df_data[df_data[CONST.STOCK_DATE_ENG] == buydate]
    max_5 = df_data_high.nlargest(stock_nums, [PRICE_RAISE_60])
    print(max_5)



# 计算60日内的涨幅最大,计算多天的数据
def _getHS300ParamCalForManyDays(logger, stock_code, df_data, selectedDays=60):

    df_data[PRICE_RAISE_60]= (df_data[CONST.STOCK_CLOSE_PRICE_ENG] - df_data[CONST.STOCK_OPEN_PRICE_ENG].shift(selectedDays)) / df_data[CONST.STOCK_CLOSE_PRICE_ENG]
    df_data[PRICE_RAISE_60]= df_data[PRICE_RAISE_60].apply(lambda x:round(x,2))
    df_data = df_data[df_data[PRICE_RAISE_60].notnull()]
    return df_data

# 计算60日内的涨幅最大
def _getHS300ParamCal(logger, stock_code, df_data, dateAgo='', selectedDays=60):
    if dateAgo == '':
        dateAgo = Utils.GetNdaysBefore()

    df_data = df_data[df_data[CONST.STOCK_DATE_ENG] >= dateAgo]
    df_data.loc[:,[PRICE_RAISE_60]] = (df_data[CONST.STOCK_CLOSE_PRICE_ENG] - df_data[CONST.STOCK_OPEN_PRICE_ENG].shift(selectedDays)) / df_data[CONST.STOCK_CLOSE_PRICE_ENG]
    df_data.loc[:,[PRICE_RAISE_60]] = df_data[PRICE_RAISE_60].apply(lambda x:round(x,2))
    df_data = df_data[df_data[PRICE_RAISE_60].notnull]
    return df_data


# 输入股票list,获取最新日期的涨幅最大的5支股票
def getStockListDataWithDynamicParam(logger, stock_code_list, file_name=CONST.STOCK_DATA_AFTER_FILE_NAME,
                                     path=CONST.STOCK_DATA_FOLDER_PATH):
    data_column = [CONST.STOCK_CODE_ENG, CONST.STOCK_DATE_ENG, CONST.STOCK_OPEN_PRICE_ENG, CONST.STOCK_CLOSE_PRICE_ENG,
                   PRICE_RAISE_60]
    df_stocks = pd.DataFrame(columns=data_column)
    for stock_code in stock_code_list:
        df_single = RD.readSingleStockData(logger, stock_code, file_name, path)
        if df_single.empty:
            continue
        df_data = _getHS300ParamCal(logger, stock_code, df_single)
        df_res = df_data.loc[:, data_column]
        # append之后需要将数值返回，df_stocks.append()结果不赋值导致df_stock为空。
        df_stocks = df_stocks.append(df_res.tail(1), ignore_index=False)

    return df_stocks


# 输入股票list,获取对应的所有日期的数据
def getStockListDataWithDynamicParamForManyDays(logger, stock_code_list,largestNum = 5, buyPeriod=20,file_name=CONST.STOCK_DATA_AFTER_FILE_NAME,
                                     path=CONST.STOCK_DATA_FOLDER_PATH):
    data_column = [CONST.STOCK_CODE_ENG, CONST.STOCK_DATE_ENG, CONST.STOCK_OPEN_PRICE_ENG, CONST.STOCK_CLOSE_PRICE_ENG,
                   PRICE_RAISE_60,SELL_DATE,SELL_PRICE]
    df_stocks = pd.DataFrame(columns=data_column)
    for stock_code in stock_code_list:
        df_single = RD.readSingleStockData(logger, stock_code, file_name, path)
        if df_single.empty:
            continue
        df_data_temp = _getHS300ParamCalForManyDays(logger, stock_code, df_single)

        df_data = df_data_temp.copy()
        df_data.loc[:,SELL_DATE] = df_single[CONST.STOCK_DATE_ENG].shift(-(buyPeriod-1))
        df_data.loc[:,SELL_PRICE] = df_single[CONST.STOCK_CLOSE_PRICE_ENG].shift(-(buyPeriod-1))

        df_res = df_data.loc[:, data_column]
        # append之后需要将数值返回，df_stocks.append()结果不赋值导致df_stock为空。
        df_stocks = df_stocks.append(df_res, ignore_index=False)

    df_data = df_stocks.groupby(df_stocks[CONST.STOCK_DATE_ENG])

    df_max_for_day = pd.DataFrame(columns=df_stocks.columns)
    for key, value in df_data:
        df_temp = value.nlargest(largestNum, [PRICE_RAISE_60])
        df_max_for_day = df_max_for_day.append(df_temp,ignore_index=False)

    return df_max_for_day
