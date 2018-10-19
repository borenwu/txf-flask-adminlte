# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify, g
from common.libs.Helper import ops_render
from common.models.member.Member import Member
from common.models.food.Food import Food
from common.models.community.Community import Community
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.food.FoodSaleChangeLog import FoodSaleChangeLog
from application import app, db
from common.libs.UrlManager import UrlManager
from common.libs.Helper import iPagination, selectFilterObj, getDictListFilterField, getDictFilterField, getCurrentDate
from sqlalchemy import func
from decimal import Decimal
import json
import datetime
from common.libs.Helper import getFormatDate

route_finance = Blueprint('finance_page', __name__)


@route_finance.route("/index")
def index():
    current_user = g.current_user
    resp_data = {}
    req = request.values

    community_map = {}
    communities = Community.query.filter_by(platform_id=current_user.platform_id)
    for community in communities:
        community_map[community.id] = community.name

    page = int(req['p']) if ('p' in req and req['p']) else 1

    now = datetime.datetime.now()
    today = getFormatDate(date=now, format="%Y-%m-%d")
    default_date_from = today.__str__() + " 00:00:00"
    default_date_to = today.__str__() + " 23:59:59"
    date_from = req['date_from'] + " 00:00:00" if 'date_from' in req and req['date_from'] != '' else default_date_from
    date_to = req['date_to'] + " 23:59:59" if 'date_to' in req and req['date_to'] != '' else default_date_to

    query = FoodSaleChangeLog.query.filter_by(platform_id=current_user.platform_id)
    query = query.filter(FoodSaleChangeLog.created_time >= date_from).filter(FoodSaleChangeLog.created_time <= date_to)

    if 'community_name' in req and req['community_name'] != '-1':
        print(req['community_name'])
        query = query.filter(FoodSaleChangeLog.community_name == req['community_name'])

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    food_sale_change_log_list = query.order_by(FoodSaleChangeLog.created_time.desc()).offset(offset).limit(
        app.config['PAGE_SIZE']).all()

    data_list = []
    for log in food_sale_change_log_list:
        quantity = log.quantity
        price = log.price
        temp_total = price * quantity
        total = Decimal(temp_total).quantize(Decimal('0.00'))

        member_id = log.member_id
        member = Member.query.filter_by(id=member_id).first()
        nickname = member.nickname

        food_id = log.food_id
        food = Food.query.filter_by(id=food_id).first()
        food_name = food.name

        temp_data = {
            "id":log.id,
            "created_time": log.created_time,
            "nickname": nickname,
            "community_name": log.community_name,
            "food_name": food_name,
            "price": price,
            "quantity": quantity,
            "total": total
        }
        data_list.append(temp_data)

    resp_data['communities'] = community_map
    resp_data['list'] = data_list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['current'] = 'index'

    if g.current_user.community_id is not None:
        return ops_render("finance/leader.html")
    return ops_render("finance/index.html", resp_data)


# @route_finance.route("/test/index")
# def testindex():
#     current_user = g.current_user
#     resp_data = {}
#     req = request.values
#     page = int(req['p']) if ('p' in req and req['p']) else 1
#
#     query = PayOrder.query.filter_by(platform_id=current_user.platform_id)
#
#     if 'status' in req and int(req['status']) > -1:
#         query = query.filter(PayOrder.status == int(req['status']))
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
#     pay_list = query.order_by(PayOrder.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
#     data_list = []
#     if pay_list:
#         pay_order_ids = selectFilterObj(pay_list, "id")
#         pay_order_items_map = getDictListFilterField(PayOrderItem, PayOrderItem.pay_order_id, "pay_order_id",
#                                                      pay_order_ids)
#
#         food_mapping = {}
#         if pay_order_items_map:
#             food_ids = []
#             for item in pay_order_items_map:
#                 tmp_food_ids = selectFilterObj(pay_order_items_map[item], "food_id")
#                 tmp_food_ids = {}.fromkeys(tmp_food_ids).keys()
#                 food_ids = food_ids + list(tmp_food_ids)
#
#             # food_ids里面会有重复的，要去重
#             food_mapping = getDictFilterField(Food, Food.id, "id", food_ids)
#
#         for item in pay_list:
#             tmp_data = {
#                 "id": item.id,
#                 "status_desc": item.status_desc,
#                 "order_number": item.order_number,
#                 "price": item.total_price,
#                 "pay_time": item.pay_time,
#                 "created_time": item.created_time.strftime("%Y%m%d%H%M%S")
#             }
#             tmp_foods = []
#             tmp_order_items = pay_order_items_map[item.id]
#             for tmp_order_item in tmp_order_items:
#                 tmp_food_info = food_mapping[tmp_order_item.food_id]
#                 tmp_foods.append({
#                     'community_name': tmp_order_item.community_name,
#                     'name': tmp_food_info.name,
#                     'quantity': tmp_order_item.quantity
#                 })
#
#             tmp_data['foods'] = tmp_foods
#             data_list.append(tmp_data)
#
#     resp_data['list'] = data_list
#     resp_data['pages'] = pages
#     resp_data['search_con'] = req
#     resp_data['pay_status_mapping'] = app.config['PAY_STATUS_MAPPING']
#     resp_data['current'] = 'index'
#
#     print(resp_data)
#
#     if g.current_user.community_id is not None:
#         return ops_render("finance/leader.html")
#     return ops_render("finance/index.html", resp_data)


@route_finance.route("/pay-info")
def info():
    resp_data = {}
    req = request.values
    id = int(req['id']) if 'id' in req else 0

    reback_url = UrlManager.buildUrl("/finance/index")

    if id < 1:
        return redirect(reback_url)

    food_sale_change_log = FoodSaleChangeLog.query.filter_by(id=id).first()
    if not food_sale_change_log:
        return redirect(reback_url)

    member_info = Member.query.filter_by(id=food_sale_change_log.member_id).first()
    if not member_info:
        return redirect(reback_url)

    pay_order_item = PayOrderItem.query.filter_by(id=food_sale_change_log.pay_order_item_id).first()
    pay_order_id = pay_order_item.pay_order_id
    pay_order = PayOrder.query.filter_by(id=pay_order_id).first()
    address_info = json.loads(pay_order.express_info)

    resp_data['pay_order_info'] = pay_order
    resp_data['member_info'] = member_info
    resp_data['address_info'] = address_info
    resp_data['current'] = 'index'
    return ops_render("finance/pay_info.html", resp_data)


@route_finance.route("/account")
def set():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = PayOrder.query.filter_by(status=1)

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    list = query.order_by(PayOrder.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()

    stat_info = db.session.query(PayOrder, func.sum(PayOrder.total_price).label("total")) \
        .filter(PayOrder.status == 1).first()

    app.logger.info(stat_info)
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['total_money'] = stat_info[1] if stat_info[1] else 0.00
    resp_data['current'] = 'account'
    return ops_render("finance/account.html", resp_data)


@route_finance.route("/ops", methods=["POST"])
def orderOps():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    pay_order_info = PayOrder.query.filter_by(id=id).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙。请稍后再试~~"
        return jsonify(resp)

    if act == "express":
        pay_order_info.express_status = -6
        pay_order_info.updated_time = getCurrentDate()
        db.session.add(pay_order_info)
        db.session.commit()

    return jsonify(resp)
