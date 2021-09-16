import StockAnalyze.EnumData.CONSTDEFINE as CONST
import matplotlib.pyplot as plt


# 统计股票的在每周的涨跌
def staticsSingleStockForWeek(stock_code, df_stock_data):

    return


# 统计每个月的股票的涨跌情况
def staticsSingleStockForMonth(stock_code, df_stock_data):
    return


# 统计每个月1-31号的股票的涨跌情况
def staticsSingleStockForMonth(stock_code, df_stock_data):
    return


# 统计股票的交易量
def staticSingleStockForVolume(stock_code, df_stock_data):
    df_stock_data = df_stock_data[df_stock_data[CONST.STOCK_DATE_ENG] >= '2021-07-01']
    df_stock_data.index = df_stock_data[CONST.STOCK_DATE_ENG]

    color_dict = {CONST.STOCK_DEAL_COUNT_ENG: '#BBBBBB', CONST.STOCK_CLOSE_PRICE_ENG: '#F9D587',
                  CONST.STOCK_J_LINE: '#FF00FF'}

    plt.figure(figsize=(12, 6))

    plt.subplot(211)
    plt.xticks(fontsize=5)
    plt.legend(loc=0)  # 设置图例在左上方
    plt.title(stock_code)
    df_stock_data[CONST.STOCK_DEAL_COUNT_ENG].plot(label=CONST.STOCK_DEAL_COUNT_ENG,
                                                   color=color_dict[CONST.STOCK_DEAL_COUNT_ENG],
                                                   rot=20)

    plt.subplot(212)
    plt.xticks(fontsize=6)
    plt.legend(loc=0)  # 设置图例在左上方
    df_stock_data[CONST.STOCK_CLOSE_PRICE_ENG].plot(label=CONST.STOCK_CLOSE_PRICE_ENG, grid=True,
                                                    color=color_dict[CONST.STOCK_CLOSE_PRICE_ENG], rot=20)

    plt.show()
    print(df_stock_data)
    return


# 统计股票的证跌幅
def staticSingleStockForAM(stock_code, df_stock_data):
    return
