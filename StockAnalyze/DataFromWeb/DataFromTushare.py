import tushare as ts


def setToken():
    # 设置token
    token = 'ad82772c1b29371d27453121955c93099a9c48beeb048a4b2d89c8ec'
    ts.set_token(token)

    pro = ts.pro_api()
    return pro

#获取沪股通成分
def getHSs():
    pro = setToken()
    data = pro.hs_const(hs_type='SH')
    print(data)

#获取深股通成分
def getSZs():
    pro = setToken()
    data = pro.hs_const(hs_type='SZ')
    print(data)



if __name__ =='__main__':
    # 获取沪股通成分
    getHSs()
    print('*******************')
    getSZs()
    #ts.get_industry_classified()
