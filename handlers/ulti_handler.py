from utils.autho_press import User_Info
from handlers.main import Base

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
        next_url = self.get_argument('next', '')  #校验用户名和密码
        passed = User_Info.Virity_User(username, password)

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
            result = User_Info.Reg_User(R_username,R_password1)
            if result:
                self.write('注册成功!')
                self.session.set('s_user',R_username)
                self.redirect(r'/')
            else:
                self.write('用户名已注册，请选择其它用户名')
                self.redirect(r'/regist')

        else:
            self.write('用户名不能为空或两次密码输入不一致！')


