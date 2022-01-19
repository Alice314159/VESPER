import tushare as ts

def getBasicInfo():
    # 设置token
    token = 'ad82772c1b29371d27453121955c93099a9c48beeb048a4b2d89c8ec'
    ts.set_token(token)

    ts.get_stock_basics()
    return

def getReport():
    # 设置token
    token = 'ad82772c1b29371d27453121955c93099a9c48beeb048a4b2d89c8ec'
    ts.set_token(token)

    # code, 代码
    # name, 名称
    # esp, 每股收益
    # eps_yoy, 每股收益同比( %)
    # bvps, 每股净资产
    # roe, 净资产收益率( %)
    # epcf, 每股现金流量(元)
    # net_profits, 净利润(万元)
    # profits_yoy, 净利润同比( %)
    # distrib, 分配方案
    # report_date, 发布日期
    data = ts.get_report_data(2021,3)

    print(data)



if __name__ =='__main__':
    # 获取沪股通成分
    getReport()
    print('*******************')

    #ts.get_industry_classified()
