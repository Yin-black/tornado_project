from sqlalchemy import Column,Integer,DateTime,String,ForeignKey
from datetime import datetime
import hashlib
from utils.Sql_Session import Sql_Base,Session
from sqlalchemy.orm import relationship


class UserInfo(Sql_Base):
    """
    user_info基类
    """
    __tablename__ = 'user_info'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(20),default=None,nullable=False)
    password = Column(String(50),default=None)
    creattime = Column(DateTime,default=datetime.now)

    @classmethod
    def hash_data(cls,data):
        """
        MD5加密
        """
        return hashlib.md5(data.encode()).hexdigest()

    @classmethod
    def virity_user(cls,username,password):  #验证用户名和密码是否正确
        if username and password:
            return Session.query(UserInfo.id).filter(UserInfo.username == username and UserInfo.password== UserInfo.hash_data(password)).all()
        else:
            return False

    @classmethod
    def reg_user(cls,R_username,R_password):
        """
        用户注册，写入数据库
        """
        rel = Session.query(UserInfo).filter(UserInfo.username == R_username).all()  #用户名不能重
        if rel:
            return False
        has_password =  UserInfo.hash_data(R_password)
        new_user = UserInfo(username = R_username,password = has_password)
        Session.add(new_user)
        Session.commit()
        return True

class Like(Sql_Base):
    __tablename__ = 'likes'
    user_id = Column(Integer,ForeignKey('user_info.id'),nullable=True,primary_key=True)
    post_id = Column(Integer,ForeignKey('postname.imgid'),nullable=True,primary_key=True)

    # likes = relationship('UserInfo',backref = 'likes_link',secondary = 'Like')

    @classmethod
    def get_post_id(cls,user_id):
        post_id = Session.query(cls.post_id).filter(cls.user_id == user_id).all()
        return post_id