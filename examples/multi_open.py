# -*- coding: utf-8 -*-
import sys
import ntchat

# 多开3个微信
for i in range(3):
    wechat = ntchat.WeChat()
    wechat.open(smart=False)

