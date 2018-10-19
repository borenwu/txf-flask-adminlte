# -*- coding: utf-8 -*-
from web.controllers.api import route_api
from flask import request, jsonify, g
from common.models.food.FoodCat import FoodCat
from common.models.food.Food import Food
from common.models.member.MemberCart import MemberCart
from common.models.member.MemberComments import MemberComments
from common.models.member.Member import Member
from common.libs.UrlManager import UrlManager
from common.libs.Helper import getCurrentDate, getDictFilterField, selectFilterObj
from application import app, db
from sqlalchemy import or_
from common.libs.Helper import getFormatDate
import datetime


@route_api.route("/food/index")
def foodIndex():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    platform_id = int(req['platform_id']) if 'platform_id' in req else 0
    community_name = req['community_name'] if 'community_name' in req else ''
    cat_list = FoodCat.query.filter_by(status=1).order_by(FoodCat.weight.desc()).all()
    data_cat_list = []
    data_cat_list.append({
        'id': 0,
        'name': "全部"
    })
    if cat_list:
        for item in cat_list:
            tmp_data = {
                'id': item.id,
                'name': item.name
            }
            data_cat_list.append(tmp_data)
    resp['data']['cat_list'] = data_cat_list

    rule = Food.communities.ilike("%{0}%".format(community_name))
    now = datetime.datetime.now()
    today = getFormatDate(date=now)
    query = Food.query.filter_by(status=1, platform_id=platform_id).filter(Food.date_from <= today).filter(
        Food.date_to >= today)
    food_list = query.filter(rule).order_by(Food.total_count.desc(), Food.id.desc()).limit(3).all()

    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'pic_url': item.main_image
            }
            data_food_list.append(tmp_data)

    resp['data']['banner_list'] = data_food_list
    return jsonify(resp)


@route_api.route("/food/search")
def foodSearch():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    platform_id = int(req['platform_id']) if 'platform_id' in req else 0
    community_name = req['community_name'] if 'community_name' in req else ''
    cat_id = int(req['cat_id']) if 'cat_id' in req else 0
    mix_kw = str(req['mix_kw']) if 'mix_kw' in req else ''
    p = int(req['p']) if 'p' in req else 1

    if p < 1:
        p = 1
    # print(p)

    page_size = 10
    offset = (p - 1) * page_size
    # print(offset)

    print(community_name)
    rule = Food.communities.ilike("%{0}%".format(community_name))
    now = datetime.datetime.now()
    today = getFormatDate(date=now)
    query = Food.query.filter_by(status=1, platform_id=platform_id).filter(Food.date_from <= today).filter(
        Food.date_to >= today).filter(rule)
    print(query.all())

    if cat_id > 0:
        query = query.filter_by(cat_id=cat_id)

    if mix_kw:
        rule = or_(Food.name.ilike("%{0}%".format(mix_kw)), Food.tags.ilike("%{0}%".format(mix_kw)))
        query = query.filter(rule)

    food_list = query.order_by(Food.total_count.desc(), Food.id.desc()).all()
    print(food_list)

    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'name': "%s" % (item.name),
                'price': str(item.price),
                'market_price': str(item.market_price),
                'date_to': str(item.date_to),
                'pic_url': item.main_image,
                'stock': item.stock,
                'limit_quantity': item.limit_quantity
            }
            data_food_list.append(tmp_data)
    resp['data']['list'] = data_food_list
    resp['data']['has_more'] = 0 if len(data_food_list) < page_size else 1
    return jsonify(resp)


@route_api.route("/food/info")
def foodInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0
    food_info = Food.query.filter_by(id=id).first()
    if not food_info or not food_info.status:
        resp['code'] = -1
        resp['msg'] = "美食已下架"
        return jsonify(resp)

    member_info = g.member_info
    cart_number = 0
    if member_info:
        cart_number = MemberCart.query.filter_by(member_id=member_info.id).count()
    resp['data']['info'] = {
        "id": food_info.id,
        "name": food_info.name,
        "summary": food_info.summary,
        "total_count": food_info.total_count,
        "comment_count": food_info.comment_count,
        'main_image': food_info.main_image,
        "price": str(food_info.price),
        "stock": food_info.stock,
        "limit_quantity":food_info.limit_quantity,
        "pics": [food_info.main_image]
    }
    resp['data']['cart_number'] = cart_number
    return jsonify(resp)


@route_api.route("/food/comments")
def foodComments():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0
    query = MemberComments.query.filter(MemberComments.food_ids.ilike("%_{0}_%".format(id)))
    list = query.order_by(MemberComments.id.desc()).limit(5).all()
    data_list = []
    if list:
        member_map = getDictFilterField(Member, Member.id, "id", selectFilterObj(list, "member_id"))
        for item in list:
            if item.member_id not in member_map:
                continue
            tmp_member_info = member_map[item.member_id]
            tmp_data = {
                'score': item.score_desc,
                'date': item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                "content": item.content,
                "user": {
                    'nickname': tmp_member_info.nickname,
                    'avatar_url': tmp_member_info.avatar,
                }
            }
            data_list.append(tmp_data)
    resp['data']['list'] = data_list
    resp['data']['count'] = query.count()
    return jsonify(resp)
