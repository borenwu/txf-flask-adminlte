# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify,g
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.log.AppAccessLog import AppAccessLog
from common.models.community.Community import Community
from sqlalchemy import or_
from application import app, db

route_community = Blueprint('community_page', __name__)


@route_community.route("/index")
def index():
    print('community index')
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Community.query.filter(Community.platform_id == g.current_user.platform_id)

    if 'mix_kw' in req:
        rule = Community.name.ilike("%{0}%".format(req['mix_kw']))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Community.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    list = query.order_by(Community.id).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    if g.current_user.community_id is not None:
        return ops_render("community/leader.html")
    return ops_render("community/index.html", resp_data)


@route_community.route("/info")
def info():
    resp_data = {}
    req = request.args
    id = int(req.get('id', 0))
    reback_url = UrlManager.buildUrl("/community/index")
    if id < 1:
        return redirect(reback_url)

    info = Community.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)

    # access_list = AppAccessLog.query.filter_by(uid=uid).order_by(AppAccessLog.id.desc()).limit(10).all()
    resp_data['info'] = info
    # resp_data['access_list'] = access_list
    return ops_render("community/info.html", resp_data)


@route_community.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int(req.get("id", 0))
        info = None
        current_user = g.current_user
        if id:
            info = Community.query.filter_by(id=id).first()
        resp_data['info'] = info
        resp_data['current_user'] = current_user
        return ops_render("community/set.html", resp_data)

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    print(req)

    id = req['id'] if 'id' in req else 0
    print('id=' + id)
    name = req['name'] if 'name' in req else ''
    province = req['province'] if 'province' in req else ''
    city = req['city'] if 'city' in req else ''
    description = req['description'] if 'description' in req else ''
    pickups = req['pickups'] if 'pickups' in req else ''

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的社区名~~"
        return jsonify(resp)

    if province is None or len(province) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的省份~~"
        return jsonify(resp)

    if city is None or len(city) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的城市~~"
        return jsonify(resp)

    if description is None or len(description) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的社区简介~~"
        return jsonify(resp)

    if pickups is None or len(city) < 2:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的自提点信息~~"
        return jsonify(resp)

    has_in = Community.query.filter(Community.name == name, Community.id != id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该社区名已存在，请换一个试试~~"
        return jsonify(resp)

    community_info = Community.query.filter_by(id=id).first()
    if community_info:
        model_community = community_info
    else:
        model_community = Community()
        model_community.platform_id = g.current_user.platform_id
        model_community.platform_name = g.current_user.platform_name

    model_community.name = name
    model_community.province = province
    model_community.city = city
    model_community.description = description
    model_community.pickups = pickups

    db.session.add(model_community)
    db.session.commit()
    return jsonify(resp)


@route_community.route("/ops", methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)

    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    community_info = Community.query.filter_by(id=id).first()
    if not community_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在~~"
        return jsonify(resp)

    if act == "remove":
        community_info.status = 0
    elif act == "recover":
        community_info.status = 1

    db.session.add(community_info)
    db.session.commit()
    return jsonify(resp)
