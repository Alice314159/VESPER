from StockAnalyze.EnumData import CONSTDEFINE  as CONST
from StockAnalyze.ReadDataFromFile import readDataFromFile as RD
import pandas as pd
from StockAnalyze.Common.Utils import GetNQuartersDate
#计算一段时间内上涨的股票
def CalRisenStockForInterval(logger,file_name=CONST.STOCK_DATA_AFTER_FILE_NAME,
                                     path=CONST.STOCK_DATA_FOLDER_PATH):
    #读取股票数据
    stock_list = RD.ReadHS300StockCode(logger)

    for stock_code in stock_list:
        calRisenStock(logger,stock_code)

#输入股票的计算季度，计算在该前nQuarters个季度内是否上涨
def calRisenStock(logger,stock_code,nQuarters=3,file_name=CONST.STOCK_DATA_AFTER_FILE_NAME,
                                     path=CONST.STOCK_DATA_FOLDER_PATH):
    df_single = RD.readSingleStockData(logger, stock_code, file_name, path)
    data_column = [CONST.STOCK_CODE_ENG, CONST.STOCK_DATE_ENG, CONST.STOCK_OPEN_PRICE_ENG, CONST.STOCK_CLOSE_PRICE_ENG]

    df_single = df_single[data_column]
    if df_single.empty:
        logger.warning('stock code {} has no enough init data'.format(stock_code))
        return

    list_AM = []
    for i in range(nQuarters):
        (strBeginDate,strEndDate) = GetNQuartersDate(i+1)
        print(df_single)
        df_cal = df_single[strBeginDate <= df_single[CONST.STOCK_DATE_ENG] <= strEndDate]
        if df_cal.empty:
            logger.warning('stock code {} has no enough cal data for date:{}-{}'.format(stock_code,strBeginDate,strEndDate))
            list_AM.append(-1)

        print(df_cal.loc[0,])



    return