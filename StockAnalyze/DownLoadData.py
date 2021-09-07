from GetStockData import GetDataFromWeb as DownLoadStockData
from GetStockData import GetCompositeIndex as DownLoadCompositeData
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
from datetime import datetime


# 输出时间
def job():
    strnum = paramParse()
    DownLoadCompositeData.GetCompositeIndex(logger)
    DownLoadStockData.TimeToGetDataRunForEveryDay(logger,strnum)


job()
scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', day_of_week='1-5', hour=18, minute=30)
scheduler.start()
