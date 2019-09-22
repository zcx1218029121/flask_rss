FROM python:3.5
ADD ./ /usr/src/file
MAINTAINER loafer
EXPOSE  9091
VOLUME /db
WORKDIR /usr/src/file
# 安装网络框架 flask
RUN pip install Flask -i https://pypi.douban.com/simple
#  安装定时任务工具
RUN pip install apscheduler -i https://pypi.douban.com/simple
# 安装美丽汤
RUN pip install beautifulsoup4 -i https://pypi.douban.com/simple
# ORM 框架
RUN pip install sqlalchemy -i https://pypi.douban.com/simple
RUN pip install requests -i https://pypi.douban.com/simple
# 安装redits 连接模块
RUN pip3 install redis -i https://pypi.douban.com/simple
CMD ["python", "app.py"]
