import os
import pandas as pd
from StockAnalyze.EnumData import CONSTDEFINE as CONST



def getFoldersName(folder_path):
    folders = os.listdir(folder_path)
    folders_final = []
    for folder_name in folders:
        folder_inner_path = folder_path + '\\' + folder_name
        if os.path.isdir(folder_inner_path):
            folders_final.append(folder_inner_path)

    return folders_final


def combineSingleStockData(stock_code, path='../stockData'):
    file_path = path + "\\" + stock_code
    files = os.listdir(file_path)

    dfs = []
    for file in files:
        if file.endswith('.xlsx'):
            file_name = file_path + '\\' + file
            data = pd.read_excel(file_name)
            dfs.append(data)
            os.remove(file_name)
            print("删除文件%s成功" % file_name)

    df_stock = dfs[0]
    for i in range(1, len(dfs)):
        df_stock = df_stock.append(dfs[i], ignore_index=True)

    df_stock1 = df_stock.drop(labels='Unnamed: 0', axis=1)
    df_final = df_stock1.drop_duplicates(subset=[CONST.STOCK_DATE_ENG], keep='first')
    df_final.to_excel(file_path + "\\" + "data.xlsx", sheet_name='data')
    print("写入文件%s成功" % (file_path + "\\" + "data.xlsx"))
    return df_final


def readSingleStockData(logger, stock_code, file_name=CONST.STOCK_DATA_AFTER_FILE_NAME, path=CONST.STOCK_CODE_FOLDER_PATH):
    df_final = pd.DataFrame()
    file_path = path + "\\" + stock_code + "\\" + file_name
    if os.path.exists(file_path):
        logger.info("file = {} is existed,begin to read".format(file_path))
        df_stock = pd.read_excel(file_path)
        df_stock = df_stock.drop_duplicates(subset=[CONST.STOCK_DATE_ENG], keep='last')
        df_final = df_stock.copy()
        # 筛选2021年以来的数据
        df_final = df_final[df_final[CONST.STOCK_DATE_ENG] > CONST.DATA_BEGIN_DATA].copy()
        df_final[CONST.STOCK_CLOSE_PRICE_ENG] = df_final[CONST.STOCK_CLOSE_PRICE_ENG].apply(
            lambda x: round(x, 2))
        df_final[CONST.STOCK_OPEN_PRICE_ENG] = df_final[CONST.STOCK_OPEN_PRICE_ENG].apply(
            lambda x: round(x, 2))
        logger.debug("file = {} data：{}".format(file_path, df_final))
        return df_final
    else:
        logger.warn("file = {} is not existed".format(file_path))
        return df_final


# 获取上证指数、深证指数的原始数据
def getCompositeIndexFileData(logger, stock_code='SH.000001', file_name=CONST.STOCK_DATA_ORIGNAL_FILE_NAME,
                              path=CONST.STOCK_CODE_FOLDER_PATH):
    if stock_code not in ['SH.000001', 'SZ.399106']:
        logger.warn('CompositeIndex code is {} not right'.format(stock_code))
        df_final = pd.DataFrame()
        return df_final

    return readSingleStockData(logger, stock_code, file_name, path)


def ReadHS300StockCode(logger):
    file_name = CONST.STOCK_CODE_FOLDER_PATH + "\\" + CONST.STOCK_CODE_HS300_FILE_NAME
    pd_stock = pd.read_excel(file_name, usecols=[4, 7])

    list_stock = pd_stock.values.tolist()
    list_stock_res = []
    for stock_info in list_stock:
        stock_code = stock_info[0]
        stock_temp_home = stock_info[1]
        stock_home = 'SZ.'
        if stock_temp_home == 'SHH':
            stock_home = 'SH.'

        stock_code_info = stock_home + str(stock_code).zfill(6)
        list_stock_res.append(stock_code_info)
    return list_stock_res


if __name__ == '__main__':
    # ss = getFoldersName(path)
    # print(ss)
    combineSingleStockData('000001')
