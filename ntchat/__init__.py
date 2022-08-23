from .conf import VERSION
from .core.wechat import WeChat
from .wc import wcprobe
from .const.wx_type import *
from .exception import *

__version__ = VERSION

exit_ = wcprobe.exit
