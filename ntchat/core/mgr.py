import json
import os.path
from ntchat.wc import wcprobe
from ntchat.utils.xdg import get_helper_file
from ntchat.exception import WeChatVersionNotMatchError, WeChatBindError
from ntchat.utils.singleton import Singleton
from ntchat.const import wx_type
from ntchat.utils.logger import get_logger

log = get_logger("WeChatManager")


class WeChatMgr(metaclass=Singleton):
    __instance_list = []
    __instance_map = {}

    def __init__(self, wechat_exe_path=None, wechat_version=None):
        self.set_wechat_exe_path(wechat_exe_path, wechat_version)

        # init callbacks
        wcprobe.init_callback(self.__on_accept, self.__on_recv, self.__on_close)

    def set_wechat_exe_path(self, wechat_exe_path=None, wechat_version=None):
        exe_path = ''
        if wechat_exe_path is not None:
            exe_path = wechat_exe_path

        if wechat_version is None:
            version = wcprobe.get_install_wechat_version()
        else:
            version = wechat_version

        helper_file = get_helper_file(version)
        if not os.path.exists(helper_file):
            raise WeChatVersionNotMatchError()

        log.info("initialize wechat, version: %s", version)

        # init env
        wcprobe.init_env(helper_file, exe_path)

    def append_instance(self, instance):
        log.debug("new wechat instance")
        self.__instance_list.append(instance)

    def __bind_wechat(self, client_id, pid):
        bind_instance = None
        if client_id not in self.__instance_map:
            for instance in self.__instance_list:
                if instance.pid == pid:
                    instance.client_id = client_id
                    instance.status = True
                    self.__instance_map[client_id] = instance
                    bind_instance = instance
                    break
        if bind_instance is None:
            raise WeChatBindError()
        self.__instance_list.remove(bind_instance)

    def __on_accept(self, client_id):
        log.debug("accept client_id: %d", client_id)

    def __on_recv(self, client_id, data):
        message = json.loads(data)
        if message["type"] == wx_type.MT_READY_MSG:
            self.__bind_wechat(client_id, message["data"]["pid"])
        else:
            self.__instance_map[client_id].on_recv(message)

    def __on_close(self, client_id):
        log.debug("close client_id: %d", client_id)
        if client_id in self.__instance_map:
            self.__instance_map[client_id].login_status = False
            self.__instance_map[client_id].status = False
