import datetime
import StockAnalyze.EnumData.ConfigParam as PARAM
import StockAnalyze.EnumData.CONSTDEFINE as CONST
from StockAnalyze.EnumData.EnumInfo import StockTrade
from StockAnalyze.DingTalk import SendMsg as DT
import StockAnalyze.Common.Utils as utils
import pandas as pd


# 将股票信息中的买卖数据统一进行格式转换，方便统一格式
def stockData2TradeInfo(logger, stock_code, df_stock_trade_info, configParam):
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
            if last_buy_price > 0 and temp_price / last_buy_price >= configParam.GetJlineSellParm(
                    PARAM.J_LINE_SELL_EARN_RATE):
                last_status = CONST.STOCK_SELL_SECTION
                dict_trade_info_total[date] = (
                    StockTrade.Sell, round(data[CONST.STOCK_CLOSE_PRICE_ENG], 2), CONST.STOCK_SELL_COMMON)
                logger.info(
                    'stockcode:{},sell info:[{},{}],earn rate is more than 5%'.format(stock_code, date, data[
                        CONST.STOCK_CLOSE_PRICE_ENG]))

        # 计算止损点，为卖出点
        if last_status == CONST.STOCK_BUY_SECTION:
            temp_price = data[CONST.STOCK_CLOSE_PRICE_ENG]
            if last_buy_price > 0 and (
                    temp_price / last_buy_price <= configParam.GetJlineSellParm(PARAM.J_LINE_SELL_STOP_LOSSES)):
                last_status = CONST.STOCK_SELL_SECTION
                dict_trade_info_total[date] = (
                    StockTrade.Sell, data[CONST.STOCK_CLOSE_PRICE_ENG], CONST.STOCK_SELL_STOP_LOSS)
                logger.info(
                    'stockcode:{},sell info:[{},{}],stop losses'.format(stock_code, date, data[
                        CONST.STOCK_CLOSE_PRICE_ENG]))

    return dict_trade_info_total

#统一输出股票信息数据
def printTradeInfo(logger, stock_code, date, trade_flag):
    if trade_flag == StockTrade.Buy:
        logger.info('date {} buy stock {}'.format(date, stock_code))
    elif trade_flag == StockTrade.Sell:
        logger.info('date {} sell stock {}'.format(date, stock_code))
    else:
        logger.info('date {} no deal stock {}'.format(date, stock_code))

#初始一万，验证策略
def VerifyStrategyForDataFrame(logger, stock_code, dict_stock_trade_info):
    temp_idle_money = 10000
    temp_stock_money = 0
    last_buy_price = 0
    last_buy_date = ''

    currentTime = datetime.datetime.now().strftime("%Y-%m-%d")
    for key, value in dict_stock_trade_info.items():
        trade_flag = value[0]
        temp_date = key

        printTradeInfo(logger, stock_code, temp_date, trade_flag)

        if (trade_flag == StockTrade.Buy):
            temp_stock_money = temp_idle_money
            last_buy_date = key
            last_buy_price = round(value[1], 2)
            temp_idle_money = 0

            if currentTime == last_buy_date:
                logger.warn("good time {} to buy {}".format(currentTime, stock_code))

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
            # DT.send_news(logger, print_log)
        else:
            print_log = 'from {} to {},time is not enough'.format(begin_time, end_time)

        logger.warn(print_log)
        return total_money
    else:
        logger.warn('stockcode:{},data is not enough'.format(stock_code))
        return -1
