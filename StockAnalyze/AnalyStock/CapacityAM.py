from StockAnalyze.EnumData import CONSTDEFINE  as CONST
from StockAnalyze.ReadDataFromFile import readDataFromFile as RD
import StockAnalyze.EnumData.ConfigParam as PARAM
from StockAnalyze.Common import ReadConfig
from StockAnalyze.Common import Utils
Config = ReadConfig.ReadConfig()

from loguru import logger
logger.add("../Log/CApacityAM.log", rotation="1 MB")

# 计算股票
def CalCapacityStock(file_name=CONST.STOCK_DATA_AFTER_FILE_NAME,
                              path=CONST.STOCK_DATA_FOLDER_PATH):
    Utils.DeleteFolders(CONST.STOCK_TEMP_CAPACITY_PATH)
    Utils.mkdir(CONST.STOCK_TEMP_CAPACITY_PATH)
    # 读取股票数据
    stock_list = RD.ReadAllStockCode(logger)

    for stock_code in stock_list:
        calCapacityRisenStock(stock_code)


# 输入股票的编号，计算fangliang股票信息
def calCapacityRisenStock( stock_code, file_name=CONST.STOCK_DATA_AFTER_FILE_NAME,
                  path=CONST.STOCK_DATA_FOLDER_PATH):

    try:
        df_single = RD.readSingleStockData(logger, stock_code, file_name, path)
        data_column = [CONST.STOCK_CODE_ENG, CONST.STOCK_DATE_ENG, CONST.STOCK_DEAL_COUNT_ENG]

        df_data = df_single[data_column]
        if df_data.empty:
            logger.warning('stock code {} has no enough init data'.format(stock_code))
            return

        df_data['Capacity'] = df_data[CONST.STOCK_DEAL_COUNT_ENG] / df_data[
            CONST.STOCK_DEAL_COUNT_ENG].shift() >= Config.GetCapacityParm(PARAM.CapacityAM_RATIO_THRESHOLD)

        data_list = df_data.tail(1).values.tolist()
        if data_list[0][-1]:
            df_data.to_excel(CONST.STOCK_TEMP_CAPACITY_PATH + stock_code + '.xlsx')
            logger.warning('stock Capacity Am info:{}'.format(data_list[0]))
    except Exception as err:
        logger.warning(err.args)


    return


if __name__ == '__main__':
    from loguru import logger
    logger.add("../Log/CApacityAM.log", rotation="1 MB")
    CalCapacityStock(logger)