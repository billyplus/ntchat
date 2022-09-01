# -*- coding: utf-8 -*-
import ntchat
import requests
from typing import Dict, Union
from ntchat.utils.singleton import Singleton
from utils import generate_guid
from exception import ClientNotExists


class ClientWeChat(ntchat.WeChat):
    guid: str = ""


class ClientManager(metaclass=Singleton):
    __client_map: Dict[str, ntchat.WeChat] = {}
    callback_url: str = ""

    def new_guid(self):
        """
        生成新的guid
        """
        while True:
            guid = generate_guid("wechat")
            if guid not in self.__client_map:
                return guid

    def create_client(self):
        guid = self.new_guid()
        wechat = ClientWeChat()
        wechat.guid = guid
        self.__client_map[guid] = wechat

        # 注册回调
        wechat.on(ntchat.MT_ALL, self.__on_callback)
        wechat.on(ntchat.MT_RECV_WECHAT_QUIT_MSG, self.__on_quit_callback)
        return guid

    def get_client(self, guid: str) -> Union[None, ntchat.WeChat]:
        client = self.__client_map.get(guid, None)
        if client is None:
            raise ClientNotExists(guid)
        return client

    def remove_client(self, guid):
        if guid in self.__client_map:
            del self.__client_map[guid]

    def __on_callback(self, wechat, message):
        if not self.callback_url:
            return

        client_message = {
            "guid": wechat.guid,
            "message": message
        }
        requests.post(self.callback_url, json=client_message)

    def __on_quit_callback(self, wechat):
        self.__on_callback(wechat, {})
