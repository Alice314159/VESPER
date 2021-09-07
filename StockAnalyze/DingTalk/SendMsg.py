from dingtalkchatbot.chatbot import DingtalkChatbot


def send_news(logger,message):
    webHook = 'https://oapi.dingtalk.com/robot/send?access_token=3a6e6d90849314f2a96f6fd3981ed3883059ccb231309878e4cb5d2f8dd72fbc'
    xiaoDing = DingtalkChatbot(webHook)
    message = 'notify：' + message
    res = xiaoDing.send_text(msg=message,is_at_all=False)
    print(res)
    if res['errcode'] == 0:
        logger.info(message + ' response:' + str(res))
    else:
        logger.warn(message + ' response:' + str(res))

if __name__ == "__main__":
   send_news('notify：' + 'time to buy 2010-05-12')
