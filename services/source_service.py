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

    def source_all(self, user_range=0, page_index=0, page_size=20):
        """"
        该方法返回大于用户range的数据
        :param user_range:int 用户权限
        :param page_index :int 当前分页
        :param page_size:int 分页数量
        """
        session = self.get_session()
        sources = session.query(Source).filter(Source.range > user_range).limit(page_size).offset(
            (page_index - 1) * page_size)
        session.close()
        return sources
