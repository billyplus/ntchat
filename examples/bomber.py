# -*- coding: utf-8 -*-
import os
os.environ['NTCHAT_LOG'] = "ERROR"

import time
import ntchat

wechat = ntchat.WeChat()
wechat.open(smart=True)

print("正在登录微信")
wechat.wait_login()

peer_wxid = None

while True:
    contact_remark = input("请输入想发送的联系人备注: ")
    contacts = wechat.search_contacts(remark=contact_remark)
    if not contacts:
        print(f"没有搜索到备注是{contact_remark}的联系人")
    else:
        print(f"搜索到{len(contacts)}个联系人: ")
        print("0. 重新选择")
        for i, contact in enumerate(contacts):
            print(f"{i+1}. 昵称: {contact['nickname']}, 备注: {contact['remark']}")
        seq = int(input("输入上面编号进行选择: "))
        if seq != 0:
            peer_wxid = contacts[seq-1]["wxid"]
            break

content = input("请输入发送的内容: ")
number = int(input("请输入发送的次数: "))

for i in range(1, number+1):
    time.sleep(0.1)
    print("正在发送第%d遍" % i)
    wechat.send_text(to_wxid=peer_wxid, content=content)


ntchat.exit_()



