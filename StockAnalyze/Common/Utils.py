# 引入模块
import os
from EnumData import CONSTDEFINE as CONST
import pandas as pd
import time
import datetime
import numpy as np
from Common import ReadConfig


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)
        return True

    return False


# 根据获取的数据类型（原始数据，前复权数据，后复权数据）获取存储的文件名称
def getFileNameByAdjust(dataType):
    if dataType == CONST.STOCK_DATA_Original:
        return CONST.STOCK_DATA_ORIGNAL_FILE_NAME

    if dataType == CONST.STOCK_DATA_PreStandardized:
        return CONST.STOCK_DATA_PRE_FILE_NAME

    if dataType == CONST.STOCK_DATA_AfterStandardized:
        return CONST.STOCK_DATA_AFTER_FILE_NAME


# 计算两个日期相差天数，自定义函数名，和两个日期的变量名。
def CalDaysBetweenDates(date1, date2):
    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    # date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    # date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    date1 = time.strptime(date1, "%Y-%m-%d")

    endTime = datetime.datetime.now().strftime("%Y-%m-%d")
    date2 = time.strptime(endTime, "%Y-%m-%d")

    # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    # date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    # date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数
    return abs((date2 - date1).days)  # 将天数转成int型


# 输入日期字符串，格式"%Y-%m-%d"，分析是
def GetWeekday(strDate):
    import datetime
    nweek = datetime.datetime.strptime(strDate, "%Y-%m-%d").weekday() + 1
    return nweek


# 生成指定个数的随机数
def GenerateRandomNum(num):
    list_num = []
    while (len(set(list_num)) < num):
        list_num.append(np.random.randint(0, 300))

    return list(set(list_num))

#根据配置文件生成文件名称
def GetJLineEarnRateFileName():
    RD = ReadConfig.ReadConfig()
    param_list = RD.GetJlineItems()
    file_name = "param_J_"
    for data in param_list:
        file_name += (data[1] +"_")
    file_name += ".xlsx"
    return file_name

def CalKDJLine(stock_code, df_stock_data):
    low_list = df_stock_data[CONST.STOCK_LOWEST_ENG].rolling(9, min_periods=9).min()
    low_list.fillna(value=df_stock_data[CONST.STOCK_LOWEST_ENG].expanding().min(), inplace=True)
    high_list = df_stock_data[CONST.STOCK_HIGHEST_ENG].rolling(9, min_periods=9).max()
    high_list.fillna(value=df_stock_data[CONST.STOCK_HIGHEST_ENG].expanding().max(), inplace=True)
    rsv = (df_stock_data[CONST.STOCK_CLOSE_PRICE_ENG] - low_list) / (high_list - low_list) * 100

    df_stock_data[CONST.STOCK_K_LINE] = pd.DataFrame(rsv).ewm(com=2).mean()
    df_stock_data[CONST.STOCK_D_LINE] = df_stock_data[CONST.STOCK_K_LINE].ewm(com=2).mean()
    df_stock_data[CONST.STOCK_J_LINE] = 3 * df_stock_data[CONST.STOCK_K_LINE] - 2 * df_stock_data[CONST.STOCK_D_LINE]

    return df_stock_data

if __name__ == '__main__':
    ndays = GetWeekday('2021-08-31')
    print(ndays)
