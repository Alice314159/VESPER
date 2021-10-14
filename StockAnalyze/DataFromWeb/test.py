# 导入聚宽数据的sdk
import jqdatasdk as jd

jd.auth("account", "password")

import pandas as pd
from datetime import date, timedelta

filename = 'D:\python\data\data.csv'  # 数据储存路径

# csv文件初始化
date_init = date(2013, 1, 1)
stocks = jd.get_index_stocks('000300.XSHG', date=date_init)
