from utils.Sql_Session import Sql_Base,Session
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship
from utils.autho_press import UserInfo
import uuid
import os


class Post(Sql_Base):
    __tablename__ = 'postname'
    imgid = Column(Integer,primary_key=True,autoincrement = True)
    imgurl = Column(String(100),nullable=True)
    thumbsurl = Column(String(100),nullable=True)
    user_id = Column(Integer,ForeignKey(UserInfo.id))

    Post= relationship(UserInfo,backref = 'post',uselist = False,cascade = 'all')

    @classmethod
    def selec_thumbs_url(cls,userid):
        """
        从数据库取所有的upolad和缩略图地址
        """
        return Session.query(Post.imgurl, Post.thumbsurl).filter(Post.user_id ==userid).all()

    @classmethod
    def get_current_user_id(cls,user_name):
        """
        获取当前用户id
        """
        re = Session.query(UserInfo).filter(UserInfo.username == user_name).first()
        if re:
            return re.id
        else:
            return False

    @classmethod
    def  u_add(cls,current_user_id,filename,thumbs_url):
        """
            增加图片upload图片url
            """
        newimg_url = Post(user_id = current_user_id,imgurl= filename,thumbsurl=thumbs_url)
        Session.add(newimg_url)
        Session.commit()

    @classmethod
    def get_imgurl(cls,id):
        """
            获取图片upload图片url
            """
        return Session.query(cls.imgurl).filter(cls.imgid== id).first()




class PostUrl():
    upload_addr = 'uploads'
    thumbs_addr = 'thubms'

    def __init__(self,static_addr):
        self.static_addr = static_addr
        self.name = self.gen_name()

    def gen_name(self):
        return uuid.uuid4().hex

    def get_post_url(self,filename):
        """
        生成post到uploads文件夹地址
        """
        _, ext = os.path.splitext(filename)
        return os.path.join(self.upload_addr, self.name+ext)

    def get_thumbs_url(self,filename):
        """
        生成缩略图到uploads/thumbs的地址
        """
        _, ext = os.path.splitext(filename)
        return os.path.join(self.upload_addr, self.thumbs_addr, self.name+ext)

    @classmethod
    def save_post_img(cls,static_url,post_url,post_file_name,content):
        """
        保存post的图片到uploads文件夹
        """

        # file,ext = os.path.splitext(post_file_name)
        with open(static_url+'/'+post_url,'wb') as f:
            f.write(content)

    @classmethod
    def save_thumbs_img(cls,static_url,thumbs_url,post_file_name,content):
        """
        保存成thubms图片
        """
        # file, ext = os.path.splitext(post_file_name)
        with open(static_url+'/'+thumbs_url, 'wb') as f:
            f.write(content)

    @classmethod
    def save_sql_url(cls,user_id,post_url,thumbs_url):
        """
        地址写入数据库
        """
        current_user_id = Post.get_current_user_id(user_id)
        if current_user_id:
            Post.u_add(current_user_id, post_url,thumbs_url)
        else:
            return False


