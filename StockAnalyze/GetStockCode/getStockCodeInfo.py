# 获取当前所有股票的基础信息
import tushare as ts
import pandas as pd
import EnumData.CONSTDEFINE as CONST
import Common.Utils as utils

# 获取所有股票编号，并存入文件
def getAllStockCodeFromWeb(logger):
    # 设置token
    token = 'ad82772c1b29371d27453121955c93099a9c48beeb048a4b2d89c8ec'
    ts.set_token(token)
    pro = ts.pro_api()
    # 查询当前所有正常上市交易的股票列表(获取基础信息数据，包括股票代码、名称、上市日期、退市日期等)
    df_stock_info = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    data = pd.DataFrame(df_stock_info)
    file_name = CONST.STOCK_FOLDER_PATH + "\\" + CONST.STOCK_CODE_FILE_NAME
    utils.mkdir(CONST.STOCK_FOLDER_PATH)
    data.to_excel(file_name, sheet_name='data')


def getAllStockCodeFromFile(logger):
    file_name = CONST.STOCK_FOLDER_PATH + "\\" + CONST.STOCK_CODE_FILE_NAME
    pd_stock = pd.read_excel(file_name)
    list_stock = pd_stock.values.tolist()

    list_stock_code = []
    for stock_info in list_stock:
        stock_code_temp = stock_info[1]
        #转换成函数需要的格式
        split_data = str(stock_code_temp).split(".")
        if len(split_data) >1:
            stock_code = split_data[1] +"." + str(split_data[0]).lower()
            list_stock_code.append(stock_code)
        else:
            logger.warn('stock code error {}'.format(stock_code_temp))

    return list_stock_code

def getAllStockCodeWithoutExFromFile(logger):
    file_name = CONST.STOCK_FOLDER_PATH + "\\" + CONST.STOCK_CODE_FILE_NAME
    pd_stock = pd.read_excel(file_name, usecols=[1])
    list_stock = pd_stock.values.tolist()

    list_stock_code = []
    for stock_info in list_stock:
        stock_code_temp = stock_info[0]
        #转换成函数需要的格式
        split_data = str(stock_code_temp).split(".")
        if len(split_data) >1:
            stock_code = split_data[0]
            list_stock_code.append(stock_code)
        else:
            logger.warn("stock code {} is wrong ,please check".format(stock_code_temp))
    return list_stock_code

if __name__ == "__main__":
    getAllStockCodeWithoutExFromFile()
