import EnumData.CONSTDEFINE as CONST
import EnumData.ConfigParam as PARAM
import pandas as pd
from AnalyStock.BuyORSell import stockData2TradeInfo
import matplotlib.pyplot as plt
from Common import ReadConfig
from Common import Utils
Config = ReadConfig.ReadConfig()


# # 计算9日KDJ线
# def _calKDJData(stock_code, df_stock_data):
#     low_list = df_stock_data[CONST.STOCK_LOWEST_ENG].rolling(9, min_periods=9).min()
#     low_list.fillna(value=df_stock_data[CONST.STOCK_LOWEST_ENG].expanding().min(), inplace=True)
#     high_list = df_stock_data[CONST.STOCK_HIGHEST_ENG].rolling(9, min_periods=9).max()
#     high_list.fillna(value=df_stock_data[CONST.STOCK_HIGHEST_ENG].expanding().max(), inplace=True)
#     rsv = (df_stock_data[CONST.STOCK_CLOSE_PRICE_ENG] - low_list) / (high_list - low_list) * 100
#
#     df_stock_data[CONST.STOCK_K_LINE] = pd.DataFrame(rsv).ewm(com=2).mean()
#     df_stock_data[CONST.STOCK_D_LINE] = df_stock_data[CONST.STOCK_K_LINE].ewm(com=2).mean()
#     df_stock_data[CONST.STOCK_J_LINE] = 3 * df_stock_data[CONST.STOCK_K_LINE] - 2 * df_stock_data[CONST.STOCK_D_LINE]
#
#     testSwitch = 0
#     if testSwitch == 1:
#         df_stock_data = df_stock_data[df_stock_data[CONST.STOCK_DATE_ENG] >= '2021-08-01']
#
#         df_stock_data.index = df_stock_data[CONST.STOCK_DATE_ENG]
#         color_dict = {CONST.STOCK_K_LINE: '#BBBBBB', CONST.STOCK_D_LINE: '#F9D587', CONST.STOCK_J_LINE: '#FF00FF'}
#         df_stock_data[CONST.STOCK_K_LINE].plot(label=CONST.STOCK_K_LINE, color=color_dict[CONST.STOCK_K_LINE], rot=45)
#         df_stock_data[CONST.STOCK_D_LINE].plot(label=CONST.STOCK_D_LINE, color=color_dict[CONST.STOCK_D_LINE], rot=45)
#         df_stock_data[CONST.STOCK_J_LINE].plot(label=CONST.STOCK_J_LINE, color=color_dict[CONST.STOCK_J_LINE], rot=45)
#
#         plt.title(stock_code)
#         plt.legend()
#         plt.show()
#         print(df_stock_data)
#
#     return df_stock_data


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


