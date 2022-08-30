# -*- coding: utf-8 -*-
import sys
import time
import ntchat
try:
    import win32api
except ImportError:
    print("Error: this example require pywin32, use `pip install pywin32` install")
    sys.exit()

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)


# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]

    # 判断消息不是自己发的，并回复对方
    if from_wxid != self_wxid:
        wechat_instance.send_text(to_wxid=from_wxid, content=f"你发送的消息是: {data['msg']}")


def exit_application():
    ntchat.exit_()
    sys.exit()


def on_exit(sig, func=None):
    exit_application()


# 当关闭cmd窗口时
win32api.SetConsoleCtrlHandler(on_exit, True)

# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
# 当Ctrl+C结束程序时
except KeyboardInterrupt:
    exit_application()
