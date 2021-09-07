import numpy as np
import pandas as pd

file_total_stock = "E:\pythonCode\StockData\stockCode.xlsx"
file_set_stock = "E:\pythonCode\StockData\\30020210904.xls"
pd_total_stock = pd.read_excel(file_total_stock)
list_total_stock = pd_total_stock.values.tolist()
print(list_total_stock)

pd_set_stock = pd.read_excel(file_set_stock)
list_set_stock = pd_set_stock.values.tolist()
print(list_set_stock)


ss = pd_total_stock[pd_total_stock['symbol'] in pd_set_stock['代码']]
ss.to_excel('aa.xlsx')
print(ss)
