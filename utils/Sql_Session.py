import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy.dialects



HOST = 'localhost'
USER = 'admin'
PASSWD = 'Root110qwe'
PORT = 3306
DB = 'python_test'
DB_INFO = "mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWD, HOST,PORT, DB)

def Engine(db_info):
        return sqlalchemy.create_engine(db_info)


Session = sessionmaker(Engine(DB_INFO))()    #数据库操作Session

Sql_Base = declarative_base(Engine(DB_INFO))   #数据库基类

