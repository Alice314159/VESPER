# 计算股票的周线
import pandas as pd

from StockAnalyze.ReadDataFromFile import readDataFromFile as RD
import StockAnalyze.EnumData.CONSTDEFINE as CONST
from StockAnalyze.Common.Utils import Date2DateDays
import StockAnalyze.Common.Drawing as Draw


# 计算周线函数
def StockWeekData(logger):
    # 获取股票列表
    stock_list = RD.ReadHS300StockCode(logger)
    # 按照股票列表分别读取数据
    _calWeekData(logger, stock_list)
    #
    return


# 输入股票的list,计算股票的周函数
def _calWeekData(logger, stock_code_list):
    for stock_code in stock_code_list:
        df_single = RD.readSingleStockData(logger, stock_code, CONST.STOCK_DATA_AFTER_FILE_NAME,
                                           CONST.STOCK_DATA_FOLDER_PATH)

    return


# 输入股票的代码，计算股票的周线函数
def _calWeekDataForSingleStock(logger, stock_code):
    df_single = RD.readSingleStockData(logger, stock_code, CONST.STOCK_DATA_AFTER_FILE_NAME,
                                       CONST.STOCK_DATA_FOLDER_PATH)

    # 筛选数据中的日期，开盘价，收盘价，最高价，最低价
    df_data = df_single[
        [CONST.STOCK_DATE_ENG, CONST.STOCK_OPEN_PRICE_ENG, CONST.STOCK_CLOSE_PRICE_ENG, CONST.STOCK_HIGHEST_ENG,
         CONST.STOCK_LOWEST_ENG]]

    # 将dataFrame转换为list
    date_list = df_data[CONST.STOCK_DATE_ENG].values
    print(date_list)

    # 股票的开市时间进行分组
    split_list = []
    nlength = len(date_list)
    begin_split = 0
    for i in range(nlength):

        if i == 0:
            begin_split = 0
            if (Date2DateDays(date_list[1], date_list[0]) > 1):
                split_list.append((0, 0))

        elif i == nlength - 1:
            if (Date2DateDays(date_list[i], date_list[i - 1]) > 1):
                split_list.append((i, i))
            else:
                split_list.append((begin_split, i))
        else:
            before_day = date_list[i - 1]
            current_day = date_list[i]
            after_day = date_list[i + 1]

            diff_before = Date2DateDays(current_day, before_day)
            diff_after = Date2DateDays(after_day, current_day)

            if diff_before > 1:
                begin_split = i

            if diff_after > 1:
                split_list.append((begin_split, i))

    # 定义周数据（日期，开盘价，收盘价，最高价，最低价）
    week_info = []
    open_price_list = df_data[CONST.STOCK_OPEN_PRICE_ENG].values
    close_price_list = df_data[CONST.STOCK_CLOSE_PRICE_ENG].values
    highest_list = df_data[CONST.STOCK_HIGHEST_ENG].values
    lowest_list = df_data[CONST.STOCK_LOWEST_ENG].values
    for split in split_list:
        begin_split = split[0]
        end_split = split[1]

        str_date = date_list[end_split]
        open_price = open_price_list[begin_split]
        close_price = close_price_list[end_split]

        highest_price = max(highest_list[begin_split:end_split + 1])
        lowest_price = min(lowest_list[begin_split:end_split + 1])

        week_info.append((str_date, open_price, close_price, highest_price, lowest_price))

    df_week = pd.DataFrame(week_info,
                           columns=[CONST.STOCK_DATE_ENG, CONST.STOCK_OPEN_PRICE_ENG, CONST.STOCK_CLOSE_PRICE_ENG,
                                    CONST.STOCK_HIGHEST_ENG,
                                    CONST.STOCK_LOWEST_ENG])

    logger.info('stock:{} week k-line data is :{}'.format(stock_code,df_week))

    return df_week
