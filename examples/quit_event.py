# -*- coding: utf-8 -*-
import sys
import time
import ntchat


def version_tuple(v):
    return tuple(map(int, (v.split("."))))


if version_tuple(ntchat.__version__) < version_tuple('0.1.4'):
    print("error: ntchat version required 0.1.4, use `pip install -U ntchat` to upgrade")
    sys.exit()

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

global_quit_flag = False


# 微信进程关闭通知
@wechat.msg_register(ntchat.MT_RECV_WECHAT_QUIT_MSG)
def on_wechat_quit(wechat_instace):
    print("###################")
    global global_quit_flag
    global_quit_flag = True


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
while True:
    if global_quit_flag:
        break
    time.sleep(0.5)

ntchat.exit_()
sys.exit()
