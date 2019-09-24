from services.base_service import BaseService
from sql.sql import Subscribe


class SubscribeService(BaseService):
    # 返回用户订阅的源id
    def get_source(self, user_id):
        session = self.get_session()
        subscribes = session.query(Subscribe).filter_by(user_id=user_id).all()
        session.close()
        return subscribes

    # 返回用户订阅的源id
    def get_source_id(self, user_id):
        session = self.get_session()
        result_list = []
        subscribes = session.query(Subscribe.source_id).filter_by(user_id=user_id).all()
        for subscribe in subscribes:
            result_list.append(subscribe.source_id)
        session.close()
        return result_list

    def add_source(self, user_id, source_id):
        session = self.get_session()
        session.add(Subscribe(user_id=user_id, source_id=source_id))
        session.commit()
        session.close()

    def del_source(self, user_id, source_id):
        session = self.get_session()
        s = session.query(Subscribe).filter_by(user_id=user_id, source_id=source_id).first()
        session.delete(s)
        session.commit()
        session.close()
