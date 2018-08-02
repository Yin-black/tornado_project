import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy.dialects


class  Sql_Info():    #创建数据库引擎
    HOST = 'localhost'
    USER = 'admin'
    PASSWD = 'Root110qwe'
    PORT = 3306
    DB = 'python_test'
    database_info = "mysql+pymysql://{}:{}@{}/{}".format(USER, PASSWD, HOST, DB)

    @classmethod
    def Engine(cls):
        return sqlalchemy.create_engine(cls.database_info)


Session = sessionmaker(Sql_Info.Engine())()    #数据库操作Session

Sql_Base = declarative_base(Sql_Info.Engine())   #数据库基类

