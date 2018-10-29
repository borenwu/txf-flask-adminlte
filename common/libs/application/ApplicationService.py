# -*- coding: utf-8 -*-
from application import app, db
from common.models.member.Member import Member
from common.libs.Helper import getCurrentDate


class ApplicationService():

    @staticmethod
    def changeCommunity(platform_id, member_id, community_id, community_name):
        member = Member.query.filter_by(platform_id=platform_id,id=member_id).first()
        member.community_id = community_id
        member.community_name = community_name
        db.session.add(member)
        db.session.commit()
        return True
