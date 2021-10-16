# 计算股票的调整周期
from StockAnalyze.ReadDataFromFile import readDataFromFile as RD
import StockAnalyze.EnumData.CONSTDEFINE as CONST


def StockAdjustCycle(logger):
    # 获取股票列表
    stock_list = RD.ReadHS300StockCode(logger)
    # 按照股票列表分别读取数据
    _getStockAdjustCycle(logger, stock_list)
    #
    return


#
def _getStockAdjustCycle(logger, stock_code_list):
    for stock_code in stock_code_list:
        df_single = RD.readSingleStockData(logger, stock_code, CONST.STOCK_DATA_AFTER_FILE_NAME,
                                           CONST.STOCK_DATA_FOLDER_PATH)

        data_column = [CONST.STOCK_CODE_ENG, CONST.STOCK_DATE_ENG, CONST.STOCK_CLOSE_PRICE_ENG]

        df_single = df_single[data_column]
        if df_single.empty:
            continue
        df_data_temp = _getSingleStockAdjustCycle(logger, stock_code, df_single)

    return


# 计算每一只股票的调整周期
def _getSingleStockAdjustCycle(logger, stock_code, df_data):
    # 计算N日内的最大值和最小值，并保存日期
    nDays = 20
    strDaysMax = 'DaysMax'
    strDaysMin = 'DaysMin'
    strDaysMaxDate = 'DaysMaxDate'
    strDaysMinDate = 'DaysMinDate'

    df_data[strDaysMax] = df_data[CONST.STOCK_CLOSE_PRICE_ENG].rolling(window=nDays).max()
    df_data[strDaysMaxDate] = df_data[df_data[CONST.STOCK_CLOSE_PRICE_ENG] == df_data[strDaysMax]][CONST.STOCK_DATE_ENG]

    df_data[strDaysMin] = df_data[CONST.STOCK_CLOSE_PRICE_ENG].rolling(window=nDays).min()
    df_data[strDaysMinDate] = df_data[df_data[CONST.STOCK_CLOSE_PRICE_ENG] == df_data[strDaysMin]][CONST.STOCK_DATE_ENG]

    df_data_extreme = df_data[df_data[strDaysMaxDate].notnull() | df_data[strDaysMinDate].notnull()]

    df_data_max = df_data_extreme[df_data_extreme[strDaysMaxDate].notnull()]
    df_data_min = df_data_extreme[df_data_extreme[strDaysMinDate].notnull()]

    df_data_max['date_index'] = df_data_max.index.tolist()
    df_data_extreme['date_diff'] = df_data_max['date_index'] - df_data_max['date_index'].shift(1)
    df_data_extreme.to_excel('E:\Code\pythonCode\StockAnalyzeProj\Data\MinMax\\' + stock_code + 'minMax.xlsx')
    print(df_data)

    return
