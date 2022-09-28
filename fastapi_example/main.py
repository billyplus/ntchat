# -*- coding: utf-8 -*-
import uvicorn
from functools import wraps
from fastapi import FastAPI
from mgr import ClientManager
from down import get_local_path
from exception import MediaNotExistsError, ClientNotExists
import models
import ntchat


def response_json(status=0, data=None, msg=""):
    return {
        "status": status,
        "data": {} if data is None else data,
        "msg": msg
    }


class catch_exception:
    def __call__(self, f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            try:
                return await f(*args, **kwargs)
            except ntchat.WeChatNotLoginError:
                return response_json(msg="wechat instance not login")
            except ntchat.WeChatBindError:
                return response_json(msg="wechat bind error")
            except ntchat.WeChatVersionNotMatchError:
                return response_json(msg="wechat version not match, install require wechat version")
            except MediaNotExistsError:
                return response_json(msg="file_path or url error")
            except ClientNotExists as e:
                return response_json(msg="client not exists, guid: %s" % e.guid)
            except Exception as e:
                return response_json(msg=str(e))

        return wrapper


client_mgr = ClientManager()
app = FastAPI(title="NtChat fastapi完整示例",
              description="NtChat项目地址: https://github.com/smallevilbeast/ntchat")


@app.post("/client/create", summary="创建实例", tags=["Client"],
          response_model=models.ResponseModel)
@catch_exception()
async def client_create():
    guid = client_mgr.create_client()
    return response_json(1, {"guid": guid})


@app.post("/client/open", summary="打开微信", tags=["Client"],
          response_model=models.ResponseModel)
@catch_exception()
async def client_open(model: models.ClientOpenReqModel):
    ret = client_mgr.get_client(model.guid).open(model.smart, model.show_login_qrcode)
    return response_json(1 if ret else 0)


@app.post("/global/set_callback_url", summary="设置接收通知地址", tags=["Global"],
          response_model=models.ResponseModel)
@catch_exception()
async def client_set_callback_url(model: models.CallbackUrlReqModel):
    client_mgr.callback_url = model.callback_url
    return response_json(1)


@app.post("/user/get_profile", summary="获取自己的信息", tags=["User"],
          response_model=models.ResponseModel)
@catch_exception()
async def user_get_profile(model: models.ClientReqModel):
    data = client_mgr.get_client(model.guid).get_self_info()
    return response_json(1, data)


@app.post("/contact/get_contacts", summary="获取联系人列表", tags=["Contact"],
          response_model=models.ResponseModel)
@catch_exception()
async def get_contacts(model: models.ClientReqModel):
    data = client_mgr.get_client(model.guid).get_contacts()
    return response_json(1, data)


@app.post("/contact/get_contact_detail", summary="获取指定联系人详细信息", tags=["Contact"],
          response_model=models.ResponseModel)
@catch_exception()
async def get_contact_detail(model: models.ContactDetailReqModel):
    data = client_mgr.get_client(model.guid).get_contact_detail(model.wxid)
    return response_json(1, data)


@app.post("/contact/modify_remark", summary="修改联系人备注", tags=["Contact"], response_model=models.ResponseModel)
@catch_exception()
async def send_gif(model: models.ModifyFriendRemarkReqModel):
    data = client_mgr.get_client(model.guid).modify_friend_remark(model.wxid, model.remark)
    return response_json(1, data)


@app.post("/room/get_rooms", summary="获取群列表", tags=["Room"],
          response_model=models.ResponseModel)
@catch_exception()
async def get_rooms(model: models.ClientReqModel):
    data = client_mgr.get_client(model.guid).get_rooms()
    return response_json(1, data)


@app.post("/room/get_room_members", summary="获取群成员列表", tags=["Room"],
          response_model=models.ResponseModel)
@catch_exception()
async def get_room_members(model: models.GetRoomMembersReqModel):
    data = client_mgr.get_client(model.guid).get_room_members(model.room_wxid)
    return response_json(1, data)


@app.post("/room/create_room", summary="创建群", tags=["Room"],
          response_model=models.ResponseModel)
@catch_exception()
async def create_room(model: models.CreateRoomReqModel):
    ret = client_mgr.get_client(model.guid).create_room(model.member_list)
    return response_json(1 if ret else 0)


@app.post("/room/add_room_member", summary="添加好友入群", tags=["Room"],
          response_model=models.ResponseModel)
@catch_exception()
async def add_room_member(model: models.RoomMembersReqModel):
    data = client_mgr.get_client(model.guid).add_room_member(model.room_wxid, model.member_list)
    return response_json(1, data)


@app.post("/room/invite_room_member", summary="邀请好友入群", tags=["Room"],
          response_model=models.ResponseModel)
@catch_exception()
async def invite_room_member(model: models.RoomMembersReqModel):
    data = client_mgr.get_client(model.guid).invite_room_member(model.room_wxid, model.member_list)
    return response_json(1, data)


@app.post("/room/del_room_member", summary="删除群成员", tags=["Room"],
          response_model=models.ResponseModel)
@catch_exception()
async def del_room_member(model: models.RoomMembersReqModel):
    data = client_mgr.get_client(model.guid).del_room_member(model.room_wxid, model.member_list)
    return response_json(1, data)


@app.post("/room/add_room_friend", summary="添加群成员为好友", tags=["Room"],
          response_model=models.ResponseModel)
@catch_exception()
async def add_room_friend(model: models.AddRoomFriendReqModel):
    data = client_mgr.get_client(model.guid).add_room_friend(model.room_wxid,
                                                             model.wxid,
                                                             model.verify)
    return response_json(1, data)


@app.post("/room/modify_name", summary="修改群名", tags=["Room"],
          response_model=models.ResponseModel)
@catch_exception()
async def add_room_friend(model: models.ModifyRoomNameReqModel):
    data = client_mgr.get_client(model.guid).modify_room_name(model.room_wxid,
                                                              model.name)
    return response_json(1, data)


@app.post("/room/quit_room", summary="退出群", tags=["Room"],
          response_model=models.ResponseModel)
@catch_exception()
async def quit_room(model: models.RoomReqModel):
    data = client_mgr.get_client(model.guid).quit_room(model.room_wxid)
    return response_json(1, data)


@app.post("/msg/send_text", summary="发送文本消息", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def msg_send_text(model: models.SendTextReqModel):
    ret = client_mgr.get_client(model.guid).send_text(model.to_wxid, model.content)
    return response_json(1 if ret else 0)


@app.post("/msg/send_room_at", summary="发送群@消息", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_room_at(model: models.SendRoomAtReqModel):
    ret = client_mgr.get_client(model.guid).send_room_at_msg(model.to_wxid,
                                                             model.content,
                                                             model.at_list)
    return response_json(1 if ret else 0)


@app.post("/msg/send_card", summary="发送名片", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_card(model: models.SendCardReqModel):
    ret = client_mgr.get_client(model.guid).send_card(model.to_wxid,
                                                      model.card_wxid)
    return response_json(1 if ret else 0)


@app.post("/msg/send_link_card", summary="发送链接卡片消息", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_link_card(model: models.SendLinkCardReqModel):
    ret = client_mgr.get_client(model.guid).send_link_card(model.to_wxid,
                                                           model.title,
                                                           model.desc,
                                                           model.url,
                                                           model.image_url)
    return response_json(1 if ret else 0)


@app.post("/msg/send_image", summary="发送图片", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_image(model: models.SendMediaReqModel):
    file_path = get_local_path(model)
    if file_path is None:
        raise MediaNotExistsError()
    ret = client_mgr.get_client(model.guid).send_image(model.to_wxid, file_path)
    return response_json(1 if ret else 0)


@app.post("/msg/send_file", summary="发送文件", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_file(model: models.SendMediaReqModel):
    file_path = get_local_path(model)
    if file_path is None:
        raise MediaNotExistsError()
    ret = client_mgr.get_client(model.guid).send_file(model.to_wxid, file_path)
    return response_json(1 if ret else 0)


@app.post("/msg/send_video", summary="发送视频", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_video(model: models.SendMediaReqModel):
    file_path = get_local_path(model)
    if file_path is None:
        raise MediaNotExistsError()
    ret = client_mgr.get_client(model.guid).send_video(model.to_wxid, file_path)
    return response_json(1 if ret else 0)


@app.post("/msg/send_gif", summary="发送GIF", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_gif(model: models.SendMediaReqModel):
    file_path = get_local_path(model)
    if file_path is None:
        raise MediaNotExistsError()
    ret = client_mgr.get_client(model.guid).send_gif(model.to_wxid, file_path)
    return response_json(1 if ret else 0)


@app.post("/msg/send_xml", summary="发送XML原始消息", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_gif(model: models.SendXmlReqModel):
    ret = client_mgr.get_client(model.guid).send_xml(model.to_wxid, model.xml)
    return response_json(1 if ret else 0)


@app.post("/msg/send_pat", summary="发送拍一拍", tags=["Msg"], response_model=models.ResponseModel)
@catch_exception()
async def send_gif(model: models.SendPatReqModel):
    data = client_mgr.get_client(model.guid).send_pat(model.room_wxid, model.patted_wxid)
    return response_json(1, data)


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8000)
