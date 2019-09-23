from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import os

Base = declarative_base()
engine = create_engine("sqlite:///db/rss.db?check_same_thread=False", echo=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    # 用户名
    name = Column(String(20))
    # 用户昵称
    nick_name = Column(String(32))
    # 用户头像
    head_icon = Column(String(255))
    # 用户密码  md5 加密
    password = Column(String(32))
    # 用户权限
    range = Column(Integer)


class Item(Base):
    __tablename__ = 'item'
    # 指定id映射到id字段; id字段为整型，为主键
    id = Column(Integer, primary_key=True)
    # 指定name映射到name字段; name字段为字符串类形，
    title = Column(String(255))
    # content 富文本 洗掉 js 标签
    content = Column(Text)
    link = Column(String(255))
    # time 更新时间
    time = Column(DateTime(timezone=True), server_default=func.now(format("YYYY-MM-DD HH:MM")))
    # Source id 请求源
    source_id = Column(Integer)
    # 源 name
    source_name = Column(String(30))
    # 源 icon
    source_icon = Column(String(255))
    # 源 等级
    range = Column(Integer)


class Source(Base):
    __tablename__ = 'source'
    # 源 id
    id = Column(Integer, primary_key=True)
    # 源 name
    source_name = Column(String(30))
    # 源 icon
    source_icon = Column(String(255))

    url = Column(String(255))
    # 源 等级
    range = Column(Integer)


class Subscribe(Base):
    __tablename__ = 'subscribe'
    user_id = Column(Integer, primary_key=True)
    source_id = Column(Integer, primary_key=True)
    time = Column(DateTime(timezone=True), server_default=func.now())


def init_table(force_creat=False):
    if force_creat:
        Base.metadata.create_all(engine)
        return
    if not os.path.exists("../db/rss.db"):
        Base.metadata.create_all(engine)
    else:
        print("skip db creat...")
