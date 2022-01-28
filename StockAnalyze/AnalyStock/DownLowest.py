#获取最近一段时间跌幅最小的股票数据

from StockAnalyze.EnumData import CONSTDEFINE  as CONST
from StockAnalyze.ReadDataFromFile import readDataFromFile as RD
import pandas as pd
from StockAnalyze.Common import ReadConfig
from StockAnalyze.Common import Utils
Config = ReadConfig.ReadConfig()

import time
t = time.strftime("%Y_%m_%d")
from loguru import logger
logger.add(sink="../Log/Down-{}.log".format(t),level= "INFO", rotation="1 MB",retention="10 days")


# 计算股票
def CalRecentDownLowestStock(caldate = '20220101',file_name=CONST.STOCK_DATA_AFTER_FILE_NAME,
                              path=CONST.STOCK_DATA_FOLDER_PATH):

    # 读取股票数据
    stock_list = RD.ReadAllStockCode(logger)

    downList = []
    for stock_code in stock_list:
        res = calDownAmStock(stock_code)
        if res != None:
            downList.append(res)
    data = pd.DataFrame(downList,columns=[CONST.STOCK_CODE_ENG, CONST.STOCK_DATE_ENG,CONST.STOCK_DATE_ENG, CONST.STOCK_OPEN_PRICE_ENG,CONST.STOCK_CLOSE_PRICE_ENG,'DownAM'])
    data.to_excel('downAM.xlsx')



# 输入股票的编号，计算跌幅股票信息
def calDownAmStock( stock_code,caldate = '2022-01-01', file_name=CONST.STOCK_DATA_AFTER_FILE_NAME,
                  path=CONST.STOCK_DATA_FOLDER_PATH):

    try:
        df_single = RD.readSingleStockData(logger, stock_code, file_name, path)
        data_column = [CONST.STOCK_CODE_ENG, CONST.STOCK_DATE_ENG, CONST.STOCK_OPEN_PRICE_ENG,CONST.STOCK_CLOSE_PRICE_ENG]

        df_single = df_single[df_single[CONST.STOCK_DATE_ENG] >= caldate]

        df_data = df_single[data_column]

        head_data = df_data.head(1).values.tolist()[0]
        tail_data = df_data.tail(1).values.tolist()[0]

        downAm = 100*(tail_data[3] - head_data[2])/head_data[2]

        beginDate = head_data[1]
        endDate = tail_data[1]
        if downAm >0:
            logger.info('stockcode:{} during time {} -{},open price-{},close-price-{},rise-{}'.format(stock_code,beginDate,endDate,head_data[2],tail_data[3],downAm))
        else:
            logger.info('stockcode:{} during time {} -{},open price-{},close-price-{},down-{}'.format(stock_code,beginDate,endDate,head_data[2],tail_data[3],downAm))

    except Exception as err:
        logger.warning('stockcode :{},error msg:{}'.format(stock_code,err.args))
        return None

    #(stock_code,beginDate,endData,beginOpenPrice,endClosePrice,DownAm)
    return (stock_code,beginDate,head_data[2],endDate,tail_data[3],downAm)


