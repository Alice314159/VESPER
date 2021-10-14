# 股票买卖的定义
from enum import Enum


class StockTrade(Enum):
    NoTrade = 'nodeal'
    Buy = 'buy'
    Sell = 'sell'


class StockCodeType(Enum):
    StockTypeAll = 'AllCode'
    StockHS300 = 'HS300'
