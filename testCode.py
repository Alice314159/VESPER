import tushare as ts
import pandas as pd

# 获取所有股票编号，并存入文件

# 设置token
token = 'ad82772c1b29371d27453121955c93099a9c48beeb048a4b2d89c8ec'
ts.set_token(token)
pro = ts.pro_api()
# 查询当前所有正常上市交易的股票列表(获取基础信息数据，包括股票代码、名称、上市日期、退市日期等)
df_stock_info = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

data = pd.DataFrame(df_stock_info)
data.to_excel('stock_code.xlsx', sheet_name='data')
