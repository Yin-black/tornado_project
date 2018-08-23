from utils.autho_press import UserInfo
from utils.post_press import Post,PostUrl,Like
from utils.Sql_Session import Session
from handlers.main import Base
import time
import tornado.websocket
from tornado.web import authenticated
from tornado.httpclient import HTTPClient,AsyncHTTPClient
from tornado.gen    import coroutine
import redis
import _ctypes
import pickle

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
    users =set()
    # Redis = redis.Redis(host="localhost", port=6379)
    def open(self):
        MsgWebScoketHandler.users.add(self)
        # self.Redis.sadd('users',id(self))

        for u in MsgWebScoketHandler.users:  # 向已在线用户发送消息
             u.write_message(
             u"[%s]-[%s]-进入聊天室" % (self.current_user, time.strftime('%Y:%m:%d:%H:%M:%S',time.localtime())))

    def on_message(self, message):
        for u in MsgWebScoketHandler.users:
            u.write_message(u"[%s]-[%s]-说：%s"%(self.current_user,time.strftime('%Y:%m:%d:%H:%M:%S',time.localtime()),message))

    def on_close(self):
        MsgWebScoketHandler.users.remove(self)

class AsyncSaveImages(Base):
    """
    异步模式下载图片
    """
    @authenticated
    @coroutine     #用协程来实现异步
    def get(self):
        self.render('asyncsaveimage.html')

    @coroutine   #用协程来实现异步
    def post(self):
        url = self.get_argument('imgurl')
        print("----"+url)
        if url:
            respon = yield self.fetch(url)  #调用异步函数
            static_addr = self.settings['static_path']
            p_posturl = PostUrl(static_addr)

            post_url = p_posturl.get_post_url('1.jpg')
            p_posturl.save_post_img(static_addr, post_url, respon.body)

            thumbs_url = p_posturl.get_thumbs_url('1.jpg')
            p_posturl.save_thumbs_img(static_addr, thumbs_url, post_url, respon.body)

            current_user_id = self.current_user  # 把upload和thumbs图片url 存入数据库
            p_posturl.save_sql_url(current_user_id, post_url, thumbs_url)

        else:
            self.write('网址为空')
        self.render('asyncsaveimage.html')

    async def fetch(self,url):  #异步函数
        http_client = AsyncHTTPClient()
        try:
            respon = await http_client.fetch(url)
        except Exception as e:
            print("Error: %s"%e)
        return respon


class PostLike(Base):
    """
    对图片标记喜欢
    """
    def get(self):
        a=0
        p=self.get_argument('post_id')
        userid=Post.get_current_user_id(self.current_user)
        post_id = Like.get_post_id(userid)   #查询当前用户标记了喜欢的图片列表

        for s in post_id:
            for i in s:
                print(p,i)
                if int(p) == int(i):    #列表中有当前的图片ID
                    a=1
        if a == 1:
            self.write('like')
        else:
            self.write('unlike')

    def post(self):
        post_id = self.get_argument('post_id')
        active = self.get_argument('active')
        userid = Post.get_current_user_id(self.current_user)

        if active =='like':
            newlike = Like(user_id=userid,post_id = post_id)
            Session.add(newlike)
            Session.commit()
            print(1)
            self.write('like')
            pass
        elif active == 'unlike':
            re = Session.query(Like).filter(Like.post_id == post_id)[0]
            if re:
                Session.delete(re)
                Session.commit()
                print(2)
                self.write('unlike')
            else:
                print("出错")