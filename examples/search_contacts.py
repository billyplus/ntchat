# -*- coding: utf-8 -*-
import sys
import time
import ntchat


def version_tuple(v):
    return tuple(map(int, (v.split("."))))


if version_tuple(ntchat.__version__) < version_tuple('0.1.7'):
    print("error: ntchat version required 0.1.7, use `pip install -U ntchat` to upgrade")
    sys.exit()

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

# 等待登录
wechat.wait_login()

# 根据wxid模糊查询查询联系人
contacts = wechat.search_contacts(wxid="wxid_")
print(contacts)

# 根据微信号模糊查询联系人
# contacts = wechat.search_contacts(account="")


# 根据昵称模糊查询联系人, 如昵称包含`小`的联系人
contacts = wechat.search_contacts(nickname="小")
print(contacts)

# 根据备注查询联系人
contacts = wechat.search_contacts(remark="备注")
print(contacts)


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
