from GetStockData import GetDataFromWeb as DownLoadStockData
from GetStockData import GetCompositeIndex as DownLoadCompositeData
from datetime import datetime
import sys
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
    DownLoadCompositeData.GetCompositeIndex(logger)
    DownLoadStockData.TimeToGetDataRunForEveryDay(logger,strnum)


def GetRealDataForMin():
    DownLoadStockData.TimeToGetDataRunForEveryMin(logger)

GetDataForDay()
scheduler = BlockingScheduler()
scheduler.add_job(GetDataForDay, 'cron', day_of_week='1-5', hour=18, minute=30)
scheduler.add_job(GetRealDataForMin,trigger='interval', minutes=5,next_run_time=datetime.now())
scheduler.start()
