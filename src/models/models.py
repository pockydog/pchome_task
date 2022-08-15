from sqlalchemy import func
from app import db


class Product(db.Model):
    __bind__ = 'productdb'
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500), nullable=False, comment='商品名稱')
    price = db.Column(db.Integer, nullable=False, comment='定價')
    code = db.Column(db.String(100), nullable=False, comment='商品代號')
    pic_url = db.Column(db.String(1000), comment='圖片url')
    type = db.Column(db.String(100), nullable=False, comment='商品分類')
    create_datetime = db.Column(db.DateTime, server_default=func.now())
    update_datetime = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


