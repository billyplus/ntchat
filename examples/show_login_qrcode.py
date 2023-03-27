# -*- coding: utf-8 -*-
import sys
import time
import ntchat


def version_tuple(v):
    return tuple(map(int, (v.split("."))))


if version_tuple(ntchat.__version__) < version_tuple('0.1.15'):
    print("error: ntchat version required 0.1.15, use `pip install -U ntchat` to upgrade")
    sys.exit()

wechat = ntchat.WeChat()

# 打开一个新的微信，并显示二维码界面
wechat.open(smart=False, show_login_qrcode=True)
