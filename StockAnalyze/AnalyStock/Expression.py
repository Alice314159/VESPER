import StockAnalyze.EnumData.ConfigParam as PARAM
import StockAnalyze.EnumData.CONSTDEFINE as CONST
from StockAnalyze.AnalyStock import ParamCal
import pandas as pd

#获取满足条件的上证指数日期
def GetCompositeIndexDateList(logger,stock_code,df_data,thresh,section = CONST.STOCK_J_LINE,expression = '>'):
    df_res = pd.DataFrame(columns = [CONST.STOCK_DATE_ENG,CONST.STOCK_SZ_JLINE_THRES])
    if expression not in [CONST.ExPression_Equal,CONST.ExPression_Bigger,CONST.ExPression_Smaller]:
        logger.warn("stock {},expression is {},not right,please check".format(stock_code,expression))
        return df_res
    if expression == CONST.ExPression_Equal:
        df_data[CONST.STOCK_SZ_JLINE_THRES] = df_data[df_data[CONST.STOCK_J_LINE] == thresh]
    elif expression == CONST.ExPression_Bigger:
        df_data[CONST.STOCK_SZ_JLINE_THRES] = df_data[df_data[CONST.STOCK_J_LINE] > thresh]
    elif expression == CONST.ExPression_Smaller:
        df_data[CONST.STOCK_SZ_JLINE_THRES] = df_data[df_data[CONST.STOCK_J_LINE] < thresh]
    elif expression == CONST.ExPression_Smaller_Equal:
        df_data[CONST.STOCK_SZ_JLINE_THRES] = df_data[df_data[CONST.STOCK_J_LINE] <= thresh]
    elif expression == CONST.ExPression_Bigger_Equal:
        df_data[CONST.STOCK_SZ_JLINE_THRES] = df_data[df_data[CONST.STOCK_J_LINE] >= thresh]
    else:
        logger.warn('stock_code{},unknown expression{}!'.format(stock_code,expression))
        return df_res

    df = df_data.loc[:,[CONST.STOCK_DATE_ENG,CONST.STOCK_SZ_JLINE_THRES]]
    return df

#买入价格和60日均线价格之间的关系
def GetSatisfyBuyPriceAnd60Means(logger,stock_code,df_data,thresh,expression = '>'):
    df_data = df_data.loc[:,[CONST.STOCK_DATE_ENG,CONST.STOCK_CLOSE_PRICE_ENG]]
    df_data = ParamCal.calMa60Data(df_data)
    if expression == CONST.ExPression_Equal:
        df_data[PARAM.BUY_PRICE_60_MEANS] = (df_data[CONST.STOCK_CLOSE_PRICE_ENG]/df_data[CONST.STOCK_60_MEAN_ENG]) == thresh
    elif expression == CONST.ExPression_Bigger:
        df_data[CONST.BUY_PRICE_60_MEANS] = (df_data[CONST.STOCK_CLOSE_PRICE_ENG]/df_data[CONST.STOCK_60_MEAN_ENG]) > thresh
    elif expression == CONST.ExPression_Smaller:
        df_data[CONST.BUY_PRICE_60_MEANS] = (df_data[CONST.STOCK_CLOSE_PRICE_ENG]/df_data[CONST.STOCK_60_MEAN_ENG])< thresh
    elif expression == CONST.ExPression_Smaller_Equal:
        df_data[CONST.BUY_PRICE_60_MEANS] = (df_data[CONST.STOCK_CLOSE_PRICE_ENG]/df_data[CONST.STOCK_60_MEAN_ENG]) <= thresh
    elif expression == CONST.ExPression_Bigger_Equal:
        df_data[CONST.BUY_PRICE_60_MEANS] = (df_data[CONST.STOCK_CLOSE_PRICE_ENG]/df_data[CONST.STOCK_60_MEAN_ENG]) >= thresh
    else:
        logger.warn('{} unknown expression {}!'.format(stock_code,expression))


    df = df_data.loc[:,[CONST.STOCK_DATE_ENG,CONST.BUY_PRICE_60_MEANS]]
    return df

