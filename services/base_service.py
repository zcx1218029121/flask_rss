from sqlalchemy.orm import sessionmaker
from sql.sql import engine as sql_engine


# 数据库操作服务 继承
class BaseService:
    def __init__(self, engine=sql_engine):
        self.engine = engine

    def get_session(self):
        session = sessionmaker(bind=self.engine)
        session = session()
        return session
