from typing import Optional, List, Any, Union, Dict
from pydantic import BaseModel


class ClientReqModel(BaseModel):
    guid: str


class ResponseModel(BaseModel):
    status: int
    msg: Optional[str] = ""
    data: Optional[Any] = None


class ClientOpenReqModel(ClientReqModel):
    smart: Optional[bool] = True
    show_login_qrcode: Optional[bool] = False


class CallbackUrlReqModel(BaseModel):
    callback_url: Optional[str] = ""


class UserProfileModel(BaseModel):
    wxid: str
    nickname: str
    account: str
    avatar: str


class ContactModel(BaseModel):
    account: str
    avatar: str
    city: str
    country: str
    nickname: str
    province: str
    remark: str
    sex: int
    wxid: str


class ContactDetailReqModel(ClientReqModel):
    wxid: str


class ContactDetailModel(BaseModel):
    account: str
    avatar: str
    city: str
    country: str
    nickname: str
    province: str
    remark: str
    sex: int
    wxid: str
    signature: str
    small_avatar: str
    sns_pic: str
    source_type: int
    status: int
    v1: str
    v2: str


class AcceptFriendReqModel(ClientReqModel):
    encryptusername: str
    ticket: str
    scene: int


class RoomModel(BaseModel):
    wxid: str
    nickname: str
    avatar: str
    is_manager: int
    manager_wxid: str
    total_member: int
    member_list: List[str]


class RoomMemberModel(ContactModel):
    display_name: str


class GetRoomMembersReqModel(ClientReqModel):
    room_wxid: str


class GetRoomNameReqModel(ClientReqModel):
    room_wxid: str


class CreateRoomReqModel(ClientReqModel):
    member_list: List[str]


class RoomMembersReqModel(CreateRoomReqModel):
    room_wxid: str


class AddRoomFriendReqModel(ClientReqModel):
    room_wxid: str
    wxid: str
    verify: str


class RoomReqModel(ClientReqModel):
    room_wxid: str


class ModifyRoomNameReqModel(RoomReqModel):
    name: str


class SendMsgReqModel(ClientReqModel):
    to_wxid: str


class SendTextReqModel(SendMsgReqModel):
    content: str


class SendRoomAtReqModel(SendTextReqModel):
    at_list: List[str]


class SendCardReqModel(SendMsgReqModel):
    card_wxid: str


class SendLinkCardReqModel(SendMsgReqModel):
    title: str
    desc: str
    url: str
    image_url: str


class SendMediaReqModel(SendMsgReqModel):
    file_path: Optional[str] = ""
    url: Optional[str] = ""


class SendXmlReqModel(SendMsgReqModel):
    xml: str


class SendPatReqModel(ClientReqModel):
    room_wxid: str
    patted_wxid: str


class ModifyFriendRemarkReqModel(ClientReqModel):
    wxid: str
    remark: str