#获取收盘价，最高价，最低价之间的关系
def GetClosePriceInHighAndLow(logger,stock_code,df_data,thresh,expression = '>'):
    df_data = df_data.loc[:,[CONST.STOCK_DATE_ENG,CONST.STOCK_CLOSE_PRICE_ENG,CONST.STOCK_HIGHEST_ENG,CONST.STOCK_LOWEST_ENG]]
    df_data['PriceVarity'] = (df_data[CONST.STOCK_CLOSE_PRICE_ENG] - df_data[CONST.STOCK_LOWEST_ENG])/(df_data[CONST.STOCK_HIGHEST_ENG] - df_data[CONST.STOCK_LOWEST_ENG])

    if expression == CONST.ExPression_Equal:
        df_data[PARAM.CLOSE_PRICE_HIGH_LOW] = df_data['PriceVarity'] == thresh
    elif expression == CONST.ExPression_Bigger:
        df_data[CONST.CLOSE_PRICE_HIGH_LOW] = df_data['PriceVarity'] > thresh
    elif expression == CONST.ExPression_Smaller:
        df_data[CONST.CLOSE_PRICE_HIGH_LOW] = df_data['PriceVarity']< thresh
    elif expression == CONST.ExPression_Smaller_Equal:
        df_data[CONST.CLOSE_PRICE_HIGH_LOW] = df_data['PriceVarity'] <= thresh
    elif expression == CONST.ExPression_Bigger_Equal:
        df_data[CONST.CLOSE_PRICE_HIGH_LOW] = df_data['PriceVarity'] >= thresh
    else:
        logger.warn('{} unknown expression {}!'.format(stock_code,expression))

    df = df_data.loc[:, [CONST.STOCK_DATE_ENG, PARAM.CLOSE_PRICE_HIGH_LOW]]
    return df


#获取收盘价，最高价，最低价之间的关系
def GetTradeMoneyVariety(logger,stock_code,df_data,thresh,expression = '>'):
    df_data = df_data.loc[:,[CONST.STOCK_DATE_ENG,CONST.STOCK_DEAL_MONEY_ENG]]
    df_data['ratio'] = df_data[CONST.STOCK_DEAL_MONEY_ENG] / df_data[CONST.STOCK_DEAL_MONEY_ENG].shift()
    if expression == CONST.ExPression_Equal:
        df_data[PARAM.TRADE_MONEY_RATE] = df_data['ratio']  == thresh
    elif expression == CONST.ExPression_Bigger:
        df_data[CONST.TRADE_MONEY_RATE] = df_data['ratio'] > thresh
    elif expression == CONST.ExPression_Smaller:
        df_data[CONST.TRADE_MONEY_RATE] = df_data['ratio']< thresh
    elif expression == CONST.ExPression_Smaller_Equal:
        df_data[CONST.TRADE_MONEY_RATE] = df_data['ratio'] <= thresh
    elif expression == CONST.ExPression_Bigger_Equal:
        df_data[CONST.TRADE_MONEY_RATE] = df_data['ratio'] >= thresh
    else:
        logger.warn('{} unknown expression {}!'.format(stock_code,expression))

    df = df_data.loc[:, [CONST.STOCK_DATE_ENG, PARAM.TRADE_MONEY_RATE]]
    return df

#J线变化趋势,默认largen=True为变大的趋势,满足则返回true,小则返回False
def GetJlineVariationTrend (logger,stock_code,df_data):
    df_data[CONST.STOCK_J_LINE_LARGEN] = df_data[CONST.STOCK_J_LINE] - df_data[CONST.STOCK_J_LINE].shift() > 0
    logger.info('stock {} jline varity'.format(stock_code))
    df = df_data.loc[:, [CONST.STOCK_DATE_ENG, CONST.STOCK_J_LINE_LARGEN]]
    return df

