## WeChatVersionNotMatchError异常
如果出现`ntchat.exception.WeChatVersionNotMatchError`异常, 请确认是否安装github上指定的微信版本，如果确认已经安装，还是报错，可以在代码中添加以下代码，跳过微信版本检测
```python
import ntchat
ntchat.set_wechat_exe_path(wechat_version='3.6.0.18') 
```
如果还是无法正常使用，但确认已经安装过了3.6.0.18版本可以如下设置
```python
import ntchat

# wechat_exe_path设置成自己3.6.0.18版本的微信的安装路径
ntchat.set_wechat_exe_path(
    wechat_exe_path=r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe", 
    wechat_version="3.6.0.18")
```

也可以使用注册表修复这个问题，将下面内容保存成WeChatFix.reg, 并双击运行, 如果安装时有修改安装路径，需要修改下面的InstallPath为自己设定的安装路径
```editorconfig
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\SOFTWARE\Tencent\WeChat]
"Version"=dword:63060012
"InstallPath"="C:\Program Files (x86)\Tencent\WeChat"
```


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

打包fastapi_example示例，需要添加`--paths=. --collect-data=ntchat`
```bash
pyinstaller -F --paths=. --collect-data=ntchat main.py
```