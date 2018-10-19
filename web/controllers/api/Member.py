# -*- coding: utf-8 -*-
from web.controllers.api import route_api
from flask import request, jsonify, g
from application import app, db
import requests, json
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.models.food.WxShareHistory import WxShareHistory
from common.models.community.Community import Community
from common.models.community.Platform import Platform
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.food.FoodSaleChangeLog import FoodSaleChangeLog
from common.models.food.Food import Food
from common.libs.Helper import getCurrentDate
from common.libs.member.MemberService import MemberService


@route_api.route("/member/orderlogs", methods=["POST"])
def getOrderLogs():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    platform_id = req['platform_id'] if 'platform_id' in req else 0
    community_id = req['community_id'] if 'community_id' in req else 0
    if not platform_id or platform_id == 0:
        resp['code'] = -1
        resp['msg'] = "需要platform_id"
        return jsonify(resp)

    if not community_id or community_id == 0:
        resp['code'] = -1
        resp['msg'] = "community_id"
        return jsonify(resp)

    order_list = []
    order_items = FoodSaleChangeLog.query.filter_by(platform_id=platform_id, community_id=community_id).order_by(
        FoodSaleChangeLog.created_time.desc()).limit(
        50).all()
    for item in order_items:
        member = Member.query.filter_by(platform_id=platform_id, id=item.member_id).first()
        nickname = member.nickname
        avatar = member.avatar
        food = Food.query.filter_by(platform_id=platform_id, id=item.food_id).first()
        food_name = food.name
        temp_data = {
            'updated_time': item.created_time.__str__(),
            'avatar': avatar,
            'nickname': nickname,
            'food_name': food_name,
            'quantity': item.quantity
        }
        order_list.append(temp_data)
    resp['data']['order_list'] = order_list
    return jsonify(resp)


@route_api.route("/member/communities", methods=["POST"])
def getCommunities():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    platform_id = req['platform_id'] if 'platform_id' in req else 0
    if not platform_id or platform_id == 0:
        resp['code'] = -1
        resp['msg'] = "需要platform_id"
        return jsonify(resp)

    communities = Community.query.filter(Community.platform_id == platform_id).filter_by(status=1).all()
    community_list = []

    for community in communities:
        tmp_data = {
            'community_id': community.id,
            'community_name': community.name
        }
        community_list.append(tmp_data)
    resp['data']['communities'] = community_list
    return jsonify(resp)


@route_api.route("/member/login", methods=["GET", "POST"])
def login():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    platform_id = int(req['platform_id']) if 'platform_id' in req and req['platform_id'] else 0
    community_id = int(req['community_id']) if 'community_id' in req and req['community_id'] else 0
    community_name = req['community_name'] if 'community_name' in req else ''
    stamp = req['stamp'] if 'stamp' in req else None

    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return jsonify(resp)
    print(code)
    openid = MemberService.getWeChatOpenId(code, stamp=stamp)
    print(openid)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    '''
        判断是否已经测试过，注册了直接返回一些信息
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = nickname
        model_member.platform_id = platform_id
        model_member.community_id = community_id
        model_member.community_name = community_name
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {
        'token': token,
        'id': member_info.id,
        'platform_id': member_info.platform_id
    }
    return jsonify(resp)


@route_api.route("/member/change-community", methods=["POST"])
def changeCommunity():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    member_id = int(req['member_id']) if 'member_id' in req and req['member_id'] else 0
    platform_id = int(req['platform_id']) if 'platform_id' in req and req['platform_id'] else 0
    community_id = int(req['community_id']) if 'community_id' in req and req['community_id'] else 0
    community_name = req['community_name'] if 'community_name' in req else ''

    try:
        member_info = Member.query.filter_by(id=member_id, platform_id=platform_id).first()
        print(member_info)
        member_info.community_id = community_id
        member_info.community_name = community_name

        g.member_info = member_info
        db.session.add(member_info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        resp['code'] = -1
        resp['msg'] = "修改社区失败失败"
        resp['msg'] = str(e)
        return jsonify(resp)
    return jsonify(resp)


@route_api.route("/member/check-reg", methods=["GET", "POST"])
def checkReg():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    stamp = req['stamp'] if 'stamp' in req else None

    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code, stamp=stamp)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = "未绑定"
        return jsonify(resp)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "未查询到绑定信息"
        return jsonify(resp)

    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {
        'token': token,
        'platform_id': member_info.platform_id,
        'member_id': member_info.id,
        'community_id': member_info.community_id,
        'community_name': member_info.community_name
    }
    return jsonify(resp)


@route_api.route("/member/share", methods=["POST"])
def memberShare():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    url = req['url'] if 'url' in req else ''
    member_info = g.member_info
    model_share = WxShareHistory()
    if member_info:
        model_share.member_id = member_info.id
    model_share.share_url = url
    model_share.created_time = getCurrentDate()
    db.session.add(model_share)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/member/info")
def memberInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    resp['data']['info'] = {
        "nickname": member_info.nickname,
        "avatar_url": member_info.avatar
    }
    return jsonify(resp)


@route_api.route("/member/check-limit")
def checkLimit():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    member_id = int(req['member_id']) if 'member_id' in req and req['member_id'] else 0
    food_id = int(req['food_id']) if 'food_id' in req and req['food_id'] else 0
    food = Food.query.filter_by(id=food_id).first()
    if food.limit_quantity == 0:
        return jsonify(resp)
    else:
        date_from = food.date_from.__str__() + " 00:00:00"
        date_to = food.date_to.__str__() + " 23:59:59"
        sale_change_log = FoodSaleChangeLog \
            .query.filter_by(food_id=food.id, member_id=member_id) \
            .filter(FoodSaleChangeLog.created_time >= date_from) \
            .filter(FoodSaleChangeLog.created_time <= date_to).all()
        if len(sale_change_log) > 0:
            resp['code'] = -1
            resp['msg'] = "已经购买过一次了，不能再次购买限购商品"
            return jsonify(resp)
        else:
            return jsonify(resp)
