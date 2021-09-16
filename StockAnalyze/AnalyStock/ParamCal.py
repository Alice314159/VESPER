import sys

import pandas as pd
import StockAnalyze.EnumData.CONSTDEFINE as CONST
from StockAnalyze.ReadDataFromFile import readDataFromFile as RD



# 计算M日均线
def calMeanLineDataForDays(logger,stock_code, df_stock_data, ndays=60):
    if ndays == 20:
        df_stock_data[CONST.STOCK_20_MEAN_ENG] = df_stock_data[CONST.STOCK_CLOSE_ENG].rolling(window=ndays).mean()
    elif ndays == 30:
        df_stock_data[CONST.STOCK_30_MEAN_ENG] = df_stock_data[CONST.STOCK_CLOSE_ENG].rolling(window=ndays).mean()
    elif ndays == 60:
        df_stock_data[CONST.STOCK_60_MEAN_ENG] = df_stock_data[CONST.STOCK_CLOSE_ENG].rolling(window=ndays).mean()
    else:
        logger.warning("stock_code {} get {}-days Mean lines failed".format(stock_code,ndays))
    return df_stock_data


#计算M日内的收盘价最大值
def calMaxClosePrice(logger,stock_code, df_stock_data, ndays=60):
    if ndays == 20:
        df_stock_data[CONST.STOCK_10_CLOSE_PRICE_HIGHEST] = df_stock_data[CONST.STOCK_CLOSE_ENG].rolling(window=ndays).max()
    elif ndays == 60:
        df_stock_data[CONST.STOCK_20_CLOSE_PRICE_HIGHEST] = df_stock_data[CONST.STOCK_CLOSE_ENG].rolling(window=ndays).max()
    else:
        logger.warning("stock_code {} get {}-days Mean lines failed".format(stock_code,ndays))
    return df_stock_data


# 计算KDJ线
def calKDJLine(stock_code, df_stock_data):
    low_list = df_stock_data[CONST.STOCK_LOWEST_ENG].rolling(9, min_periods=9).min()
    low_list.fillna(value=df_stock_data[CONST.STOCK_LOWEST_ENG].expanding().min(), inplace=True)
    high_list = df_stock_data[CONST.STOCK_HIGHEST_ENG].rolling(9, min_periods=9).max()
    high_list.fillna(value=df_stock_data[CONST.STOCK_HIGHEST_ENG].expanding().max(), inplace=True)
    rsv = (df_stock_data[CONST.STOCK_CLOSE_PRICE_ENG] - low_list) / (high_list - low_list) * 100

    df_stock_data[CONST.STOCK_K_LINE] = pd.DataFrame(rsv).ewm(com=2).mean()
    df_stock_data[CONST.STOCK_D_LINE] = df_stock_data[CONST.STOCK_K_LINE].ewm(com=2).mean()
    df_stock_data[CONST.STOCK_J_LINE] = 3 * df_stock_data[CONST.STOCK_K_LINE] - 2 * df_stock_data[CONST.STOCK_D_LINE]

    return df_stock_data


# 获取上证指数，并计算上证指数的KDJ
def calCompositeIndexKDJ(logger):
    # 获取上证综合指数数据
    df_SZ_data = RD.getCompositeIndexFileData(logger, CONST.SZ_INDEX_CODE, CONST.STOCK_DATA_ORIGNAL_FILE_NAME,
                                              CONST.STOCK_FOLDER_PATH)

    df_SZ_data = calKDJLine(CONST.SZ_INDEX_CODE, df_SZ_data)

    df_SZ_data = df_SZ_data.loc[:, [CONST.STOCK_DATE_ENG, CONST.STOCK_J_LINE]]

    df_SZ_data = df_SZ_data.rename(columns={CONST.STOCK_J_LINE: CONST.STOCK_SZ_J_LINE})

    return df_SZ_data


# 多个不同的参数，相互进行交叉验证，将多个dataframe按照日期进行合并
def paramUnion(df_stock_data, df_SZ_Data):
    stock_min = df_stock_data[CONST.STOCK_DATE_ENG].min()
    df_SZ_Data = df_SZ_Data[df_SZ_Data[CONST.STOCK_DATE_ENG] >= stock_min]
    df_final = pd.merge(df_stock_data, df_SZ_Data, on=CONST.STOCK_DATE_ENG)

    df_final = df_final[df_final[CONST.STOCK_DATE_ENG] >= '2021-01-01']
    return df_final