#J线斜率变化趋势,大于一个值
def GetJlineSlopeLargenTrend (logger,stock_code,df_data,thresh):
    df_data['diff'] = df_data[CONST.STOCK_J_LINE] - df_data[CONST.STOCK_J_LINE].shift()
    df_data[CONST.STOCK_J_SLOPE_LARGEN] = (df_data['diff'] / df_data['diff'].shift()) > thresh
    logger.info('stock {} jline  slope larger varity thresh {}'.format(stock_code,thresh))
    df = df_data.loc[:, [CONST.STOCK_DATE_ENG, CONST.STOCK_J_LINE_LARGEN]]
    return df

#J线斜率变化趋势,小于一个值
def GetJlineSlopeLowerTrend (logger,stock_code,df_data,thresh):
    df_data['diff'] = df_data[CONST.STOCK_J_LINE] - df_data[CONST.STOCK_J_LINE].shift()
    df_data[CONST.STOCK_J_SLOPE_LOWER] = (df_data['diff'] / df_data['diff'].shift()) < thresh
    logger.info('stock {} jline  slope larger varity thresh {}'.format(stock_code,thresh))
    df = df_data.loc[:, [CONST.STOCK_DATE_ENG, CONST.STOCK_J_SLOPE_LOWER]]
    return df

#J线阈值范围,要大于某一个值
def GetJlineBiggerThreshold (logger,stock_code,df_data,thresh):
    df_data[PARAM.J_LINE_BIGGER_THRESHOLD] = df_data[CONST.STOCK_J_LINE] > thresh
    df = df_data.loc[:, [CONST.STOCK_DATE_ENG, PARAM.J_LINE_BIGGER_THRESHOLD]]
    return df

#J线阈值范围,要小于某一个值
def GetJlineSmallerThreshold (logger,stock_code,df_data,thresh):
    df_data[PARAM.J_LINE_SMALLER_THRESHOLD] = df_data[CONST.STOCK_J_LINE] < thresh
    df = df_data.loc[:, [CONST.STOCK_DATE_ENG, PARAM.J_LINE_SMALLER_THRESHOLD]]
    return df

#J线收盘价与60日均线之间的关系
def GetJLineCloseWith60Means(logger,stock_code,df_data,thresh,expression = '>'):
    df_data = df_data.loc[:,[CONST.STOCK_DATE_ENG,CONST.STOCK_CLOSE_PRICE_ENG]]
    df_data = ParamCal.calMa60Data(df_data)
    if expression == CONST.ExPression_Equal:
        df_data[PARAM.BUY_PRICE_60_MEANS] = (df_data[CONST.STOCK_CLOSE_PRICE_ENG]/df_data[CONST.STOCK_60_MEAN_ENG]) == thresh
    elif expression == CONST.ExPression_Bigger:
        df_data[CONST.BUY_PRICE_60_MEANS] = (df_data[CONST.STOCK_CLOSE_PRICE_ENG]/df_data[CONST.STOCK_60_MEAN_ENG]) > thresh
    elif expression == CONST.ExPression_Smaller:
        df_data[CONST.BUY_PRICE_60_MEANS] = (df_data[CONST.STOCK_CLOSE_PRICE_ENG]/df_data[CONST.STOCK_60_MEAN_ENG])< thresh
    elif expression == CONST.ExPression_Smaller_Equal:
        df_data[CONST.BUY_PRICE_60_MEANS] = (df_data[CONST.STOCK_CLOSE_PRICE_ENG]/df_data[CONST.STOCK_60_MEAN_ENG]) <= thresh
    elif expression == CONST.ExPression_Bigger_Equal:
        df_data[CONST.BUY_PRICE_60_MEANS] = (df_data[CONST.STOCK_CLOSE_PRICE_ENG]/df_data[CONST.STOCK_60_MEAN_ENG]) >= thresh
    else:
        logger.warn('{} unknown expression {}!'.format(stock_code,expression))


    df = df_data.loc[:,[CONST.STOCK_DATE_ENG,CONST.BUY_PRICE_60_MEANS]]
    return df

