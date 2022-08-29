## NtChat fastapi完整示例

通过fastapi的swagger在线文档可以很方便的管理NtChat接口
![vfazT0.jpg](https://s1.ax1x.com/2022/08/29/vfazT0.jpg)

## 安装依赖
```bash
pip install -r requirements.txt
```

## 运行例子
```bash
python main.py
```

## 访问api在线文档
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


## 如何调用 

可以使用requests库去访问接口

/client/create 是创建一个微信的实例，返回guid，标识实例的id, 后面所有的接口都要用到

/client/open   是打开并管理上微信实例