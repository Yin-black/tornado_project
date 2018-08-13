from utils.autho_press import UserInfo
from handlers.main import Base
import time
import tornado.websocket
from tornado.web import authenticated

class LoginHandler(Base):
    """
    登陆页面。跳转到登陆前的页面
    """
    def get(self, *args, **kwargs):
        next_url = self.get_argument('next', None)
        self.render('login.html',nexturl = next_url)

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        next_url = self.get_argument('next', '')
        #校验用户名和密码
        passed = UserInfo.virity_user(username, password)
        if passed:
            self.session.set('s_user',username)
            if next_url:
                self.redirect(r'/')
            else:
                self.redirect(next_url)
        else:
            self.redirect(r'/login')

class LogoutHandler(Base):
    """
    退出登陆，并删除session
    """
    def get(self, *args, **kwargs):
        if self.current_user:
            self.session.delete('s_user')
        self.redirect(r'/login')

class RegistHandler(Base):
    def get(self, *args, **kwargs):
        self.render("regist.html")

    def post(self, *args, **kwargs):
        R_username = self.get_argument('username', None)
        R_password1 = self.get_argument('password1', None)
        R_password2 = self.get_argument('password2', None)

        if R_username and R_password1 and (R_password1 == R_password2):
            result = UserInfo.reg_user(R_username,R_password1)
            if result:
                self.write('注册成功!')
                time.sleep(1)
                self.session.set('s_user',R_username)
                self.redirect(r'/')
            else:
                self.write('用户名已注册，请选择其它用户名')
                time.sleep(2)
                self.redirect(r'/regist')


        else:
            self.write('用户名不能为空或两次密码输入不一致！')
            time.sleep(2)
            self.redirect(r'/regist')


class ChartHandler(Base,tornado.websocket.WebSocketHandler):
    """
    聊天室
    """
    @authenticated
    def get(self):

        self.render('webchat.html')

class MsgWebScoketHandler(tornado.websocket.WebSocketHandler,Base):
    """
    websocket处理函数
    """
    users = set()
    def open(self):
        MsgWebScoketHandler.users.add(self)
        for u in MsgWebScoketHandler.users:  # 向已在线用户发送消息
            u.write_message(
                u"[%s]-[%s]-进入聊天室" % (self.current_user, time.strftime('%Y:%m:%d:%H:%M:%S',time.localtime())))

    def on_message(self, message):
        for u in MsgWebScoketHandler.users:

            u.write_message(u"[%s]-[%s]-说：%s"%(self.current_user,time.strftime('%Y:%m:%d:%H:%M:%S',time.localtime()),message))

    def on_close(self):
        if self in MsgWebScoketHandler.users:
            self.users.remove(self)