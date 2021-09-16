import baostock as bs
import pandas as pd
import os
import datetime
from StockAnalyze.EnumData import CONSTDEFINE as CONST
from StockAnalyze.Common.Utils import mkdir



# 获取指数(综合指数、规模指数、一级行业指数、二级行业指数、策略指数、成长指数、价值指数、主题指数)K线数据
# 综合指数，例如：sh.000001 上证指数，sz.399106 深证综指 等；
# 规模指数，例如：sh.000016 上证50，sh.000300 沪深300，sh.000905 中证500，sz.399001 深证成指等；
# 一级行业指数，例如：sh.000037 上证医药，sz.399433 国证交运 等；
# 二级行业指数，例如：sh.000952 300地产，sz.399951 300银行 等；
# 策略指数，例如：sh.000050 50等权，sh.000982 500等权 等；
# 成长指数，例如：sz.399376 小盘成长 等；
# 价值指数，例如：sh.000029 180价值 等；
# 主题指数，例如：sh.000015 红利指数，sh.000063 上证周期 等；
def _getStockData(logger,stock_code = 'SH.000001'):

    folder_path = CONST.STOCK_FOLDER_PATH + "\\" + stock_code.upper()
    mkdir(folder_path)

    file_name = folder_path + "\\" + CONST.STOCK_DATA_ORIGNAL_FILE_NAME

    end_time = (datetime.date.today()).strftime("%Y-%m-%d")
    # 详细指标参数，参见“历史行情指标参数”章节；“周月线”参数与“日线”参数不同。
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg

    rs = bs.query_history_k_data_plus(stock_code,
                                      "date,code,open,high,low,close,preclose,volume,amount,pctChg",
                                    start_date='', end_date=end_time, frequency="d")

    if rs.error_code == '0':
        logger.info('query_history_k_data_plus {} success'.format(str(stock_code)))
    else:
        logger.warning('query_history_k_data_plus {},respond error_code:{}'.format(stock_code, rs.error_code))
        logger.warning('query_history_k_data_plus {},respond  error_msg:{}'.format(stock_code, rs.error_msg))

    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    # 结果集输出到csv文件
    result.to_excel(file_name, index=False)
    logger.info('save file {} finished'.format(file_name))



def GetCompositeIndex(logger):
    #综合指数
    composite_list = ['sh.000001','sz.399106']
    #规模指数
    size_index_list = ['sh.000016','sh.000300','sh.000905','sz.399001' ]

    list_total = composite_list + size_index_list

    bs.login()
    for stock_list in list_total:
        _getStockData(logger,stock_list)
    bs.logout()
# 获取指数(综合指数、规模指数、一级行业指数、二级行业指数、策略指数、成长指数、价值指数、主题指数)K线数据
# 综合指数，例如：sh.000001 上证指数，sz.399106 深证综指 等；
# 规模指数，例如：sh.000016 上证50，sh.000300 沪深300，sh.000905 中证500，sz.399001 深证成指等；
# 一级行业指数，例如：sh.000037 上证医药，sz.399433 国证交运 等；
# 二级行业指数，例如：sh.000952 300地产，sz.399951 300银行 等；
# 策略指数，例如：sh.000050 50等权，sh.000982 500等权 等；
# 成长指数，例如：sz.399376 小盘成长 等；
# 价值指数，例如：sh.000029 180价值 等；
# 主题指数，例如：sh.000015 红利指数，sh.000063 上证周期 等；


if __name__ == "__main__":
    GetCompositeIndex()
