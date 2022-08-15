import os


class Config:
    DB_NAME = os.environ['DB_NAME']
    MYSQL_USER = os.environ['MYSQL_USER']
    MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
    MYSQL_HOST = os.environ['MYSQL_HOST']
    MYSQL_PORT = os.environ['MYSQL_PORT']
    SQLALCHEMY_BINDS = {
        DB_NAME: f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{DB_NAME}'
    }
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_BINDS[DB_NAME]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
