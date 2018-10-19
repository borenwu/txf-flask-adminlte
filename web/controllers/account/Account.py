# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify, g
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.log.AppAccessLog import AppAccessLog
from common.models.User import User
from common.models.community.Community import Community
from decimal import Decimal
from sqlalchemy import or_
from application import app, db


route_account = Blueprint('account_page', __name__)


@route_account.route("/index")
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = User.query.filter(User.platform_id == g.current_user.platform_id)

    if 'mix_kw' in req:
        rule = or_(User.nickname.ilike("%{0}%".format(req['mix_kw'])), User.mobile.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == int(req['status']))

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

    list = query.order_by(User.uid).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    if g.current_user.community_id is not None:
        return ops_render("account/leader.html")
    return ops_render("account/index.html", resp_data)


@route_account.route("/info")
def info():
    resp_data = {}
    req = request.args
    uid = int(req.get('id', 0))
    reback_url = UrlManager.buildUrl("/account/index")
    if uid < 1:
        return redirect(reback_url)

    info = User.query.filter_by(uid=uid).first()
    if not info:
        return redirect(reback_url)

    access_list = AppAccessLog.query.filter_by(uid=uid).order_by(AppAccessLog.id.desc()).limit(10).all()
    resp_data['info'] = info
    resp_data['access_list'] = access_list
    return ops_render("account/info.html", resp_data)


@route_account.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        uid = int(req.get("id", 0))
        info = None
        if uid:
            info = User.query.filter_by(uid=uid).first()
        current_user = g.current_user
        communities = Community.query.filter(Community.platform_id == current_user.platform_id)
        resp_data['info'] = info
        resp_data['communities'] = communities
        return ops_render("account/set.html", resp_data)

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    platform_id = req['platform_id'] if 'platform_id' in req else ''
    platform_name = req['platform_name'] if 'platform_name' in req else ''
    community_id = req['community_id'] if 'community_id' in req else ''
    community_name = req['community_name'] if 'community_name' in req else ''
    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    email = req['email'] if 'email' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    benefit = req['benefit'] if 'benefit' in req else 0

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~~"
        return jsonify(resp)

    if mobile is None or len(mobile) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的手机号码~~"
        return jsonify(resp)

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录用户名~~"
        return jsonify(resp)

    if login_pwd is None or len(login_pwd) < 3:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录密码~~"
        return jsonify(resp)

    has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该登录名已存在，请换一个试试~~"
        return jsonify(resp)

    benefit = Decimal(benefit).quantize(Decimal('0.00'))
    if benefit < 0:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的售卖价格~~"
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()
    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.platform_id = platform_id
        model_user.platform_name = platform_name
        model_user.community_id = community_id
        model_user.community_name = community_name
        model_user.email = email
        model_user.benefit = 0.00
        model_user.created_time = getCurrentDate()
        model_user.login_salt = UserService.geneSalt()

    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.login_name = login_name
    model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
    model_user.benefit = benefit

    model_user.updated_time = getCurrentDate()
    db.session.add(model_user)
    db.session.commit()
    return jsonify(resp)


@route_account.route("/ops", methods=["POST"])
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

    user_info = User.query.filter_by(uid=id).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在~~"
        return jsonify(resp)

    if act == "remove":
        user_info.status = 0
    elif act == "recover":
        user_info.status = 1

    user_info.update_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)
