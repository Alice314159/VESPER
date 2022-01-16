# 引入模块
import os
from StockAnalyze.EnumData import CONSTDEFINE as CONST
import shutil
import time
import datetime
import numpy as np
from dateutil.parser import parse
from StockAnalyze.Common import ReadConfig
import math
from dateutil.relativedelta import relativedelta


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

def getStockFileStorePath(stock_code,parent_path):
    stock_info = stock_code.split('.')
    stock_suffix = str(stock_info[0]).upper()
    if stock_suffix in ['SH','SZ','BZ']:
        return parent_path + "\\" + stock_suffix + "\\" + stock_info[1]
    else:
        return parent_path + "\\" + stock_info[1] + "\\" + stock_suffix



def getFileNameByAdjustForTushare(dataType):
    if dataType == 'qfq':
        return CONST.STOCK_DATA_PRE_FILE_NAME

    elif dataType == 'hfq':
        return CONST.STOCK_DATA_AFTER_FILE_NAME
    else:
        return CONST.STOCK_DATA_ORIGNAL_FILE_NAME

# 根据获取的数据类型（原始数据，前复权数据，后复权数据）获取存储的文件名称
def getFileNameByAdjust(dataType):
    if dataType == CONST.STOCK_DATA_Original:
        return CONST.STOCK_DATA_ORIGNAL_FILE_NAME

    if dataType == CONST.STOCK_DATA_PreStandardized:
        return CONST.STOCK_DATA_PRE_FILE_NAME

    if dataType == CONST.STOCK_DATA_AfterStandardized:
        return CONST.STOCK_DATA_AFTER_FILE_NAME


# 计算两个日期相差天数，自定义函数名，和两个日期的变量名。
def CalDaysBetweenDates(beginDate, EndDate):
    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    # date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    # date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    date1 = time.strptime(beginDate, "%Y-%m-%d")

    endTime = datetime.datetime.now().strftime("%Y-%m-%d")
    date2 = time.strptime(endTime, "%Y-%m-%d")

    # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    # date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    # date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数
    return abs((date2 - date1).days)  # 将天数转成int型


# 输入日期字符串，格式"%Y-%m-%d"，分析是周几
def GetWeekday(strDate):
    import datetime
    nweek = datetime.datetime.strptime(strDate, "%Y-%m-%d").weekday() + 1
    return nweek


def GetNdaysBefore(ndays=90):
    import datetime
    date_ago = (datetime.datetime.now() - datetime.timedelta(ndays)).strftime('%Y-%m-%d')
    return date_ago


# 生成指定个数的随机数
def GenerateRandomNum(num):
    list_num = []
    while (len(set(list_num)) < num):
        list_num.append(np.random.randint(0, 300))

    return list(set(list_num))


# 根据配置文件生成文件名称
def GetJLineEarnRateFileName(earn_money=10000):
    RD = ReadConfig.ReadConfig()
    param_list = RD.GetJlineItems()
    file_name = CONST.STOCK_TEMP_FOLDER_PATH + "\\" + "param_J_" + str(earn_money) + '_'
    for data in param_list:
        if data[1] == '':
            continue
        file_name += (data[1] + "_")
    file_name += ".xlsx"
    return file_name


def DeleteFolders(folderpath):
    isExists = os.path.exists(folderpath)
    # 判断结果
    if isExists:
        shutil.rmtree(folderpath)
    return


# 输入日期，转换为星期函数,0-星期一；6-星期日
def Date2Week(strDate):
    return parse(strDate).weekday()


# 输入两个日期，计算两个日期之间的天数
def Date2DateDays(strDate1, strDate2):
    ndays = parse(strDate1) - parse(strDate2)
    return abs(ndays.days)


#获取最近几个季度的开始和结束日期,参数默认1，计算上一个季度
def GetNQuartersDate(lastNQuarters = 1):
    nowdays = datetime.datetime.now()
    lastDateInfo = nowdays - relativedelta(months=lastNQuarters*3)

    #计算历史季度
    lastInYead = lastDateInfo.year
    lastInMonth = lastDateInfo.month
    quarterMonth = 3*math.floor(lastInMonth/3) + 1

    quarterBeginDate = datetime.datetime(lastInYead,quarterMonth,1)
    quarterEndDate = quarterBeginDate + relativedelta(months=3) - datetime.timedelta(days=1)

    str_quarterBeginDate = quarterBeginDate.strftime('%Y%m%d')
    str_quarterEndDate = quarterEndDate.strftime('%Y%m%d')

    return (str_quarterBeginDate,str_quarterEndDate)

if __name__ == '__main__':
    ndays = Date2DateDays('2021-11-07', '2021-11-10')
    aa = GetNQuartersDate(14)
    print(aa)
