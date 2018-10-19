from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.schema import FetchedValue
from application import db


class Platform(db.Model):
    __tablename__ = 'platform'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    province = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    city = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    description = db.Column(db.String(2000), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
