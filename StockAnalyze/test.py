import efinance as ef
from GetStockCode import getStockCodeInfo
from Common import Logger
logger = Logger.log()

# 股票代码
stock_code = '600519'
# 数据间隔时间为 1 分钟
freq = 1
# 获取最新一个交易日的分钟级别股票行情数据
df = ef.stock.get_quote_history(stock_code, klt=freq)
# 将数据存储到 csv 文件中
df.to_csv(f'{stock_code}.csv', encoding='utf-8-sig', index=None)
print(f'股票: {stock_code} 的行情数据已存储到文件: {stock_code}.csv 中！')


stock_code_list = getStockCodeInfo.getAllStockCodeFromFile(logger)
for stock in stock_code_list:
    stock_code_temp = stock.split(".")
    stock_code = stock_code_temp[1]
    # 获取最新一个交易日的分钟级别股票行情数据
    df = ef.stock.get_quote_history(stock_code, klt=freq)
    # 将数据存储到 csv 文件中
    df.to_excel(f'{stock_code}.xlsx')
    print(f'股票: {stock_code} 的行情数据已存储到文件: {stock_code}.xlsx 中！')

