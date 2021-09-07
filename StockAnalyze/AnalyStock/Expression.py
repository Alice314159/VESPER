import datetime
import EnumData.ConfigParam as PARAM
import EnumData.CONSTDEFINE as CONST
from EnumData.EnumInfo import StockTrade
from DingTalk import SendMsg as DT
import Common.Utils as utils
import pandas as pd

#获取满足条件的上证指数日期
def GetCompositeIndexDateList(logger,df_data,thresh,section = CONST.STOCK_J_LINE,expression = '>'):
    list_date = []
    df_res = pd.DataFrame(columns = df_data.columns)
    if expression not in [CONST.ExPression_Equal,CONST.ExPression_Bigger,CONST.ExPression_Smaller]:
        logger.warn("expression is {},not right,please check".format(expression))
        return []
    if expression == CONST.ExPression_Equal:
        df_res = df_data[df_data[CONST.STOCK_J_LINE] == thresh]
    elif expression == CONST.ExPression_Bigger:
        df_res = df_data[df_data[CONST.STOCK_J_LINE] > thresh]
    elif expression == CONST.ExPression_Smaller:
        df_res = df_data[df_data[CONST.STOCK_J_LINE] < thresh]
    else:
        logger.warn('unknown expression!')
        return []

    list_date = df_res[CONST.STOCK_DATE_ENG].tolist()
    return list_date
