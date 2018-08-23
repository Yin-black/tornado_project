from tornado.web import RequestHandler
from tornado.options import options,define
import tornado
from tornado.ioloop import IOLoop
from handlers.main import IndexHandler,PostHandler,ExploreHandler,ProfileHandler,UploadHandler
from handlers.ulti_handler import AsyncSaveImages,LoginHandler,LogoutHandler,RegistHandler,ChartHandler,MsgWebScoketHandler,PostLike
from handlers.chat import WebsocketHandler,ChatHandler

import pycket
import redis

define('port',default=8000,type=int,help='Open Port')

def redis_init():  #初始化redis  users列表
    Redis = redis.Redis(host="localhost", port=6379)
    # if Redis.scard('users') > 0:
    #     for u in Redis.smembers('users'):
    #         Redis.srem('users',u)
    # if Redis.scard('waiters') > 0:
    #     for u in Redis.smembers('waiters'):
    #         Redis.srem('waiters',u)

class Application(tornado.web.Application):
    def __init__(self):
        redis_init()
        handlers= [
            (r'/',IndexHandler),
            (r'/post/(?P<post_id>[0-9]+)',PostHandler),
            # (r'/profile/(?P<id>[0-9]+)',ProfileHandler),
            (r'/explore',ExploreHandler),
            (r'/upload',UploadHandler),
            (r'/login',LoginHandler),
            (r'/logout',LogoutHandler),
            (r'/regist',RegistHandler),
            (r'/chat',ChartHandler),
            (r'/websocket',MsgWebScoketHandler),
            (r'/profile',ProfileHandler),
            (r'/save',AsyncSaveImages),
            (r'/like',PostLike),
            (r'/web',ChatHandler), #老师的版本
            (r'/ws',WebsocketHandler),#老师的版本
        ],
        settings =dict(
            static_path= 'static',
            template_path= 'templates',
            debug = True,
            login_url = '/login',
            cookie_secret = 'wigjigjiajgiwewgj12413',
            pycket ={
                'engine':'redis',
                'storage':{
                    'host':'localhost',
                    'port':6379,
                    'db_sessions':5,
                    'db_notifications':11,
                    'max_connections':2**31,
                },
                'cokies':{
                    'expire_days':30,
                },
            },
        )
        super().__init__(*handlers,**settings)

if __name__ == "__main__":
    app = Application()
    options.parse_command_line()
    print("Server start on port:{}".format(str(options.port)))
    app.listen(options.port)
    IOLoop.current().start()