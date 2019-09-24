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

    def update_user_by_id(self, uid, nick_name, pass_word, icon):
        session = self.get_session()
        user = session.query(User).filter_by(id=uid).update(
            {User.nick_name: nick_name, User.password: pass_word, User.head_icon: icon})
        session.commit()
        session.close()
        return user

    def registered(self, name, nick_name, pass_word, icon):
        session = self.get_session()
        user = session.query(User).filter_by(name=name).first()
        if user is not None:
            return
        # 登注册的用户默认权限为 2 级别
        # 1 级别为 r18
        session.add(User(name=name, nick_name=nick_name, password=pass_word, head_icon=icon, range=2))
        session.commit()
        session.close()
