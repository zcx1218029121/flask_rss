from flask import Flask
from flask import request
from flask import make_response
from sql.user_service import UserService
# jwt
import jwt

import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    form = request.form
    user_name = form["userName"]
    pass_word = form["password"]
    user = UserService().login(user_name, pass_word)
    if user is not None:
        return user.nick_name
    else:
        return make_response(404)


@app.route("/hot", methods=['GET'])
def find():
    return "great"


@app.route("/me", methods=['GET'])
def me():
    return "me"


@app.route("/find", methods=['GET'])
def find():
    return "find"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9091, debug=True)
