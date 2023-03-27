# -*- coding: utf-8 -*-
import sys
import time
import ntchat

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

# 等待登录
wechat.wait_login()

'''
test,你好{$@},你好{$@}.早上好

发送内容中{$@}占位符说明：

文本消息的content的内容中设置占位字符串 {$@},这些字符的位置就是最终的@符号所在的位置
假设这两个被@的微信号的群昵称分别为aa,bb
则实际发送的内容为 "test,你好@ aa,你好@ bb.早上好"(占位符被替换了)

占位字符串的数量必须和at_list中的微信数量相等.
'''

# 下面是@两个人的发送例子，room_wxid, at_list需要自己替换
wechat.send_room_at_msg(to_wxid="xxxxxx@chatroom",
                        content="测试, 你好{$@},你好{$@}",
                        at_list=['wxid_xxxxxxxx', 'wxid_xxxxxxxxx'])


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()




