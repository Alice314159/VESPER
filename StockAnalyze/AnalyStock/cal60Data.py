import EnumData.CONSTDEFINE as CONST
from EnumData.EnumInfo import StockTrade

from AnalyStock.BuyORSell import stockData2TradeInfo



def _calMa60Data(df_stock_data):
    df_stock_data[CONST.STOCK_60_MEAN_ENG] = df_stock_data[CONST.STOCK_CLOSE_ENG].rolling(window=60).mean()
    return df_stock_data


# 获取收盘价低于60日线20%的数据
def getClosingPriceLowerMa60(stock_code,df_stock_data):
    df_stock_data[CONST.STOCK_60_MEAN_ENG] = df_stock_data[CONST.STOCK_CLOSE_PRICE_ENG].rolling(window=60).mean()
    df_stock_data[CONST.STOCK_SELL_SECTION]  = df_stock_data[CONST.STOCK_60_MEAN_ENG] * 1.2 <= df_stock_data[CONST.STOCK_CLOSE_PRICE_ENG]
    df_stock_data[CONST.STOCK_BUY_SECTION] = df_stock_data[CONST.STOCK_60_MEAN_ENG] * 0.8 >= df_stock_data[CONST.STOCK_CLOSE_PRICE_ENG]

    dict_trade_info_total = stockData2TradeInfo(df_stock_data)
    return dict_trade_info_total



if __name__ == '__main__':
    print()
