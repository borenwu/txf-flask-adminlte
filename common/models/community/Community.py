from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.schema import FetchedValue
from application import db


class Community(db.Model):
    __tablename__ = 'community'

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    platform_name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    province = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    city = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    description = db.Column(db.String(2000), nullable=False, server_default=db.FetchedValue())
    pickups = db.Column(db.String(2000), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())


