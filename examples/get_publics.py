# -*- coding: utf-8 -*-
import sys
import time
import ntchat


def version_tuple(v):
    return tuple(map(int, (v.split("."))))


if version_tuple(ntchat.__version__) < version_tuple('0.1.8'):
    print("error: ntchat version required 0.1.8, use `pip install -U ntchat` to upgrade")
    sys.exit()

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

# 等待登录
wechat.wait_login()

# 获取群列表并输出
rooms = wechat.get_publics()

print("公众号列表: ")
print(rooms)

# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
