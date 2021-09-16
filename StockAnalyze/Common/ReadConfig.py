from configparser import ConfigParser
import os

BuyParam = "JlineBuyParm"
SellParam = "JlineSellParm"


class ConfigParserUper(ConfigParser):

    def optionxform(self, optionstr):
        return optionstr


class ReadConfig:
    """定义一个读取配置文件的类"""

    def __init__(self, filepath=None):
        if filepath:
            configpath = filepath
            self.configpath = configpath
        else:
            root_dir = os.path.dirname(os.path.abspath('.'))
            configpath = os.path.join(root_dir, "config.ini")
            self.configpath = configpath

        self.cf = ConfigParserUper(comment_prefixes='/', allow_no_value=True)
        self.cf.read(configpath, encoding='UTF-8')

    def GetJlineBuyParm(self, param):
        value = float(self.cf.get(BuyParam, param))
        return value

    def GetJlineSellParm(self, param):
        value = float(self.cf.get(SellParam, param))
        return value

    def GetJlineBuyItems(self):
        value = self.cf.items(BuyParam)
        return value

    def GetJlineSellItems(self):
        value = self.cf.items(SellParam)
        return value

    def GetJlineItems(self):
        value0 = self.cf.items(BuyParam)
        value1 = self.cf.items(SellParam)
        value = value0 + value1
        return value

    def SetJlineBuyParam(self, param, data):
        self.cf.set(BuyParam, param, data)
        self.cf.write(open(self.configpath, "w", encoding="utf-8"))

    def SetJlineSellParam(self, param, data):
        self.cf.set(SellParam, param, data)
        self.cf.write(open(self.configpath, "w", encoding="utf-8"))


if __name__ == '__main__':
    test = ReadConfig("E:\pythonCode\StockAnalyze\config.ini")
    t = test.GetJlineItems()
    print(t)
