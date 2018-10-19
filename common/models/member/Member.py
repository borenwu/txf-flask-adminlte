# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db,app

# `community_name` varchar(20) NOT NULL DEFAULT '' COMMENT '社区名',
class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    community_id = db.Column(db.Integer, nullable=True, server_default=db.FetchedValue())
    community_name = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    avatar = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    reg_ip = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    @property
    def status_desc(self):
        return app.config['STATUS_MAPPING'][ str( self.status ) ]

    @property
    def sex_desc(self):
        sex_mapping = {
            "0":"未知",
            "1":"男",
            "2":"女"
        }
        return sex_mapping[str(self.sex)]