from services.base_service import BaseService
from sql.sql import Item
from sqlalchemy.sql import func


# Item 服务
class ItemService(BaseService):
    # 分页查询
    def get_item_paging(self, page_size=5, page_index=0):
        """
        :param page_size:int  一页显示的条目数
        :param page_index:int  当前页码
        :return: sources[]
        """
        session = self.get_session()
        items = session.query(Item).limit(page_size).offset(
            (page_index - 1) * page_size)
        session.close()
        return items

    def get_item_paging_by_source_ids(self, source_ids, page_size=5, page_index=0):
        """
        :param page_size:int  一页显示的条目数
        :param page_index:int  当前页码
        :param source_ids:int[]  要显示的源的id数组
        :return: sources[]
        """
        session = self.get_session()
        items = session.query(Item).filter(Item.source_id.in_(source_ids)).limit(page_size).offset(
            (page_index - 1) * page_size)
        session.close()
        return items

    def get_item_paging_by_source_id(self, source_id, page_size=5, page_index=0):
        """
        :param page_size:int  一页显示的条目数
        :param page_index:int  当前页码
        :param source_id:int  要显示的源的id
        :return: sources[]
        """
        session = self.get_session()
        items = session.query(Item).filter_by(source_id=source_id).limit(page_size).offset(
            (page_index - 1) * page_size)
        session.close()
        return items

    def add_item(self, title, source, content):
        session = self.get_session()
        session.add(Item(title=title,
                         content=content,
                         source_id=source.id,
                         range=source.range,
                         source_icon=source.source_icon,
                         source_name=source.source_name
                         ))
        session.commit()
        session.close()

    def add_items(self, items):
        session = self.get_session()
        session.add_all(items)
        session.commit()
        session.close()
