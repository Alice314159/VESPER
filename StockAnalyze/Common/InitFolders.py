from StockAnalyze.Common.Utils import mkdir
from StockAnalyze.EnumData import CONSTDEFINE as CONST

#初始化首先构建文件夹，程序运行目录
def InitFolders():
    mkdir(CONST.STOCK_DATA_FOLDER_PATH)
    mkdir(CONST.STOCK_CODE_FOLDER_PATH)
    mkdir(CONST.STOCK_REAL_FOLDER_PATH)
    mkdir(CONST.STOCK_TEMP_FOLDER_PATH)

    mkdir(CONST.STOCK_TEMP_TRADE_PATH)
    mkdir(CONST.STOCK_TEMP_DRAW_PATH)
    mkdir(CONST.STOCK_TEMP_HIGH_OPEN_HIGH_CLOSE_PATH)

    return
