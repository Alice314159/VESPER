
from Common import Logger
from StockAnalyze.Common import ReadConfig
from StockAnalyze.EnumData import ConfigParam as Param
from GetStockCode import getStockCodeInfo
from AnalyStock import KDJStragety
logger = Logger.log()
Config = ReadConfig.ReadConfig()

def modifyBuyParam():
    # J线买入策略的阈值，要小于10
    for J_LINE_SMALLER_THRESHOLD in range(10,30,1):
        Config.SetJlineBuyParam(Param.J_LINE_SMALLER_THRESHOLD,str(J_LINE_SMALLER_THRESHOLD))

        # J线变小，且斜率变化小于0.8
        for J_LINE_BUY_SLOPE  in range(0,10,1):
            Config.SetJlineBuyParam(str(Param.J_LINE_BUY_SLOPE).upper(), str(J_LINE_BUY_SLOPE/10))

            # 比十日最高点下跌3%（取值范围）
            for J_LINE_CLOSE_PRICE_DOWN in range(90,99,1):
                Config.SetJlineBuyParam(Param.J_LINE_CLOSE_PRICE_DOWN, str(J_LINE_CLOSE_PRICE_DOWN/100))

                # 上证综合指数J线要低于15才能买入(取值范围10-50)
                for SZ_J_LINE in range(10, 50, 1):
                    Config.SetJlineBuyParam(Param.SZ_J_LINE, str(SZ_J_LINE))
                    print('buy flag finished')
                    modifySellParam()



def runLog():
    stock_code_list1 = getStockCodeInfo.getAllStockCodeFromFile(logger)
    stock_code_list = stock_code_list1[0:1]
    KDJStragety.KDJStragetyStockEarnMoney(logger,stock_code_list)

def modifySellParam():
    # J_LINE_BIGGER_THRESHOLD = 70
    for J_LINE_BIGGER_THRESHOLD in range(70,100,1):
        Config.SetJlineSellParam(Param.J_LINE_BIGGER_THRESHOLD, str(J_LINE_BIGGER_THRESHOLD))
        # #J线变大，且斜率变化小于0.9
        for J_LINE_SELL_SLOPE in range(7,10,1):
            Config.SetJlineSellParam(Param.J_LINE_SELL_SLOPE, str(J_LINE_SELL_SLOPE/10))

            # # 收盘价收益大于5%，则卖出
            for J_LINE_SELL_EARN_RATE in range(100,110,1):
                Config.SetJlineSellParam(Param.J_LINE_SELL_EARN_RATE, str(J_LINE_SELL_EARN_RATE / 100))

                # 在J线大于90的基础上，同时满足其他条件
                for J_LINE_SELL_THRESHOLD_90 in range(80,110,1):
                    Config.SetJlineSellParam(Param.J_LINE_SELL_THRESHOLD_90, str(J_LINE_SELL_THRESHOLD_90))

                    # # J线变小，且大于50，直接卖出
                    for J_LINE_SELL_THRESHOLD_50 in range(40,70):
                        Config.SetJlineSellParam(Param.J_LINE_SELL_THRESHOLD_50, str(J_LINE_SELL_THRESHOLD_50))

                        # # 止损参数，如果当前的收益低于0.95，则直接卖出
                        for J_LINE_SELL_STOP_LOSSES in range(80, 95,1):
                            Config.SetJlineSellParam(Param.J_LINE_SELL_STOP_LOSSES, str(J_LINE_SELL_STOP_LOSSES/100))
                            print('sell flag finished')
                            runLog()



if __name__ == '__main__':
   modifyBuyParam()
