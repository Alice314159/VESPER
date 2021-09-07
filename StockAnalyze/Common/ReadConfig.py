import configparser
import os


class ReadConfig:
    """定义一个读取配置文件的类"""
    def __init__(self, filepath=None):
        if filepath:
            print(filepath)
            configpath = filepath
        else:
            root_dir = os.path.dirname(os.path.abspath('.'))
            print(filepath)
            configpath = os.path.join(root_dir, "config.ini")
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath,encoding='UTF-8')

    def get_db(self, param):
        value = self.cf.get("mysql", param)
        return value

    def GetJlineParm(self, param):
        value = float(self.cf.get("JlineParm", param))
        return value

    def GetJlineItems(self):
        value = self.cf.items("JlineParm")
        return value


if __name__ == '__main__':
    test = ReadConfig("E:\pythonCode\StockAnalyze\config.ini")
    t = test.GetJlineItems()
    print(t)
