from StockAnalyze.EnumData import CONSTDEFINE  as CONST
from StockAnalyze.AnalyStock import HS300Dynamic
from StockAnalyze.ReadDataFromFile import readDataFromFile as RD
from StockAnalyze.AnalyStock.BuyORSell import stockData2TradeInfo
import pandas as pd

trade_list_column = [CONST.STOCK_DATE_ENG,CONST.STOCK_CLOSE_PRICE_ENG,CONST.STOCK_BUY_SECTION,CONST.STOCK_SELL_SECTION,CONST.STOCK_SELL_IF_SECTION, CONST.STOCK_J_LINE]

PRICE_RAISE_60 = 'priceRaise60'
SELL_PRICE = 'sellPrice'
SELL_DATE = 'sellDate'

#获取每天涨幅最大的5至股票
def get5MaxAMStocks(logger,buyPeriod=20,maxStock = 2):
    stock_list = RD.ReadHS300StockCode(logger)
    #stock_list = stock_list[:3]
    df_data = HS300Dynamic.getStockListDataWithDynamicParamForManyDays(logger, stock_list,maxStock)
    df_data.to_excel('max10.xlsx')

    #每隔20行取数据
    print(df_data)
    date_list = df_data[CONST.STOCK_DATE_ENG].drop_duplicates().values.tolist()

    #for j in range(20):
    row_list =[]
    for i in range(0, len(date_list), buyPeriod):  ##每隔20行取数据
        row_list.append(date_list[i])

    df_buy_data = df_data[df_data[CONST.STOCK_DATE_ENG].isin(row_list[:-1])]

    initMoney = 10000
    for date,value in df_buy_data.groupby(df_buy_data[CONST.STOCK_DATE_ENG]):
        buy_date = date
        sell_date = set(value[SELL_DATE].tolist())
        stock_trade_list = value[CONST.STOCK_CODE_ENG].tolist()

        stock_num = len(value)
        temp_money = round(initMoney/stock_num,2)
        currentMoney = 0
        for stock_code,buy_price,sell_price in zip(value[CONST.STOCK_CODE_ENG],value[CONST.STOCK_OPEN_PRICE_ENG],value[CONST.STOCK_CLOSE_PRICE_ENG]):
            earnMoney = round(temp_money *(sell_price/buy_price),2)
            currentMoney += round(temp_money *(sell_price/buy_price),2)
            logger.info('stock-{},buy info:{}~{},sell info:{}~{},money:{}~{}'.format(stock_code,buy_date,buy_price,sell_date,sell_price,temp_money,earnMoney))

        initMoney = currentMoney

    logger.info('from {} to {} earn money {}'.format(str(row_list[0]),str(row_list[-1]),initMoney))


