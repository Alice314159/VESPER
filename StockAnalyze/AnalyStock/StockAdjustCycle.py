# 计算股票的调整周期
import pandas as pd

from StockAnalyze.ReadDataFromFile import readDataFromFile as RD
import StockAnalyze.EnumData.CONSTDEFINE as CONST
import StockAnalyze.Common.Drawing as Draw

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

        Draw.DrawingKine(logger,stock_code,df_single)

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
    strMax = 'maxClose'
    strMin = 'minClose'
    strMaxDate = 'maxDate'
    strMinDate = 'minDate'

    #1.查找20日内收盘价的最值
    df_data[strMax] = df_data[CONST.STOCK_CLOSE_PRICE_ENG].rolling(window=nDays).max()
    df_data[strMin] = df_data[CONST.STOCK_CLOSE_PRICE_ENG].rolling(window=nDays).min()

    #2.查找收盘价20日内最高价的日期，并转换为dataFrame形式
    close_price_list = df_data[CONST.STOCK_CLOSE_PRICE_ENG].values.tolist()
    date_list = df_data[CONST.STOCK_DATE_ENG].values.tolist()
    list_data =[]
    for i in range(nDays,len(close_price_list)-1):
        list_temp = close_price_list[i-nDays:i]
        data_min = min(list_temp)
        min_index = list_temp.index(data_min)
        min_date = date_list[i-nDays+min_index]

        data_max = max(list_temp)
        max_index = list_temp.index(data_max)
        max_date = date_list[i - nDays + max_index]

        list_data.append((stock_code,date_list[i-1],close_price_list[i-1],data_min,min_date,data_max,max_date))
    df_data_extreme = pd.DataFrame(list_data,columns=[CONST.STOCK_CODE_ENG,CONST.STOCK_DATE_ENG,CONST.STOCK_CLOSE_PRICE_ENG,strMin,strMinDate,strMax,strMaxDate])

    df_data_extreme.to_excel('E:\Code\pythonCode\StockAnalyzeProj\Data\MinMax\\' + stock_code + '.xlsx')

    #3.分组，计算每个最值出现的次数,分组以后，每一列的统计结果值都相同为统计的个数。
    df_count = df_data_extreme.groupby(strMaxDate).count()
    list_extreme_days = []
    nThreshod = max(nDays/4,2)
    for date, row in df_count.iterrows():
        #最大值在rolling窗口期存在的时长
        maxDays = row[strMax]
        if maxDays >= nThreshod:
            list_extreme_days.append((date,maxDays))

    print(list_extreme_days)



    return