# 只根据J线判断是否需要进行买卖,根据
def calJLineStragety(stock_code, df_stock_data):
    df_stock_kdj_data = Utils.CalKDJLine(stock_code, df_stock_data)

    # 1.计算基础数据
    df_j_data = df_stock_kdj_data[[CONST.STOCK_DATE_ENG, CONST.STOCK_CLOSE_PRICE_ENG, CONST.STOCK_J_LINE]]
    df_j_data[CONST.STOCK_20_MEAN_ENG] = df_stock_kdj_data[CONST.STOCK_CLOSE_PRICE_ENG].rolling(window=20).mean()

    # 计算J线的下降数据,shift向上一条数据移动,定义临时变量，存储数据
    CONST_TEMP_JSlope = 'JSlope'
    df_j_data[CONST_TEMP_JSlope] = df_j_data[CONST.STOCK_J_LINE] - df_j_data[CONST.STOCK_J_LINE].shift(axis=0)

    # 计算10日内的最大收盘价
    df_j_data['Max10'] = df_stock_kdj_data[CONST.STOCK_CLOSE_PRICE_ENG].rolling(window=10).max()

    # 2.买卖策略--买入
    # 2.1 J线小于10
    df_j_data['Lower10'] = df_j_data[CONST.STOCK_J_LINE] < Config.GetJlineParm(PARAM.J_LINE_BUY_THRESHOLD)
    # 2.2当天收盘价比十日内的高点下跌超过8%
    df_j_data['DownAM'] = df_j_data[CONST.STOCK_CLOSE_PRICE_ENG] < Config.GetJlineParm(PARAM.J_LINE_CLOSE_PRICE_DOWN) * df_j_data['Max10']
    # 2.3 J线呈减小趋势，且变化减缓,并在一定范围内
    df_j_data['JDown'] = df_j_data[CONST.STOCK_J_LINE] < df_j_data[CONST.STOCK_J_LINE].shift(axis=0)
    df_j_data['JDownSlower'] = (abs(df_j_data[CONST_TEMP_JSlope]) / abs(df_j_data[CONST_TEMP_JSlope].shift(axis=0)))<= Config.GetJlineParm(PARAM.J_LINE_BUY_SLOPE)
    #2.4,20日斜率大于
    df_j_data['Diff20'] = (df_j_data[CONST.STOCK_20_MEAN_ENG] / df_j_data[CONST.STOCK_20_MEAN_ENG].shift(
        axis=0)) >= Config.GetJlineParm(PARAM.J_LINE_CHANGE)

    # 买入点赋值
    df_j_data[CONST.STOCK_BUY_SECTION] = df_j_data['Lower10'] & df_j_data['DownAM'] & df_j_data['JDown'] & df_j_data['JDownSlower'] & df_j_data['Diff20']

    # 3.买卖策略--卖出策略
    # 3.1J线呈上升趋势，且变化减缓
    df_j_data['higher70'] = df_j_data[CONST.STOCK_J_LINE] > Config.GetJlineParm(PARAM.J_LINE_SELL_THRESHOLD)
    df_j_data['JUP'] = df_j_data[CONST.STOCK_J_LINE] > df_j_data[CONST.STOCK_J_LINE].shift(axis=0)
    df_j_data['JUPSlower'] = (abs(df_j_data[CONST_TEMP_JSlope]) / abs(df_j_data[CONST_TEMP_JSlope].shift(axis=0)))<= Config.GetJlineParm(PARAM.J_LINE_SELL_SLOPE)
    # 3.2 J值超过90，直接卖掉
    df_j_data['Jbigger90'] = df_j_data[CONST.STOCK_J_LINE] > Config.GetJlineParm(PARAM.J_LINE_SELL_THRESHOLD_90)
    #3.3 J线变小，且大于50，直接卖出
    df_j_data['Jbigger50AndSmaller'] = (df_j_data[CONST.STOCK_J_LINE] > Config.GetJlineParm(PARAM.J_LINE_SELL_THRESHOLD_50)) & (df_j_data[CONST.STOCK_J_LINE] <= df_j_data[CONST.STOCK_J_LINE].shift(1))


    # 卖出点赋值,满足J线变大，并且变缓，同时J大于90则直接卖出
    df_j_data[CONST.STOCK_SELL_SECTION] = (df_j_data['Jbigger90'] &df_j_data['JUP']  & df_j_data['JUPSlower']) | df_j_data['Jbigger50AndSmaller']

    #若满足J线变大，并且变缓，则在收益大于5%的情况下卖出，收益条件在买卖中进行计算。
    df_j_data[CONST.STOCK_SELL_IF_SECTION] = (df_j_data['higher70'] & df_j_data['JUP'] & df_j_data['JUPSlower'])

    #df_j_data.to_excel(CONST.STOCK_FOLDER_PATH + "\\JlineData\\" + stock_code + '.xlsx')
    #dict_trade_info = stockData2TradeInfo(stock_code,df_j_data)

    df_trade_data = stockData2TradeInfo(stock_code, df_j_data,Config)

    return df_trade_data

#计算上证综合指数的KDJ数据
# def CalSZKDJ(logger)
#     df_SZ_data = getCompositeIndexFileData(logger, CONST.SZ_INDEX_CODE, CONST.STOCK_DATA_ORIGNAL_FILE_NAME,
#                                               CONST.STOCK_FOLDER_PATH)
#     df_SZ_data = df_SZ_data[df_SZ_data[CONST.STOCK_DATE_ENG] >= begin_date]
