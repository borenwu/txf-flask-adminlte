# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from application import  db


class CommunityChangeLog(db.Model):
    __tablename__ = 'community_change_log'

    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, nullable=False)
    platform_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    platform_name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    community_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    community_name = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    new_community_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    new_community_name = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    wechat = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    description = db.Column(db.String(600), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())