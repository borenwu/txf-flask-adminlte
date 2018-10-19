# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, Numeric
from sqlalchemy.schema import FetchedValue
from application import db


class FoodSaleChangeLog(db.Model):
    __tablename__ = 'food_sale_change_log'

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    community_id = db.Column(db.Integer, nullable=True, server_default=db.FetchedValue())
    community_name = db.Column(db.String(100), nullable=True, server_default=db.FetchedValue())
    pay_order_item_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    food_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    quantity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    benefit = db.Column(db.Numeric(10, 2), server_default=db.FetchedValue())
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
