import xcgui
import ntchat
from xcgui import XApp, XWindow


class NtChatWindow(XWindow):
    def __init__(self):
        super(NtChatWindow, self).__init__()
        self.loadLayout("resources\\send_text_ui.xml")
        self.setMinimumSize(600, 500)

        btn: xcgui.XButton = self.findObjectByName("btn_open")
        btn.regEvent(xcgui.XE_BNCLICK, self.on_btn_open_clicked)

        btn: xcgui.XButton = self.findObjectByName("btn_send")
        btn.regEvent(xcgui.XE_BNCLICK, self.on_btn_send_clicked)

        self.edit_wxid: xcgui.XEdit = self.findObjectByName("edit_wxid")
        self.edit_content: xcgui.XEdit = self.findObjectByName("edit_content")
        self.edit_log: xcgui.XEdit = self.findObjectByName("edit_log")
        self.edit_log.enableAutoWrap(True)

        self.wechat_instance: ntchat.WeChat = None

    def on_btn_open_clicked(self, sender, _):
        self.wechat_instance = ntchat.WeChat()
        self.wechat_instance.open(smart=True)

        # 监听所有通知消息
        self.wechat_instance.on(ntchat.MT_ALL, self.on_recv_message)

    def on_btn_send_clicked(self, sender, _):
        if not self.wechat_instance or not self.wechat_instance.login_status:
            svg = xcgui.XSvg.loadFile("resources\\warn.svg")
            svg.setSize(16, 16)
            self.notifyMsgWindowPopup(xcgui.position_flag_top, "警告", "请先打开并登录微信",
                                      xcgui.XImage.loadSvg(svg), xcgui.notifyMsg_skin_warning)
        else:
            self.wechat_instance.send_text(self.edit_wxid.getText(), self.edit_content.getText())

    def on_recv_message(self, wechat, message):
        text = self.edit_log.getText()
        text += "\n"
        text += str(message)
        self.edit_log.setText(text)
        self.redraw()


if __name__ == '__main__':
    app = XApp()
    window = NtChatWindow()
    window.showWindow()
    app.run()
    ntchat.exit_()
    app.exit()
