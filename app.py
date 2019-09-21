# jwt
from sql.sql import Item
import itsdangerous
import requests
from flask import Flask
from flask import request
from sql.sql import init_table
from services.item_service import ItemService
from services.subscribe_service import SubscribeService
from services.user_service import UserService
from services.source_service import SourceService
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

app = Flask(__name__)
# 盐
salt = "simple_rss1024"
jwt = itsdangerous.TimedJSONWebSignatureSerializer(salt, expires_in=60 * 60 * 24 * 7)

userService = UserService()
itemService = ItemService()
subscribeService = SubscribeService()
sourceService = SourceService()


def crawler_run(source):
    r = requests.get(source.url).text
    soup = BeautifulSoup(r, 'html.parser')
    items_bean = []
    items = soup.findAll('item')
    for item in items:
        title = item.find('title')
        content = item.find('description')
        link = item.find('link')
        item_bean = Item(title=title,
                         content=content,
                         link=link,
                         source_id=source.id,
                         range=source.range,
                         source_icon=source.source_icon,
                         source_name=source.source_name)
        items_bean.append(item_bean)
    itemService.add_items(items_bean)


def crawler():
    executor = ThreadPoolExecutor(max_workers=3)
    urls = []
    sources = sourceService.source_all()
    for source in sources:
        urls.append(source.url)
    executor.map(crawler_run, sources)


# jwt 验证拦截装饰器需要登录的方法在这里添加拦截器
def request_token(func):
    def deco():
        token = request.headers.get("token")
        if token is None:
            des = {"msg": "验证错误"}, 401
        else:
            try:
                user_dit = jwt.loads(token)
                des = func(user_dit)
            except Exception as e:
                print(e)
                return {"msg": "登录过期", "code": 403}, 403
        return des

    return deco


@app.route('/login', methods=['POST'])
def login():
    form = request.form
    user_name = form["userName"]
    pass_word = form["password"]
    user = userService.login(user_name, pass_word)
    if user is not None:
        return {"token": init_jwt(user), "nickname": user.nick_name, "range": user.range, "uid": user.id}
    else:
        return {"msg": "账户或者密码错误", "code": 401}, 401


# @request_token 要放到@app.route 下面 原理很简单 app.route（request_token（hot））
@app.route("/hot", methods=['GET'], endpoint="hot")
@request_token
def hot(user_dit):
    uid = user_dit["uid"]
    pager = int(request.args.get("p"))
    items = []
    ids = subscribeService.get_source_id(user_id=uid)
    for item in itemService.get_item_paging_by_source_ids(ids, page_index=pager):
        items.append({"item_id": item.id,
                      "title": item.title,
                      "range": item.range,
                      "content": item.content,
                      "time": item.time,
                      "source_id": item.source_id,
                      "source_name": item.source_name,
                      "source_icon": item.source_icon
                      })
    return {"items": items}


@app.route("/me", methods=['GET'], endpoint="me")
@request_token
def me(user):
    return "me"


@app.route("/find", methods=['GET'], endpoint="find")
@request_token
def find():
    items = []
    index = int(request.args.get("index"))
    for item in ItemService().get_item_paging(5, index):
        items.append({"title": item.title, "content": item.content, "time": item.time, "source_id": item.source_id,
                      "id": item.id})
    return {"items": items, "size": len(items)}


def init_jwt(user):
    return jwt.dumps(
        {'nickName': user.nick_name, 'name': user.name,
         'uid': user.id}).decode()  # python3 编码后得到 bytes, 再进行解码(指明解码的格式), 得到一个str


if __name__ == '__main__':
    init_table()
    scheduler = BackgroundScheduler()
    scheduler.add_job(crawler, 'interval', seconds=10000000)
    crawler()
    scheduler.start()
    app.run(host='0.0.0.0', port=9091, debug=True)
