from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask import request
from sql.sql import User
from sql.sql import Base


class UserService:
    def __init__(self, sql_path="sqlite:///db/rss.db?check_same_thread=False"):
        self.sql_path = sql_path
        self.engine = create_engine(self.sql_path, echo=True)

    def init_db(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        session = sessionmaker(bind=self.engine)
        session = session()
        return session

    def login(self, user_name, pass_word):
        user = self.get_session().query(User).filter_by(name=user_name, password=pass_word).first()
        return user
