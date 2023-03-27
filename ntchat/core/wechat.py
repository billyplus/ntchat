import pyee
import json
from ntchat.core.mgr import WeChatMgr
from ntchat.const import notify_type, send_type
from threading import Event
from ntchat.wc import wcprobe
from ntchat.utils import generate_guid
from ntchat.utils import logger
from ntchat.exception import WeChatNotLoginError
from functools import wraps
from typing import (
    List,
    Union,
    Tuple
)

log = logger.get_logger("WeChatInstance")


class ReqData:
    __response_message = None
    msg_type: int = 0
    request_data = None

    def __init__(self, msg_type, data):
        self.msg_type = msg_type
        self.request_data = data
        self.__wait_event = Event()

    def wait_response(self, timeout=None):
        self.__wait_event.wait(timeout)
        return self.get_response_data()

    def on_response(self, message):
        self.__response_message = message
        self.__wait_event.set()

    def get_response_data(self):
        if self.__response_message is None:
            return None
        return self.__response_message["data"]


class RaiseExceptionFunc:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            self.func(*args, **kwargs)
        except Exception as e:
            log.error('callback error, in function `%s`, error: %s', self.func.__name__, e)


class WeChat:
    client_id: int = 0
    pid: int = 0
    status: bool = False
    login_status: bool = False

    def __init__(self):
        WeChatMgr().append_instance(self)
        self.__wait_login_event = Event()
        self.__req_data_cache = {}
        self.event_emitter = pyee.EventEmitter()
        self.__login_info = {}

    def on(self, msg_type, f):
        if not (isinstance(msg_type, list) or isinstance(msg_type, tuple)):
            msg_type = [msg_type]
        for event in msg_type:
            self.event_emitter.on(str(event), RaiseExceptionFunc(f))

    def msg_register(self, msg_type: Union[int, List[int], Tuple[int]]):
        def wrapper(f):
            wraps(f)
            self.on(msg_type, f)
            return f
        return wrapper

    def on_close(self):
        self.login_status = False
        self.status = False
        self.event_emitter.emit(str(notify_type.MT_RECV_WECHAT_QUIT_MSG), self)

        message = {
            "type": notify_type.MT_RECV_WECHAT_QUIT_MSG,
            "data": {}
        }
        self.event_emitter.emit(str(notify_type.MT_ALL), self, message)

    def bind_client_id(self, client_id):
        self.status = True
        self.client_id = client_id

    def on_recv(self, message):
        log.debug("on recv message: %s", message)
        msg_type = message["type"]
        extend = message.get("extend", None)
        if msg_type == notify_type.MT_USER_LOGIN_MSG:
            self.login_status = True
            self.__wait_login_event.set()
            self.__login_info = message.get("data", {})
            log.info("login success, wxid: %s, nickname: %s", self.__login_info["wxid"], self.__login_info["nickname"])
        elif msg_type == notify_type.MT_USER_LOGOUT_MSG:
            self.login_status = False
            log.info("logout, pid: %d", self.pid)

        if extend is not None and extend in self.__req_data_cache:
            req_data = self.__req_data_cache[extend]
            req_data.on_response(message)
            del self.__req_data_cache[extend]
        else:
            self.event_emitter.emit(str(msg_type), self, message)
            self.event_emitter.emit(str(notify_type.MT_ALL), self, message)

    def wait_login(self, timeout=None):
        log.info("wait login...")
        self.__wait_login_event.wait(timeout)

    def open(self, smart=False, show_login_qrcode=False):
        if show_login_qrcode:
            wcprobe.show_login_qrcode()

        self.pid = wcprobe.open(smart)
        log.info("open wechat pid: %d", self.pid)
        return self.pid != 0

    def attach(self, pid: int):
        self.pid = pid
        log.info("attach wechat pid: %d", self.pid)
        return wcprobe.attach(pid)

    def detach(self):
        log.info("detach wechat pid: %d", self.pid)
        return wcprobe.detach(self.pid)

    def __send(self, msg_type, data=None, extend=None):
        if not self.login_status:
            raise WeChatNotLoginError()

        message = {
            'type': msg_type,
            'data': {} if data is None else data,
        }
        if extend is not None:
            message["extend"] = extend
        message_json = json.dumps(message)
        log.debug("communicate wechat pid: %d,  data: %s", self.pid, message)
        return wcprobe.send(self.client_id, message_json)

    def __send_sync(self, msg_type, data=None, timeout=10):
        req_data = ReqData(msg_type, data)
        extend = self.__new_extend()
        self.__req_data_cache[extend] = req_data
        self.__send(msg_type, data, extend)
        return req_data.wait_response(timeout)

    def __new_extend(self):
        while True:
            guid = generate_guid("req")
            if guid not in self.__req_data_cache:
                return guid

    def __repr__(self):
        return f"WeChatInstance(pid: {self.pid}, client_id: {self.client_id})"

    def sql_query(self, sql: str, db: int):
        """
        数据库查询
        """
        data = {
            "sql": sql,
            "db": db
        }
        return self.__send_sync(send_type.MT_SQL_QUERY_MSG, data)

    def get_login_info(self):
        """
        获取登录信息
        """
        return self.__login_info

    def get_self_info(self):
        """
        获取自己个人信息跟登录信息类似
        """
        return self.__send_sync(send_type.MT_GET_SELF_MSG)

    def get_contacts(self):
        """
        获取联系人列表
        """
        return self.__send_sync(send_type.MT_GET_CONTACTS_MSG)

    def get_publics(self):
        """
        获取关注公众号列表
        """
        return self.__send_sync(send_type.MT_GET_PUBLICS_MSG)

    def get_contact_detail(self, wxid):
        """
        获取联系人详细信息
        """
        data = {
            "wxid": wxid
        }
        return self.__send_sync(send_type.MT_GET_CONTACT_DETAIL_MSG, data)

    def search_contacts(self,
                        wxid: Union[None, str] = None,
                        account: Union[None, str] = None,
                        nickname: Union[None, str] = None,
                        remark: Union[None, str] = None,
                        fuzzy_search: bool = True):
        """
        根据wxid、微信号、昵称和备注模糊搜索联系人
        """
        conds = {}
        if wxid:
            conds["username"] = wxid
        if account:
            conds["alias"] = account
        if nickname:
            conds["nickname"] = nickname
        if remark:
            conds["remark"] = remark
        if not conds:
            return []

        cond_pairs = []
        tag = '%' if fuzzy_search else ''
        for k, v in conds.items():
            cond_pairs.append(f"{k} like '{tag}{v}{tag}'")

        cond_str = " or ".join(cond_pairs)
        sql = f"select username from contact where {cond_str}"
        message = self.sql_query(sql, 1)
        if not message:
            return []

        result = message["result"]
        if not result:
            return []

        contacts = []
        for wxid_list in result:
            if len(wxid_list) > 0:
                wxid = wxid_list[0]
                contact = self.get_contact_detail(wxid)
                contacts.append(contact)
        return contacts

    def get_rooms(self):
        """
        获取群列表
        """
        return self.__send_sync(send_type.MT_GET_ROOMS_MSG)

    def get_room_detail(self, room_wxid):
        """
        获取指定群详细信息
        """
        data = {
            "room_wxid": room_wxid
        }
        return self.__send_sync(send_type.MT_GET_ROOM_DETAIL_MSG, data)

    def get_room_members(self, room_wxid: str):
        """
        获取群成员列表
        """
        data = {
            "room_wxid": room_wxid
        }
        return self.__send_sync(send_type.MT_GET_ROOM_MEMBERS_MSG, data)

    def send_text(self, to_wxid: str, content: str):
        """
        发送文本消息
        """
        data = {
            "to_wxid": to_wxid,
            "content": content
        }
        return self.__send(send_type.MT_SEND_TEXT_MSG, data)

    def send_room_at_msg(self, to_wxid: str, content: str, at_list: List[str]):
        """
        发送群@消息
        """
        data = {
            'to_wxid': to_wxid,
            'content': content,
            'at_list': at_list
        }
        return self.__send(send_type.MT_SEND_ROOM_AT_MSG, data)

    def send_card(self, to_wxid: str, card_wxid: str):
        """
        发送名片
        """
        data = {
            'to_wxid': to_wxid,
            'card_wxid': card_wxid
        }
        return self.__send(send_type.MT_SEND_CARD_MSG, data)

    def send_link_card(self, to_wxid: str, title: str, desc: str, url: str, image_url: str):
        """
        发送链接卡片
        """
        data = {
            'to_wxid': to_wxid,
            'title': title,
            'desc': desc,
            'url': url,
            'image_url': image_url
        }
        return self.__send(send_type.MT_SEND_LINK_MSG, data)

    def send_image(self, to_wxid: str, file_path: str):
        """
        发送图片
        """
        data = {
            'to_wxid': to_wxid,
            'file': file_path
        }
        return self.__send(send_type.MT_SEND_IMAGE_MSG, data)

    def send_file(self, to_wxid: str, file_path: str):
        """
        发送文件
        """
        data = {
            'to_wxid': to_wxid,
            'file': file_path
        }
        return self.__send(send_type.MT_SEND_FILE_MSG, data)

    #
    def send_video(self, to_wxid: str, file_path: str):
        """
        发送视频
        """
        data = {
            'to_wxid': to_wxid,
            'file': file_path
        }
        return self.__send(send_type.MT_SEND_VIDEO_MSG, data)

    def send_gif(self, to_wxid, file):
        """
        发送gif:
        """
        data = {
            'to_wxid': to_wxid,
            'file': file
        }
        return self.__send(send_type.MT_SEND_GIF_MSG, data)

    def send_xml(self, to_wxid, xml, app_type=5):
        """
        发送xml消息
        """
        data = {
            "to_wxid": to_wxid,
            "xml": xml,
            "app_type": app_type
        }
        return self.__send(send_type.MT_SEND_XML_MSG, data)

    def send_pat(self, room_wxid: str, patted_wxid: str):
        """
        发送拍一拍
        """
        data = {
            "room_wxid": room_wxid,
            "patted_wxid": patted_wxid
        }
        return self.__send_sync(send_type.MT_SEND_PAT_MSG, data)

    def accept_friend_request(self, encryptusername: str, ticket: str, scene: int):
        """
        同意加好友请求
        """
        data = {
            "encryptusername": encryptusername,
            "ticket": ticket,
            "scene": scene
        }
        return self.__send_sync(send_type.MT_ACCEPT_FRIEND_MSG, data)

    def create_room(self, member_list: List[str]):
        """
        创建群
        """
        return self.__send(send_type.MT_CREATE_ROOM_MSG, member_list)

    def add_room_member(self, room_wxid: str, member_list: List[str]):
        """
        添加好友入群
        """
        data = {
            "room_wxid": room_wxid,
            "member_list": member_list
        }
        return self.__send_sync(send_type.MT_ADD_TO_ROOM_MSG, data)

    def invite_room_member(self, room_wxid: str, member_list: List[str]):
        """
        邀请好友入群
        """
        data = {
            "room_wxid": room_wxid,
            "member_list": member_list
        }
        return self.__send_sync(send_type.MT_INVITE_TO_ROOM_MSG, data)

    def del_room_member(self, room_wxid: str, member_list: List[str]):
        """
        删除群成员
        """
        data = {
            "room_wxid": room_wxid,
            "member_list": member_list
        }
        return self.__send_sync(send_type.MT_DEL_ROOM_MEMBER_MSG, data)

    def modify_room_name(self, room_wxid: str, name: str):
        """
        修改群名
        """
        data = {
            "room_wxid": room_wxid,
            "name": name
        }
        return self.__send_sync(send_type.MT_MOD_ROOM_NAME_MSG, data)

    def modify_room_notice(self, room_wxid: str, notice: str):
        """
        修改群公告
        """
        data = {
            "room_wxid": room_wxid,
            "notice": notice
        }
        return self.__send_sync(send_type.MT_MOD_ROOM_NOTICE_MSG, data)

    def add_room_friend(self, room_wxid: str, wxid: str, verify: str):
        """
        添加群成员为好友
        """
        data = {
            "room_wxid": room_wxid,
            "wxid": wxid,
            "source_type": 14,
            "remark": verify
        }
        return self.__send_sync(send_type.MT_ADD_FRIEND_MSG, data)

    def quit_room(self, room_wxid: str):
        """
        退出群
        """
        data = {
            "room_wxid": room_wxid
        }
        return self.__send(send_type.MT_QUIT_DEL_ROOM_MSG, data)

    def modify_friend_remark(self, wxid: str, remark: str):
        """
        修改好友备注
        """
        data = {
            "wxid": wxid,
            "remark": remark
        }
        return self.__send_sync(send_type.MT_MODIFY_FRIEND_REMARK, data)

    def get_room_name(self, room_wxid: str) -> str:
        """
        获取群名
        """
        sql = f"select nickname from contact where username='{room_wxid}'"
        result = self.sql_query(sql, 1)["result"]
        if result:
            return result[0][0]
        return ''
