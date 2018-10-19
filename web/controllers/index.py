# -*- coding: utf-8 -*-
from application import app, db
from flask import Blueprint, g, request, redirect
from common.libs.UrlManager import UrlManager
from common.libs.Helper import ops_render
from common.libs.Helper import getFormatDate
from common.models.stat.StatDailySite import StatDailySite
from common.models.food.Food import Food
from common.models.food.FoodSaleChangeLog import FoodSaleChangeLog
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.pay.PayOrder import PayOrder
from sqlalchemy import func
from decimal import Decimal
import json
import calendar
import time

import datetime

route_index = Blueprint('index_page', __name__)


@route_index.route("/")
def index():
    resp_data = {
        'data': {
            'finance': {
                'today': 0,
                'month': 0
            },
            'member': {
                'today_new': 0,
                'month_new': 0,
                'total': 0
            },
            'order': {
                'today': 0,
                'month': 0
            },
            'shared': {
                'today': 0,
                'month': 0
            },
        }
    }

    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    date_before_3days = now + datetime.timedelta(days=-3)
    date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    threshold = getFormatDate(date=date_before_3days)
    date_to = getFormatDate(date=now, format="%Y-%m-%d")
    today = getFormatDate(date=now, format="%Y-%m-%d")

    food_list_opening = Food.query.filter_by(platform_id=g.current_user.platform_id,status=1).filter(
        Food.date_to >= threshold).order_by(Food.date_from.desc()).all()
    resp_data['food_list_opening'] = food_list_opening

    # list = StatDailySite.query.filter(StatDailySite.date >= date_from) \
    #     .filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc()) \
    #     .all()
    # data = resp_data['data']
    # if list:
    #
    #     for item in list:
    #         data['finance']['month'] += item.total_pay_money
    #         data['member']['month_new'] += item.total_new_member_count
    #         data['member']['total'] = item.total_member_count
    #         data['order']['month'] += item.total_order_count
    #         data['shared']['month'] += item.total_shared_count
    #         if getFormatDate(date=item.date, format="%Y-%m-%d") == date_to:
    #             data['finance']['today'] = item.total_pay_money
    #             data['member']['today_new'] = item.total_new_member_count
    #             data['order']['today'] = item.total_order_count
    #             data['shared']['today'] = item.total_shared_count

    if g.current_user.community_id is not None:
        day_now = time.localtime()
        day_begin = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)  # 月初肯定是1号
        wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
        day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)
        date_month_begin = day_begin.__str__() + " 00:00:00"
        date_month_end = day_end.__str__() + " 23:59:59"

        sum_quantity_month = 0
        sum_sale_month = 0
        sum_benefit_month = 0

        sale_change_logs = FoodSaleChangeLog.query.filter_by(platform_id=g.current_user.platform_id,
                                                             community_id=g.current_user.community_id) \
            .filter(FoodSaleChangeLog.created_time >= date_month_begin) \
            .filter(FoodSaleChangeLog.created_time <= date_month_end)

        for log in sale_change_logs:
            sum_quantity_month = sum_quantity_month + log.quantity
            temp_sale = log.price * log.quantity
            sale = Decimal(temp_sale).quantize(Decimal('0.00'))
            sum_sale_month = sum_sale_month + sale
            sum_benefit_month = sum_benefit_month + log.benefit

        date_from = today.__str__() + " 00:00:00"
        date_to = today.__str__() + " 23:59:59"

        sum_quantity_today = 0
        sum_sale_today = 0
        sum_benefit_today = 0
        sale_change_logs = FoodSaleChangeLog.query.filter_by(platform_id=g.current_user.platform_id,
                                                             community_id=g.current_user.community_id) \
            .filter(FoodSaleChangeLog.created_time >= date_from) \
            .filter(FoodSaleChangeLog.created_time <= date_to)

        for log in sale_change_logs:
            sum_quantity_today = sum_quantity_today + log.quantity
            temp_sale = log.price * log.quantity
            sale = Decimal(temp_sale).quantize(Decimal('0.00'))
            sum_sale_today = sum_sale_today + sale
            sum_benefit_today = sum_benefit_today + log.benefit

        stat_list = []
        rule = Food.communities.ilike("%{0}%".format(g.current_user.community_name))
        foods = Food.query.filter_by(status=1).filter(rule).order_by(Food.date_from.desc()).all()
        for food in foods:
            temp_data = {
                "food_id": food.id,
                "food_name": food.name,
                "date_from": food.date_from,
                "date_to": food.date_to,
                "price": food.price,
                "ratio": food.ratio
            }
            stat_list.append(temp_data)

        # rs = db.session.query(FoodSaleChangeLog.food_id, func.sum(FoodSaleChangeLog.quantity)).filter_by(
        #     platform_id=g.current_user.platform_id, community_id=g.current_user.community_id).group_by(
        #     FoodSaleChangeLog.food_id).all()
        # print(rs)
        # stat_list = []
        # for row in rs:
        #     temp_data = {}
        #     food = Food.query.filter_by(platform_id=g.current_user.platform_id, id=row[0]).first()
        #     food_name = food.name
        #     temp_data['food_id'] = row[0]
        #     temp_data['food_name'] = food_name
        #     temp_data['quantity'] = row[1].__str__()
        #     stat_list.append(temp_data)

        resp_data['sum_quantity_month'] = sum_quantity_month
        resp_data['sum_sale_month'] = sum_sale_month
        resp_data['sum_benefit_month'] = sum_benefit_month

        resp_data['sum_quantity_today'] = sum_quantity_today
        resp_data['sum_sale_today'] = sum_sale_today
        resp_data['sum_benefit_today'] = sum_benefit_today

        resp_data['stat_list'] = stat_list
        return ops_render("index/leader.html", resp_data)

    return ops_render("index/index.html", resp_data)


