#股票名称
STOCK_NAME_ENG = 'stockName'
#股票代码
STOCK_CODE_ENG = 'code'
#日期
STOCK_DATE_ENG = 'date'
#开盘价
STOCK_OPEN_PRICE_ENG = 'open'
#收盘价
STOCK_CLOSE_PRICE_ENG = 'close'
#最高价
STOCK_HIGHEST_ENG = 'high'
#最低价
STOCK_LOWEST_ENG = 'low'
#成交量
STOCK_DEAL_COUNT_ENG = 'volume'
#成交额
STOCK_DEAL_MONEY_ENG = 'amount'
#交易状态
STOCK_TRADE_STATUS = 'tradestatus'
#涨跌幅（百分比）日涨跌幅=[(指定交易日的收盘价-指定交易日前收盘价)/指定交易日前收盘价]*100%
STOCK_PCT_CHG = 'pctChg'
#滚动市盈率
#(指定交易日的股票收盘价/指定交易日的每股盈余TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/归属母公司股东净利润TTM
STOCK_PETTM_ENG = 'peTTM'
#换手率
STOCK_TURN_OVER_RATE_ENG  = 'turn'
#市净率
#(指定交易日的股票收盘价/指定交易日的每股净资产)=总市值/(最近披露的归属母公司股东的权益-其他权益工具)
STOCK_PBMRQ_ENG = 'pbMRQ'
#滚动市销率
#(指定交易日的股票收盘价/指定交易日的每股销售额)=(指定交易日的股票收盘价*截至当日公司总股本)/营业总收入TTM
STOCK_PSTTM_ENG = 'psTTM'
#滚动市现率
#(指定交易日的股票收盘价/指定交易日的每股现金流TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/现金以及现金等价物净增加额TTM
STOCK_PCFNCFTTM_ENG = 'pcfNcfTTM'

#是否ST股，1是，0否
STOCK_IS_ST_ENG = 'isST'
#三十日均值
STOCK_30_MEAN_ENG = 'Stock30Mean'
#六十日均值
STOCK_60_MEAN_ENG = 'Stock60Mean'
#二十日均线
STOCK_20_MEAN_ENG = 'Stock20Mean'
#六十日线的交易字段
STOCK_TRADE_ENG = 'StockTrade'

#股票的KDJ线
STOCK_K_LINE = 'K-Line'
STOCK_D_LINE = 'D-Line'
STOCK_J_LINE = 'J-Line'
#计算KDJ的参数指标.日KDJ线对股价反应敏感是日常买卖进出的重要方法。
#默认参数为9，短期可以将参数修正为5，反应敏捷迅速准确，降低钝化现象。常用的参数有5,9,19,36,45,73等。
STOCK_KDJ_DAY_PARAM = 9
#对于做小波段的短线客来说，30MIn和60min的KDJ是重要指标。对于已制定买卖计划的即刻下单投资，5MIN和15MIN的KDJ线是进出参考
STOCK_KDJ_MIN_PARAM = 5

#KDJ计算买卖信号
STOCK_BUY_SECTION = 'BUY'
STOCK_SELL_SECTION = 'SELL'
STOCK_SELL_IF_SECTION = 'SELL_IF'

#################################
#文件存储相关
STOCK_FOLDER_PATH = '..\Data\StockData'
#STOCK_FOLDER_PATH = 'Z:\\'
#当天的实时数据
STOCK_REAL_FOLDER_PATH = '..\Data\RealData'
#股票的原始数据信息
STOCK_DATA_ORIGNAL_FILE_NAME = "original_data.xlsx"
#股票的前复权数据信息
STOCK_DATA_PRE_FILE_NAME = "pre_data.xlsx"
#股票的后复权数据信息
STOCK_DATA_AFTER_FILE_NAME = "after_data.xlsx"

STOCK_CODE_FILE_NAME = "stockCode.xlsx"




#股票的数据类型
# adjustflag：复权类型，默认不复权：3；
# 1：后复权；
# 2：前复权.
# 参数对应baostock中获取数据参数
STOCK_DATA_Original = "3"
STOCK_DATA_PreStandardized = "2"
STOCK_DATA_AfterStandardized = "1"


#低于六十日线20%则买入，高出六十线的15%则卖出
STOCK_60_BUY_THRESHOLD = 0.2
STOCK_60_SELL_THRESHOLD = 0.15


#买卖策略，正常买卖，止盈卖出，止损卖出
STOCK_BUY_COMMON = 'buyCommon'
STOCK_SELL_COMMON = 'SellCommon'
STOCK_SELL_STOP_LOSS = 'stopLoss'
STOCK_SELL_TAKE_PROFIT = 'takeProfit'

#上证指数，沪深指数
SH_INDEX_CODE = 'SH.000001'
SZ_INDEX_CODE = 'SZ.399106'


#表达式定义
ExPression_Equal = '=='
ExPression_Bigger = '>'
ExPression_Smaller = '<'
