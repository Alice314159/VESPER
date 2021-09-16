import EnumData.CONSTDEFINE as CONST
import EnumData.ConfigParam as PARAM
import pandas as pd
from AnalyStock.BuyORSell import stockData2TradeInfo
import matplotlib.pyplot as plt
from Common import ReadConfig
from Common import Utils
Config = ReadConfig.ReadConfig()


# 超买超卖信号
# 根据KDJ的取值，可将其划分为几个区域，即超买区、超卖区和徘徊区。
# 按一般划分标准，K、D、J这三值在20以下为超卖区，是买入信号；
# K、D、J这三值在80以上为超买区，是卖出信号；
# K、D、J这三值在20—80之间为徘徊区，宜观望。
def _calDataBuyOrSell(stock_code, df_stock_data):
    # 获取拆卖区域，并发送买入信号
    df_stock_data[CONST.STOCK_BUY_SECTION] = (df_stock_data[CONST.STOCK_K_LINE] <= 20) & \
                                             (df_stock_data[CONST.STOCK_D_LINE] <= 20) & \
                                             (df_stock_data[CONST.STOCK_J_LINE] <= 20)

    # K、D、J这三值在80以上为超买区，是卖出信号；
    df_stock_data[CONST.STOCK_SELL_SECTION] = (df_stock_data[CONST.STOCK_K_LINE] >= 80) & \
                                              (df_stock_data[CONST.STOCK_D_LINE] >= 80) & \
                                              (df_stock_data[CONST.STOCK_J_LINE] >= 80)

    df_stock_data_trade = df_stock_data[
        df_stock_data[CONST.STOCK_BUY_SECTION] != df_stock_data[CONST.STOCK_SELL_SECTION]]

    dict_trade_info = stockData2TradeInfo(df_stock_data_trade)
    return dict_trade_info


def _calPerfectPointAndDeathPoint(stock_code, df_stock_data):
    # df_stock_data_trade = df_stock_data[
    #     df_stock_data[CONST.STOCK_BUY_SECTION] != df_stock_data[CONST.STOCK_SELL_SECTION]]

    # 当股价经过一段很长时间的低位盘整行情，并且K、D、J三线都处于50线以下时，
    # 一旦J线和K线几乎同时向上突破D线时，表明股市即将转强，股价跌势已经结束，将止跌朝上，可以开始买进股票，进行中长线建仓。
    # 这是KDJ指标“黄金交叉”的一种形式。

    df_stock_data['lower50'] = (df_stock_data[CONST.STOCK_K_LINE] < 50) & \
                               (df_stock_data[CONST.STOCK_D_LINE] < 50) & \
                               (df_stock_data[CONST.STOCK_J_LINE] < 50)

    df_stock_data['JKbiggerD'] = (df_stock_data[CONST.STOCK_J_LINE] > df_stock_data[CONST.STOCK_D_LINE]) & \
                                 (df_stock_data[CONST.STOCK_K_LINE] > df_stock_data[CONST.STOCK_D_LINE])

    df_stock_data['JKSmallerD'] = (df_stock_data[CONST.STOCK_J_LINE] < df_stock_data[CONST.STOCK_D_LINE]) & \
                                  (df_stock_data[CONST.STOCK_K_LINE] < df_stock_data[CONST.STOCK_D_LINE])

    df_stock_data[CONST.STOCK_BUY_SECTION] = df_stock_data['lower50'] & df_stock_data['JKbiggerD'] & df_stock_data[
        'JKSmallerD'].shift(1)

    # 2当股价经过一段时间的上升过程中的盘整行情，并且K、D、J线都处于50线附近徘徊时，
    # 一旦J线和K线几乎同时再次向上突破D线，成交量再度放出时，
    # 表明股市处于一种强势之中，股价将再次上涨，可以加码买进股票或持股待涨，这就是KDJ指标“黄金交叉”的一种形式。

    # 3当股价经过前期一段很长时间的上升行情后，股价涨幅已经很大的情况下，一旦J线和K线在高位（80
    # 以上）几乎同时向下突破D线时，表明股市即将由强势转为弱势，股价将大跌，这时应卖出大部分股票而不能买股票，这就是KDJ指标的“死亡交叉”的一种形式。
    df_stock_data['bigger80'] = (df_stock_data[CONST.STOCK_K_LINE] > 80) & \
                                (df_stock_data[CONST.STOCK_D_LINE] > 80) & \
                                (df_stock_data[CONST.STOCK_J_LINE] > 80)

    df_stock_data[CONST.STOCK_SELL_SECTION] = df_stock_data['bigger80'] & df_stock_data['JKbiggerD'].shift(1) & \
                                              df_stock_data[
                                                  'JKSmallerD']

    # 4当股价经过一段时间的下跌后，而股价向上反弹的动力缺乏，各种均线对股价形成较强的压力时，KDJ曲线在经过短暂的反弹到80线附近，但未能重返80线以上时，一旦J线和K线再次向下突破D线时，表明股市将再次进入极度弱市中，股价还将下跌，可以再
    # 卖出股票或观望，这是KDJ指标“死亡交叉”的另一种形式。

    df_stock_data_trade = df_stock_data.loc[:, [CONST.STOCK_DATE_ENG, CONST.STOCK_BUY_SECTION, CONST.STOCK_SELL_SECTION,
                                                CONST.STOCK_CLOSE_PRICE_ENG]]
    # df_stock_data_trade.to_excel("buyData.xlsx")
    # print(df_stock_data_trade)

    df_stock_data_trade = df_stock_data_trade[
        df_stock_data[CONST.STOCK_BUY_SECTION] != df_stock_data[CONST.STOCK_SELL_SECTION]]

    dict_trade_info = stockData2TradeInfo(stock_code,df_stock_data_trade)
    return dict_trade_info


def CalDataByKDJ(stock_code, df_stock_data):
    df_kdj_data = Utils.CalKDJLine(stock_code, df_stock_data)
    # 超买超买点
    # dict_trade = _calDataBuyOrSell(stock_code, df_kdj_data)

    # 黄金交叉点和死亡交叉
    dict_trade_point = _calPerfectPointAndDeathPoint(stock_code, df_kdj_data)

    return dict_trade_point



