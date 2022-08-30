## 如何多开

新建多个ntchat.WeChat实例，然后调用open方法：
```python
import ntchat

# 多开3个微信
for i in range(3):
    wechat = ntchat.WeChat()
    wechat.open(smart=False)
```
更完善的多实例管理查看[fastapi_example例子](./fastapi_example)

## 如何监听输出所有的消息
```python
# 注册监听所有消息回调
@wechat.msg_register(ntchat.MT_ALL)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    print("########################")
    print(message)
```
完全例子查看[examples/msg_register_all.py](../examples/msg_register_all.py)

## 如何关闭NtChat的日志

`os.environ['NTCHAT_LOG'] = "ERROR"` 要在`import ntchat`前执行
```python
# -*- coding: utf-8 -*-
import os
import sys
import time
os.environ['NTCHAT_LOG'] = "ERROR"

import ntchat
```

## 如何正常的关闭Cmd窗口

先使用`pip install pywin32` 安装pywin32模块, 然后在代码中添加以下代码， 完整例子查看[examples/cmd_close_event.py](../examples/cmd_close_event.py)
```python
import sys
import ntchat
import win32api

def on_exit(sig, func=None):
    ntchat.exit_()
    sys.exit()


# 当关闭cmd窗口时
win32api.SetConsoleCtrlHandler(on_exit, True)
```


## pyinstaller打包exe
使用pyinstaller打包NtChat项目，需要添加`--collect-data=ntchat`选项

打包成单个exe程序
```bash
pyinstaller -F --collect-data=ntchat main.py
```

将所有的依赖文件打包到一个目录中
```bash
pyinstaller -y --collect-data=ntchat main.py
```
