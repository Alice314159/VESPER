import sys
import os
path = os.path.abspath('..')
sys.path.extend([path])

from GetStockData import GetDataFromWeb as DownLoadStockData
from GetStockData import GetCompositeIndex as DownLoadCompositeData
from EnumData import EnumInfo as EnumData
from GetStockCode import getStockCodeInfo
from DataFromWeb import DataFromTushare
import sys
from multiprocessing import Process
from loguru import logger
logger.add("../Log/downLoad.log", rotation="1 MB")


print(sys.argv)




def paramParse():
    strnum = ""
    if len(sys.argv) > 1:
        strnum = str(sys.argv[1]).upper()

        grouplist = ["SZ", "SH"]
        for i in range(10):
            grouplist.append(str(i))

        if strnum not in grouplist:
            strnum = ""
            print("arg :{} input wrong".format(str(sys.argv[1])))
    else:
        print("arg input nothing")

    return strnum


from apscheduler.schedulers.blocking import BlockingScheduler


# 每天执行一次的任务，每天下午六点半执行
def GetDataForDay(logger):
    strnum = paramParse()
    getStockCodeInfo.getAllStockCodeFromWeb(logger)
    DownLoadStockData.TimeToGetDataRunForEveryDay(logger, EnumData.StockCodeType.StockTypeAll, strnum)


def GetDataByTushare(logger):
    strnum = paramParse()
    DataFromTushare.GetDayKline(logger)
    DownLoadCompositeData.GetCompositeIndex(logger)
    DownLoadStockData.TimeToGetDataRunForEveryDay(logger, EnumData.StockCodeType.StockHS300, strnum)

def GetRealDataForMin():
    DownLoadStockData.TimeToGetDataRunForEveryMin(logger)



# scheduler = BlockingScheduler()
# scheduler.add_job(GetDataForDay, 'cron', day_of_week='0-4', hour=18, minute=30)
# # scheduler.add_job(GetRealDataForMin,trigger='interval', minutes=5,next_run_time=datetime.now())
# scheduler.start()
if __name__ == '__main__':
    GetDataByTushare(logger)
    GetDataForDay(logger)

    # p1 = Process(target=GetDataByTushare, args=(logger,))
    # p1.start()
    #
    # p2 = Process(target=GetDataForDay, args=(logger,))
    # p2.start()
