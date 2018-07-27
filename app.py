from tornado.web import RequestHandler
from tornado.options import options,define
import tornado
from tornado.ioloop import IOLoop
from handlers import main
define('port',default=8000,type=int,help='Open Port')

class Application(tornado.web.Application):
    def __init__(self):
        handlers= [
            (r'/',main.IndexHandler),
            (r'/post/(?P<post_id>[0-9]+)',main.PostHandler),
            (r'/explore',main.ExploreHandler)
        ]
        settings =dict(
            static_path= 'static',
            template_path= 'templates',
            debug = True,
        )
        super().__init__(handlers,**settings)



if __name__ == "__main__":
    app = Application()
    options.parse_command_line()
    print("Server start on port:{}".format(str(options.port)))
    app.listen(options.port)
    IOLoop.current().start()