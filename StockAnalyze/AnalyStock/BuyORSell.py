import datetime
import EnumData.ConfigParam as PARAM
import EnumData.CONSTDEFINE as CONST
from EnumData.EnumInfo import StockTrade
from DingTalk import SendMsg as DT
import Common.Logger
import Common.Utils as utils
import pandas as pd

logger = Common.Logger.log()


# 将股票信息中的买卖数据统一进行格式转换，方便统一格式
def stockData2TradeInfo(stock_code, df_stock_trade_info,configParam):
    # 第一次确认买卖点，将计算确认的买卖点筛选
    # df_trade_points = df_stock_trade_info[ (df_stock_trade_info[CONST.STOCK_SELL_IF_SECTION] == True) |
    #     (df_stock_trade_info[CONST.STOCK_BUY_SECTION] == True) | (df_stock_trade_info[CONST.STOCK_SELL_SECTION] == True)]

    # print(df_trade_points[[CONST.STOCK_DATE_ENG,CONST.STOCK_CLOSE_PRICE_ENG,CONST.STOCK_BUY_SECTION,CONST.STOCK_SELL_SECTION,CONST.STOCK_SELL_IF_SECTION]])
    # 将确认的买卖点进行去重，连续的买点或者卖点至保留时间老的一个
    # df_stock_trade_info.to_excel("E:\pythonCode\StockAnalyze\JlineData\\" + stock_code + '.xlsx')
    last_status = ""
    last_buy_price = 0
    dict_trade_info_total = {}
    for row, data in df_stock_trade_info.iterrows():
        temp_buy_status = data[CONST.STOCK_BUY_SECTION]
        temp_sell_status = data[CONST.STOCK_SELL_SECTION]
        temp_sell_if_status = data[CONST.STOCK_SELL_IF_SECTION]
        date = data[CONST.STOCK_DATE_ENG]

        if temp_buy_status == True and last_status != CONST.STOCK_BUY_SECTION:
            last_status = CONST.STOCK_BUY_SECTION
            last_buy_price = round(data[CONST.STOCK_CLOSE_PRICE_ENG], 2)
            dict_trade_info_total[date] = (StockTrade.Buy, last_buy_price, CONST.STOCK_BUY_COMMON)
            logger.info(
                'stockcode:{},buy info:[{},{}]'.format(stock_code, date, last_buy_price))

        # 卖出的规则，存多个卖出条件一致的情况
        if temp_sell_status == True and last_status != CONST.STOCK_SELL_SECTION:
            last_status = CONST.STOCK_SELL_SECTION
            dict_trade_info_total[date] = (
                StockTrade.Sell, round(data[CONST.STOCK_CLOSE_PRICE_ENG], 2), CONST.STOCK_SELL_COMMON)
            logger.info(
                'stockcode:{},certain sell info:[{},{}]'.format(stock_code, date, data[CONST.STOCK_CLOSE_PRICE_ENG]))


        # 在部分条件满足卖出的条件先，如果T日收盘价满足收益超过5%，则卖出
        elif temp_sell_if_status == True and last_status != CONST.STOCK_SELL_SECTION:
            temp_price = data[CONST.STOCK_CLOSE_PRICE_ENG]
            if last_buy_price > 0 and temp_price / last_buy_price >= configParam.GetJlineParm(PARAM.J_LINE_SELL_EARN_RATE):
                last_status = CONST.STOCK_SELL_SECTION
                dict_trade_info_total[date] = (
                    StockTrade.Sell, round(data[CONST.STOCK_CLOSE_PRICE_ENG], 2), CONST.STOCK_SELL_COMMON)
                logger.info(
                    'stockcode:{},sell info:[{},{}],earn rate is more than 5%'.format(stock_code, date, data[
                        CONST.STOCK_CLOSE_PRICE_ENG]))

        # 计算止损点，为卖出点
        if last_status == CONST.STOCK_BUY_SECTION:
            temp_price = data[CONST.STOCK_CLOSE_PRICE_ENG]
            if last_buy_price > 0 and (temp_price / last_buy_price <= configParam.GetJlineParm(PARAM.J_LINE_SELL_STOP_LOSSES)):
                last_status = CONST.STOCK_SELL_SECTION
                dict_trade_info_total[date] = (
                    StockTrade.Sell, data[CONST.STOCK_CLOSE_PRICE_ENG], CONST.STOCK_SELL_STOP_LOSS)
                logger.info(
                    'stockcode:{},sell info:[{},{}],stop losses'.format(stock_code, date, data[
                        CONST.STOCK_CLOSE_PRICE_ENG]))

    return dict_trade_info_total


def VerifyStrategyForDataFrame(stock_code, dict_stock_trade_info,list_buy_date = []):
    temp_idle_money = 10000
    temp_stock_money = 0
    last_buy_price = 0
    last_buy_date = ''

    currentTime = datetime.datetime.now().strftime("%Y-%m-%d")
    logger.info("sz datelist = {}".format(list_buy_date))
    list_temp = list(dict_stock_trade_info.keys())
    logger.info("buy or sell  datelist = {}".format(list_temp))
    logger.warn("common date:{}".format(set(list_temp).intersection(set(list_buy_date))))

    for key, value in dict_stock_trade_info.items():
        trade_flag = value[0]
        temp_date = key
        if (trade_flag == StockTrade.Buy) & (temp_date in list_buy_date):
            temp_stock_money = temp_idle_money
            last_buy_date = key
            last_buy_price = round(value[1], 2)
            temp_idle_money = 0

            if currentTime == last_buy_date:
                logger.warn("good time {} to buy {}".format(currentTime,stock_code))

        if trade_flag == StockTrade.Sell and last_buy_price > 0:
            close_money = round(value[1], 2)
            buy_date = key
            temp_idle_money = round(close_money / last_buy_price * temp_stock_money, 2)
            earn_rate = round((close_money / last_buy_price - 1) * 100, 2)
            logger.info(
                'stockcode:{},buy-[{},{},{}],sell-[{},{}，{},rate={}%]'.format(
                    stock_code, last_buy_date, last_buy_price, temp_stock_money,
                    buy_date, close_money, temp_idle_money, earn_rate))
            temp_stock_money = 0

    if len(dict_stock_trade_info) > 0:
        begin_time = sorted(dict_stock_trade_info.items())[0][0]
        end_time = sorted(dict_stock_trade_info.items())[-1][0]
        total_money = temp_stock_money + temp_idle_money
        ndays = utils.CalDaysBetweenDates(begin_time, end_time)
        printLog = ''
        if ndays > 0:
            earningRate = round((total_money - 10000) / ndays / 100 * 365, 2)
            print_log = 'from {} to {} ,stock-{} ,init money is 10000,current money :{},earning rate:{}%'.format(
                begin_time,
                end_time,
                stock_code,
                total_money,
                earningRate)
            #DT.send_news(logger, print_log)
        else:
            print_log = 'from {} to {},time is not enough'.format(begin_time, end_time)

        logger.warn(print_log)
        return total_money
    else:
        logger.warn('stockcode:{},data is not enough'.format(stock_code))
        return -1

