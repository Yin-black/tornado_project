from utils.Sql_Session import Sql_Base,Session
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship
from utils.autho_press import User_Info


class Post(Sql_Base):
    __tablename__ = 'postname'
    imgid = Column(Integer,primary_key=True,autoincrement = True)
    imgurl = Column(String(100),nullable=True)
    user_id = Column(Integer,ForeignKey(User_Info.id))

    Post= relationship(User_Info,backref = 'post',uselist = False,cascade = 'all')

    @classmethod
    def get_current_user_id(cls,user_name):
        """
        获取当前用户id
        """
        re = Session.query(User_Info).filter(User_Info.username == user_name).first()
        if re:
            return re.id
        else:
            return False

    @classmethod
    def Add(cls,current_user_id,filename):
        """
            增加图片url
            """
        newimg_url = Post(user_id = current_user_id,imgurl= filename,)
        Session.add(newimg_url)
        Session.commit()

    @classmethod
    def get_imgurl(cls,id):
        """
            获取图片url
            """
        return Session.query(cls.imgurl).filter(cls.imgid== id).first()