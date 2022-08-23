from .conf import VERSION
from .core.wechat import WeChat
from .wc import wcprobe

__version__ = VERSION

exit_ = wcprobe.exit
