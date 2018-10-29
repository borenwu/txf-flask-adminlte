from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.schema import FetchedValue
from application import db


class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    platform_name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    community_name = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    create_date = db.Column(db.DateTime, nullable=False)
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    wechat = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    description = db.Column(db.String(600), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
