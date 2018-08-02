
from sqlalchemy import Column,Integer,DateTime,String
from datetime import datetime
import hashlib
from utils.Sql_Session import Sql_Base,Session

def Hash_Data(data):
    """
    MD5加密

    """
    return hashlib.md5(data.encode()).hexdigest()



class User_Info(Sql_Base):
    """
    user_info基类
    """
    __tablename__ = 'user_info'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(20),default=None,nullable=False)
    password = Column(String(50),default=None)
    creattime = Column(DateTime,default=datetime.now)

    @classmethod
    def Virity_User(cls,username,password):  #验证用户名和密码是否正确
        if username and password:
            return Session.query(User_Info).filter(User_Info.username == username and User_Info.password== Hash_Data(password)).first()
        else:
            return False

    @classmethod
    def Reg_User(cls,R_username,R_password):
        """
        用户注册，写入数据库
        """
        rel = Session.query(User_Info).filter(User_Info.username == R_username).all()  #用户名不能重
        if rel:
            return False
        has_password =  Hash_Data(R_password)
        new_user = User_Info(username = R_username,password = has_password)
        Session.add(new_user)
        Session.commit()
        return True



