from GetStockData import GetDataFromWeb as DownLoadStockData
from GetStockData import GetCompositeIndex as DownLoadCompositeData
from EnumData import EnumInfo as EnumData
from EnumData import CONSTDEFINE as CONST
from GetStockCode import getStockCodeInfo
import sys
from Common.Utils import DeleteDataUnderFolders

print(sys.argv)

from Common import Logger

logger = Logger.log()


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
def GetDataForDay():
    strnum = paramParse()
    getStockCodeInfo.getAllStockCodeFromWeb(logger)

    DeleteDataUnderFolders(CONST.STOCK_DATA_FOLDER_PATH)
    DownLoadCompositeData.GetCompositeIndex(logger)
    DownLoadStockData.TimeToGetDataRunForEveryDay(logger, EnumData.StockCodeType.StockHS300, strnum)


def GetRealDataForMin():
    DownLoadStockData.TimeToGetDataRunForEveryMin(logger)


GetDataForDay()
scheduler = BlockingScheduler()
scheduler.add_job(GetDataForDay, 'cron', day_of_week='1-5', hour=18, minute=30)
# scheduler.add_job(GetRealDataForMin,trigger='interval', minutes=5,next_run_time=datetime.now())
scheduler.start()
