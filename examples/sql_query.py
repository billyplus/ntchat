# -*- coding: utf-8 -*-
import sys
import time
import ntchat

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

# 等待登录
wechat.wait_login()

# 获取群列表并输出
room_wxid = wechat.get_rooms()[0]["wxid"]


def get_room_name(wechat: ntchat.WeChat, room_wxid: str):
    sql = f"select nickname from contact where username='{room_wxid}'"
    result = wechat.sql_query(sql, 1)["result"]
    if result:
        return result[0][0]
    return None


print("群名是: ", get_room_name(wechat, room_wxid))

# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
