import akshare as ak
import pandas as pd
# fund_em_fund_name_df = ak.fund_em_fund_name()

# fund_em_fund_name_df.to_excel('fund.xlsx')
# print(fund_em_fund_name_df)
#

stock_zh_index_spot_df = ak.stock_zh_index_spot()
print(stock_zh_index_spot_df)
stock_zh_index_spot_df.to_excel('index.xlsx')
