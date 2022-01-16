import logging
import time
def log():
    #创建logger，如果参数为空则返回root logger
    logger= logging.getLogger()
    logger.setLevel(logging.INFO) #设置logger日志等级

    #这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
    if not logger.handlers:
        #创建handler
        file_name = time.strftime("%Y-%m-%d-%H", time.localtime()) + '.log'

        fh= logging.FileHandler('../log/'+ file_name,encoding="utf-8")
        ch= logging.StreamHandler()

        #设置输出日志格式
        formatter= logging.Formatter(
            fmt="%(asctime)s %(process)d %(name)s %(filename)s %(lineno)d  %(message)s",
            datefmt="%Y-%m-%d %X"
            )

        #为handler指定输出格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        #为logger添加的日志处理器
        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger#直接返回logger
    else:
        print('logger init failed')
