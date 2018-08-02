from tornado.web import RequestHandler
from tornado.options import options,define
import tornado
from tornado.ioloop import IOLoop
from handlers import main
from handlers.ulti_handler import LoginHandler,LogoutHandler,RegistHandler

import pycket
import redis
define('port',default=8000,type=int,help='Open Port')

class Application(tornado.web.Application):
    def __init__(self):
        handlers= [
            (r'/',main.IndexHandler),
            (r'/post/(?P<post_id>[0-9]+)',main.PostHandler),
            (r'/explore',main.ExploreHandler),
            (r'/upload',main.UploadHandler),
            (r'/login',LoginHandler),
            (r'/logout',LogoutHandler),
            (r'/regist',RegistHandler),
        ]
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
            }
        )
        super().__init__(handlers,**settings)



if __name__ == "__main__":
    app = Application()
    options.parse_command_line()
    print("Server start on port:{}".format(str(options.port)))
    app.listen(options.port)
    IOLoop.current().start()