@route_index.route("/food-info")
def getFoodInfo():
    resp_data = {}
    req = request.args
    food_id = int(req.get('id', 0))
    print(food_id)
    reback_url = UrlManager.buildUrl("/")
    if food_id < 1:
        return redirect(reback_url)

    # food_info = FoodSaleChangeLog.query.filter_by(id=food_id).all()
    food = Food.query.filter_by(id=food_id).first()
    date_from = food.date_from.__str__()
    print(date_from)
    date_to = food.date_to.__str__()
    print(date_to)
    rs = db.session.query(FoodSaleChangeLog.community_name, func.sum(FoodSaleChangeLog.quantity)).filter_by(
        food_id=food_id).filter(FoodSaleChangeLog.created_time >= date_from).filter(
        FoodSaleChangeLog.created_time <= date_to).group_by(FoodSaleChangeLog.community_name).all()

    print(rs)

    sum_quantity = 0
    stat_list = []
    for row in rs:
        sum_quantity = sum_quantity + row[1]
        temp_data = {}
        temp_data['community_name'] = row[0]
        temp_data['quantity'] = row[1].__str__()
        stat_list.append(temp_data)

    if not rs:
        return redirect(reback_url)

    resp_data['sum_quantity'] = sum_quantity
    resp_data['stat_list'] = stat_list
    return ops_render("index/info.html", resp_data)


@route_index.route("/leader-food-info")
def getLeaderFoodInfo():
    resp_data = {}
    req = request.args
    food_id = int(req.get('id', 0))
    reback_url = UrlManager.buildUrl("/")
    print(food_id)

    if food_id < 1:
        return redirect(reback_url)

    # food_info = FoodSaleChangeLog.query.filter_by(id=food_id).all()
    current_user = g.current_user
    food = Food.query.filter_by(id=food_id).first()
    date_from = food.date_from.__str__() + " 00:00:00"
    date_to = food.date_to.__str__() + " 23:59:59"
    sale_change_logs = FoodSaleChangeLog \
        .query.filter_by(food_id=food.id, platform_id=current_user.platform_id, community_id=current_user.community_id) \
        .filter(FoodSaleChangeLog.created_time >= date_from) \
        .filter(FoodSaleChangeLog.created_time <= date_to).all()
    # rs = db.session.query(FoodSaleChangeLog.community_name, func.sum(FoodSaleChangeLog.quantity)).filter_by(
    #     food_id=food_id).filter(FoodSaleChangeLog.created_time >= date_from).filter(
    #     FoodSaleChangeLog.created_time <= date_to).group_by(FoodSaleChangeLog.community_name).all()
    print(sale_change_logs)
    sum_quantity = 0
    sum_sale = 0
    sum_benefit = 0
    order_list = []
    for row in sale_change_logs:
        sum_quantity = sum_quantity + row.quantity
        temp_sale = row.price * row.quantity
        sale = Decimal(temp_sale).quantize(Decimal('0.00'))
        sum_sale = sum_sale + sale
        sum_benefit = sum_benefit + row.benefit

        pay_order_item = PayOrderItem.query.filter_by(id=row.pay_order_item_id).first()
        pay_order_id = pay_order_item.pay_order_id
        pay_order = PayOrder.query.filter_by(id=pay_order_id).first()
        address_info = json.loads(pay_order.express_info)

        temp_data = {
            "food_name": food.name,
            "created_time": row.created_time,
            "quantity": row.quantity,
            "nickname": address_info['nickname'],
            "mobile": address_info['mobile'],
            "address": address_info['address']
        }
        order_list.append(temp_data)

    if not sale_change_logs:
        return redirect(reback_url)

    resp_data['sum_quantity'] = sum_quantity
    resp_data['sum_sale'] = sum_sale
    resp_data['sum_benefit'] = sum_benefit
    resp_data['order_list'] = order_list
    return ops_render("index/leader-info.html", resp_data)
