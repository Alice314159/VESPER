import pandas as pd
from StockAnalyze.GetStockCode import getStockCodeInfo
from StockAnalyze.ReadDataFromFile import readDataFromFile as RD
import StockAnalyze.EnumData.CONSTDEFINE as CONST
#判断当前收盘价走势满足W形状？
def _wFigureJudge(logger,stock_code,df_data):
    isW  = False


    df_temp = df_data[-20:-1]
    print(df_temp)


    return isW

def JudgeStockWFigure(logger):
    #stock_list = getStockCodeInfo.getAllStockCodeFromFile(logger)
    stock_list = ['SZ.000151']
    for stock_code in stock_list:
        df_orignal = RD.readSingleStockData(logger, stock_code, CONST.STOCK_DATA_PRE_FILE_NAME,
                                        CONST.STOCK_FOLDER_PATH)
        _wFigureJudge(logger,stock_code,df_orignal)
