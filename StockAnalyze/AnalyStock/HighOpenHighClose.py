from StockAnalyze.EnumData import CONSTDEFINE  as CONST
from StockAnalyze.ReadDataFromFile import readDataFromFile as RD


# 计算高开高走的股票
def CalHighOpenHighCloseStock(logger, file_name=CONST.STOCK_DATA_AFTER_FILE_NAME,
                              path=CONST.STOCK_DATA_FOLDER_PATH):
    # 读取股票数据
    stock_list = RD.ReadHS300StockCode(logger)

    for stock_code in stock_list:
        calRisenStock(logger, stock_code)


# 输入股票的编号，计算高开高走的股票信息
def calRisenStock(logger, stock_code, file_name=CONST.STOCK_DATA_AFTER_FILE_NAME,
                  path=CONST.STOCK_DATA_FOLDER_PATH):
    df_single = RD.readSingleStockData(logger, stock_code, file_name, path)
    data_column = [CONST.STOCK_CODE_ENG, CONST.STOCK_DATE_ENG, CONST.STOCK_OPEN_PRICE_ENG, CONST.STOCK_CLOSE_PRICE_ENG,
                   CONST.STOCK_PRE_CLOSE_PRICE_ENG]

    df_data = df_single[data_column]
    if df_data.empty:
        logger.warning('stock code {} has no enough init data'.format(stock_code))
        return

    df_data['HighOpenHighClose'] = (df_data[CONST.STOCK_OPEN_PRICE_ENG]>df_data[CONST.STOCK_PRE_CLOSE_PRICE_ENG]) &(df_data[CONST.STOCK_OPEN_PRICE_ENG]<df_data[CONST.STOCK_CLOSE_PRICE_ENG])
    df_data.to_excel(CONST.STOCK_TEMP_HIGH_OPEN_HIGH_CLOSE_PATH  + stock_code + '.xlsx')
    return
