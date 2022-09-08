from .conf import VERSION
from .core.wechat import WeChat
from .wc import wcprobe
from .const.notify_type import *
from .exception import *
from . import conf

__version__ = VERSION


def set_wechat_exe_path(wechat_exe_path=None, wechat_version=None):
    """
    自定义微信路径
    """
    conf.DEFAULT_WECHAT_EXE_PATH = wechat_exe_path
    conf.DEFAULT_WECHAT_VERSION = wechat_version


def get_install_wechat_version():
    return wcprobe.get_install_wechat_version()


def exit_():
    wcprobe.exit()
