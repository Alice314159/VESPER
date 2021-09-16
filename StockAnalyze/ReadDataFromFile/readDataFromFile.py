import os
import pandas as pd
import matplotlib.pyplot as plt
from StockAnalyze.EnumData import CONSTDEFINE as CONST
import time


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


def readSingleStockData(logger,stock_code, file_name = CONST.STOCK_DATA_AFTER_FILE_NAME,path=CONST.STOCK_FOLDER_PATH):
    df_final= pd.DataFrame()
    file_path = path + "\\" + stock_code +"\\" + file_name
    if os.path.exists(file_path):
        logger.info("file = {} is existed,begin to read".format(file_path))
        df_stock = pd.read_excel(file_path)
        df_final = df_stock.drop_duplicates(subset=[CONST.STOCK_DATE_ENG], keep='last')

        #筛选2021年以来的数据
        df_final = df_final[df_final[CONST.STOCK_DATE_ENG] >CONST.DATA_BEGIN_DATA ]
        logger.debug("file = {} data：{}".format(file_path,df_final))
        return df_final
    else:
        logger.warn("file = {} is not existed".format(file_path))
        return df_final

#获取上证指数、深证指数的原始数据
def getCompositeIndexFileData(logger,stock_code='SH.000001', file_name = CONST.STOCK_DATA_ORIGNAL_FILE_NAME,path=CONST.STOCK_FOLDER_PATH):
    if stock_code not in ['SH.000001','SZ.399106']:
        logger.warn('CompositeIndex code is {} not right'.format(stock_code))
        df_final = pd.DataFrame()
        return df_final

    return readSingleStockData(logger,stock_code,file_name,path)


if __name__ == '__main__':
    # ss = getFoldersName(path)
    # print(ss)
    combineSingleStockData('000001')
