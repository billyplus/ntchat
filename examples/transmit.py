# -*- coding: utf-8 -*-
from email import message
from email.mime import image
import sys
import os.path
import time
import ntchat
import re

# 聊天记录通知
MT_RECV_CHAT_RECORDS_MSG = 11061

wechat = ntchat.WeChat()

# 要监听的wxids，可以通过获取contact接口获取wxid，也可以开启后从debug信息中看出来
from_wxids = ["xxxxx", "xxxxxx"]
# 要转发的目标群
target_wxids = ["xxxxxxxx@chatroom"]
# 检查文件等待时长，单位s
wait_limit = 10

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)


@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]

    # 判断消息不是自己发的，且来自于想要转发的用户列表，并发给target用户
    if from_wxid != self_wxid and from_wxid in from_wxids:
        for target_wxid in target_wxids:
            wechat_instance.send_text(to_wxid=target_wxid,
                                  content=f"{data['msg']}")


# 等待file_path的文件被下载,超过等待次数后返回true
def wait_for_file(file_path) -> bool:
    cnt = 0
    while not os.path.exists(file_path):
        time.sleep(1)
        cnt = cnt + 1
        if cnt > wait_limit:
            print(
                f"wait for {wait_limit} second, but file cannot be downloaded, forgive."
            )
            return False
    return True


@wechat.msg_register(ntchat.MT_RECV_IMAGE_MSG)
def on_recv_img_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    img_path = data["image"]
    # img_path = "D:\\a.png"
    self_wxid = wechat_instance.get_login_info()["wxid"]

    # 判断消息不是自己发的，且来自于想要转发的用户列表，并发给target用户
    if from_wxid != self_wxid and from_wxid in from_wxids:
        if wait_for_file(file_path=img_path):
            for target_wxid in target_wxids:
                wechat_instance.send_image(to_wxid=target_wxid, file_path=img_path)


@wechat.msg_register(ntchat.MT_RECV_FILE_MSG)
def on_recv_img_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    file_path = data["file"]
    self_wxid = wechat_instance.get_login_info()["wxid"]

    # 判断消息不是自己发的，且来自于想要转发的用户列表，并发给target用户
    if from_wxid != self_wxid and from_wxid in from_wxids:
        if wait_for_file(file_path=file_path):
            for target_wxid in target_wxids:
                wechat_instance.send_file(to_wxid=target_wxid, file_path=file_path)


def update_wxid_in_xml(xml, from_wxid, target_wxid):
    patten = re.compile(from_wxid)
    return patten.sub(target_wxid, xml)


@wechat.msg_register(MT_RECV_CHAT_RECORDS_MSG)
def on_recv_chat_record_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    raw_msg = data["raw_msg"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    xml = update_wxid_in_xml(raw_msg, from_wxid, self_wxid)
    # 判断消息不是自己发的，且来自于想要转发的用户列表，并发给target用户
    if from_wxid != self_wxid and from_wxid in from_wxids:
        for target_wxid in target_wxids:
            wechat_instance.send_xml(to_wxid=target_wxid, xml=xml)


@wechat.msg_register(ntchat.MT_RECV_LINK_MSG)
def on_recv_link_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    raw_msg = data["raw_msg"]
    # xml中的fromusername改成自己的wxid 再发
    self_wxid = wechat_instance.get_login_info()["wxid"]
    xml = update_wxid_in_xml(raw_msg, from_wxid, self_wxid)
    # 判断消息不是自己发的，且来自于想要转发的用户列表，并发给target用户
    if from_wxid != self_wxid and from_wxid in from_wxids:
        for target_wxid in target_wxids:
            wechat_instance.send_xml(to_wxid=target_wxid, xml=xml)


try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()