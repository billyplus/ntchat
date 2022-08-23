# -*- coding: utf-8 -*-
import sys
import ntchat

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=False)

# 等待登录
wechat.wait_login()

# 获取群列表并输出
rooms = wechat.get_rooms()

print("群列表: ")
print(rooms)


try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
