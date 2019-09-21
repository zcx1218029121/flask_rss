from services.base_service import BaseService
from sql.sql import Source


class SourceService(BaseService):
    # 根据 id 查询source的细节
    def source_detail(self, source_id):
        """
        :param source_id:int  id of source
        :return: sources:Source
        """
        session = self.get_session()
        source = session.query(Source).filter_by(id=source_id).first()
        session.close()
        return source

    def source_details(self, source_ids):
        """
        :param source_ids:int []
        :return: sources[]
        """
        session = self.get_session()
        sources = session.query(Source).filter(Source.id.in_(source_ids)).all()
        session.close()
        return sources

    def source_all(self):
        session = self.get_session()
        sources = session.query(Source).all()
        session.close()
        return sources
