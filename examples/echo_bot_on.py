# -*- coding: utf-8 -*-
import sys
import ntchat

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)


def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    room_wxid = data["room_wxid"]

    # 判断消息不是自己发的并且不是群消息时，回复对方
    if from_wxid != self_wxid and not room_wxid:
        wechat_instance.send_text(to_wxid=from_wxid, content=f"你发送的消息是: {data['msg']}")


# 监听接收文本消息
wechat.on(ntchat.MT_RECV_TEXT_MSG, on_recv_text_msg)

try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
