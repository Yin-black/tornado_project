import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import uuid
from tornado.web import authenticated,RequestHandler
import redis
import _ctypes


from .main import Base

class ChatHandler(Base):
    """
    聊天室
    """
    @authenticated
    def get(self):
        self.render("websocket.html",messages = WebsocketHandler.cache)

class WebsocketHandler(tornado.websocket.WebSocketHandler,Base):
    waiters = set()
    cache = []
    cache_size = 100

    # Redis = redis.Redis(host='localhost',port=6379)

    def get_compression_option(self):
        """非None的返回值"""
        return {}

    def open(self, *args, **kwargs):
        """新的websocket连接打开"""
        # self.Redis.sadd('waiters',id(self))
        logging.info("new connectin %s"% self)
        WebsocketHandler.waiters.add(self)

    def on_close(self):
        """websocket断开"""
        WebsocketHandler.waiters.remove(self)
        # self.Redis.srem('waiters',id(self))

    @classmethod
    def update_cache(cls,chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls,chat):
        """给所有用户发送消息"""
        logging.info("sending message to %d waiters"%len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error send message",exc_info =True)

    def on_message(self, message):
        """websocket接收数据"""
        logging.info("got message %r",message)
        parsed = tornado.escape.json_decode(message) #把json对象转换为python 字典
        chat = {
            "id" : str(uuid.uuid4()),
            "body" : parsed['body'],
        }

        if chat["body"].startswith('http://' or "https://"):  #如果信息内容是图片网址，则调用AsyncSaveImages函数
            pass
        #用chat字典渲染messsage.html文件后，返回的html数据,保存到chat['html']下
        chat['html']= tornado.escape.to_basestring(self.render_string("message.html",message=chat))

        WebsocketHandler.update_cache(chat)
        WebsocketHandler.send_updates(chat)