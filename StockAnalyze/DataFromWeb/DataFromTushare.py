import tushare as ts
from StockAnalyze.EnumData import CONSTDEFINE as CONST
from StockAnalyze.Common.Utils import getFileNameByAdjustForTushare,getStockFileStorePath
from StockAnalyze.Common.Utils import mkdir,DeleteFolders
import datetime
import pandas as pd
def setToken():
    # 设置token
    token = 'ad82772c1b29371d27453121955c93099a9c48beeb048a4b2d89c8ec'
    ts.set_token(token)

    pro = ts.pro_api()
    return pro

#获取沪股通成分
def getHSs():
    pro = setToken()
    data = pro.hs_const(hs_type='SH')
    print(data)

#获取深股通成分
def getSZs():
    pro = setToken()
    data = pro.hs_const(hs_type='SZ')
    print(data)


def GetDayKline(logger,dataType = ['qfq','hfq']):
    stock_end_date = (datetime.date.today()).strftime("%Y%m%d")
    # 设置token
    token = 'ad82772c1b29371d27453121955c93099a9c48beeb048a4b2d89c8ec'
    ts.set_token(token)
    pro = ts.pro_api()
    # 查询当前所有正常上市交易的股票列表(获取基础信息数据，包括股票代码、名称、上市日期、退市日期等)
    df_stock_info = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    list_stock = df_stock_info[['ts_code','list_date']].values.tolist()
    rename_list = {CONST.STOCK_DATE_TEMP_ENG: CONST.STOCK_DATE_ENG,
                   CONST.STOCK_CODE_TEMP_ENG:CONST.STOCK_CODE_ENG,
                   CONST.STOCK_DEAL_COUNT_TEMP_ENG:CONST.STOCK_DEAL_COUNT_ENG,
                   CONST.STOCK_PCT_TEMP_CHG:CONST.STOCK_PCT_CHG,
                   CONST.STOCK_PRE_CLOSE_PRICE_TEMP_ENG:CONST.STOCK_PRE_CLOSE_PRICE_ENG}

    for stock_info in list_stock:
        stock_code= stock_info[0]
        if str(stock_code).endswith('.SH'):
            continue
        stock_start_date = stock_info[1]
        folder_path = getStockFileStorePath(stock_code,CONST.STOCK_DATA_FOLDER_PATH)
        mkdir(folder_path)

        for adj1 in dataType:
            df_data = ts.pro_bar(ts_code=stock_code, adj=adj1, start_date= stock_start_date, end_date=stock_end_date)
            file_name = folder_path + "\\" + getFileNameByAdjustForTushare(adj1)
            #修改字段名称，使文件名称一致
            df1 = df_data.rename(columns=rename_list)
            df2 = df1.dropna()

            df2[CONST.STOCK_DATE_ENG] = pd.to_datetime(df2[CONST.STOCK_DATE_ENG])
            df2[CONST.STOCK_DATE_ENG] = df2[CONST.STOCK_DATE_ENG].apply(lambda x: x.strftime('%Y-%m-%d'))

            df_data1 = df2.sort_values(by=[CONST.STOCK_DATE_ENG])
            df_data1.to_excel(file_name, index=False)
            logger.info("write file:{} finished".format(file_name))
    return

def GetOrignalKLineData(logger):
    # 设置token
    token = 'ad82772c1b29371d27453121955c93099a9c48beeb048a4b2d89c8ec'
    ts.set_token(token)
    pro = ts.pro_api()
    df_stock_info = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    list_stock = df_stock_info['ts_code'].values.tolist()

    list_str_stock = []
    str_stock = ''

    #因每次请求不能超过1000个，因此需要分段请求。
    num_cal = 0
    for stock_code in list_stock:
        str_stock += stock_code + ','
        num_cal+=1
        if num_cal == 999:
            list_str_stock.append(str_stock)
            str_stock = ''
            num_cal=0
    list_str_stock.append(str_stock)
    end_time = (datetime.date.today()).strftime("%Y%m%d")

    orgin_num =0
    for request_code in list_str_stock:
        orgin_num+=1
        file_name = CONST.STOCK_DATA_FOLDER_PATH + "\\" + str(orgin_num) + '_orginal.xlsx'
        logger.info("begin to request {} data".format(request_code))
        df_orgin = pro.daily(ts_code=request_code, start_date='20000701', end_date=end_time)
        logger.info("finish to get data {}".format(request_code))
        df_orgin.to_excel(file_name, index=False)
        logger.info("write file:{} finished".format(file_name))
    return

if __name__ =='__main__':
    # 获取沪股通成分
    getHSs()
    print('*******************')
    getSZs()
    #ts.get_industry_classified()
