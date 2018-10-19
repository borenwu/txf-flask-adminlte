# -*- coding: utf-8 -*-
from flask import Blueprint, request, g
from application import db
from common.libs.Helper import ops_render
from application import app
from common.libs.Helper import getFormatDate, iPagination, getDictFilterField, selectFilterObj
from common.models.community.Community import Community
from common.models.stat.StatDailySite import StatDailySite
from common.models.stat.StatDailyFood import StatDailyFood
from common.models.stat.StatDailyMember import StatDailyMember
from common.models.member.Member import Member
from common.models.food.Food import Food
from common.models.food.FoodSaleChangeLog import FoodSaleChangeLog
import datetime
from decimal import Decimal
from sqlalchemy import func,distinct
import operator

route_stat = Blueprint('stat_page', __name__)


@route_stat.route("/index")
def index():
    resp_data = {}
    current_user = g.current_user
    data_list = []

    communities = Community.query.filter_by(platform_id=current_user.platform_id).all()

    for community in communities:
        rs = db.session.query(Member.community_name, func.count(Member.id)).filter_by(community_id=community.id).first()


        temp_data = {
            "id": community.id,
            "community_name": rs[0],
            "member_count": rs[1]
        }
        data_list.append(temp_data)

    resp_data['list'] = data_list
    resp_data['current'] = 'index'
    return ops_render("stat/index.html", resp_data)


@route_stat.route("/community-info")
def community_info():
    resp_data = {}
    data_list = []
    current_user = g.current_user
    req = request.values
    community_id = int(req['id']) if ('id' in req and req['id']) else 0
    member_count = int(req['member_count']) if ('member_count' in req and req['member_count']) else 0

    rs = db.session.query(FoodSaleChangeLog.food_id, func.count(distinct(FoodSaleChangeLog.member_id))).filter_by(
        community_id=community_id).group_by(FoodSaleChangeLog.food_id).order_by(FoodSaleChangeLog.created_time.desc()).all()
    for row in rs:
        food_id = row[0]
        food_name = Food.query.filter_by(id=food_id).first().name
        order_count = row[1]
        temp_ratio = order_count / member_count
        ratio = Decimal(temp_ratio).quantize(Decimal('0.00'))


        temp_data = {
            "food_name":food_name,
            "order_count":order_count,
            "member_count":member_count,
            "ratio":ratio
        }
        data_list.append(temp_data)

    sorted_data_list = sorted(data_list, key=operator.itemgetter('ratio'), reverse=True)
    community_name = Community.query.filter_by(id=community_id).first().name

    resp_data["list"] = sorted_data_list
    resp_data["community_name"] = community_name
    return ops_render("stat/community-info.html", resp_data)


# @route_stat.route("/test-index")
# def test_index():
#     now = datetime.datetime.now()
#     date_before_30days = now + datetime.timedelta(days=-30)
#     default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
#     default_date_to = getFormatDate(date=now, format="%Y-%m-%d")
#
#     resp_data = {}
#     req = request.values
#     page = int(req['p']) if ('p' in req and req['p']) else 1
#     date_from = req['date_from'] if 'date_from' in req else default_date_from
#     date_to = req['date_to'] if 'date_to' in req else default_date_to
#     query = StatDailySite.query.filter(StatDailySite.date >= date_from).filter(StatDailySite.date <= date_to)
#
#     page_params = {
#         'total': query.count(),
#         'page_size': app.config['PAGE_SIZE'],
#         'page': page,
#         'display': app.config['PAGE_DISPLAY'],
#         'url': request.full_path.replace("&p={}".format(page), "")
#     }
#
#     pages = iPagination(page_params)
#     offset = (page - 1) * app.config['PAGE_SIZE']
#
#     list = query.order_by(StatDailySite.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
#     resp_data['list'] = list
#     resp_data['pages'] = pages
#     resp_data['current'] = 'index'
#     resp_data['search_con'] = {
#         'date_from': date_from,
#         'date_to': date_to
#     }
#     if g.current_user.community_id is not None:
#         return ops_render("stat/leader.html")
#     return ops_render("stat/index.html", resp_data)


@route_stat.route("/food")
def food():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to
    query = StatDailyFood.query.filter(StatDailyFood.date >= date_from) \
        .filter(StatDailyFood.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    list = query.order_by(StatDailyFood.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    date_list = []
    if list:
        food_map = getDictFilterField(Food, Food.id, "id", selectFilterObj(list, "food_id"))
        for item in list:
            tmp_food_info = food_map[item.food_id] if item.food_id in food_map else {}
            tmp_data = {
                "date": item.date,
                "total_count": item.total_count,
                "total_pay_money": item.total_pay_money,
                'food_info': tmp_food_info
            }
            date_list.append(tmp_data)

    resp_data['list'] = date_list
    resp_data['pages'] = pages
    resp_data['current'] = 'food'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render("stat/food.html", resp_data)


@route_stat.route("/member")
def memebr():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to
    query = StatDailyMember.query.filter(StatDailyMember.date >= date_from) \
        .filter(StatDailyMember.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    list = query.order_by(StatDailyMember.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    date_list = []
    if list:
        member_map = getDictFilterField(Member, Member.id, "id", selectFilterObj(list, "member_id"))
        for item in list:
            tmp_member_info = member_map[item.member_id] if item.member_id in member_map else {}
            tmp_data = {
                "date": item.date,
                "total_pay_money": item.total_pay_money,
                "total_shared_count": item.total_shared_count,
                'member_info': tmp_member_info
            }
            date_list.append(tmp_data)

    resp_data['list'] = date_list
    resp_data['pages'] = pages
    resp_data['current'] = 'member'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render("stat/member.html", resp_data)


@route_stat.route("/share")
def share():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to
    query = StatDailySite.query.filter(StatDailySite.date >= date_from) \
        .filter(StatDailySite.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    list = query.order_by(StatDailySite.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['current'] = 'share'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render("stat/share.html", resp_data)
