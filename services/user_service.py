from sql.sql import User
from sql.sql import Base
from services.base_service import BaseService


class UserService(BaseService):

    def init_db(self):
        Base.metadata.create_all(self.engine)

    def login(self, user_name, pass_word):
        session = self.get_session()
        user = session.query(User).filter_by(name=user_name, password=pass_word).first()
        session.close()
        return user

    def get_user_by_id(self, uid):
        session = self.get_session()
        user = session.query(User).filter_by(id=uid).first()
        session.close()
        return user
