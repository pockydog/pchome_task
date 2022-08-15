from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Flask


app = Flask(__name__)
# 設定資料庫位置，並建立 app
config = Config()
app.config.from_object(config)
config = app.config

# 從config拿資料
db = SQLAlchemy(app)


def create_app():
    return app
