from flask import Blueprint, request, redirect, jsonify, g
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.libs.application.ApplicationService import ApplicationService
from common.models.User import User
from common.models.application.Application import Application
from common.models.log.CommunityChangeLog import CommunityChangeLog
from common.models.community.Community import Community
from common.models.User import User
from common.models.member.Member import Member
from decimal import Decimal
from sqlalchemy import or_
from application import app, db

route_application = Blueprint('application_page', __name__)


@route_application.route("/group_application")
def groupApplication():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Application.query.filter(Application.platform_id == g.current_user.platform_id).filter(
        Application.type == '入群')

    if 'application_status' in req and int(req['application_status']) > -1:
        query = query.filter(Application.status == int(req['application_status']))

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

    list = query.order_by(Application.create_date.desc()).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['application_status_mapping'] = app.config['APPLICATION_STATUS_MAPPING']
    resp_data['current'] = 'group'
    if g.current_user.community_id is not None:
        return ops_render("application/leader.html")
    return ops_render("application/group_application.html", resp_data)


@route_application.route("/group_application/approve", methods=['POST'])
def groupApplicationApprove():
    resp = {'code': 200, 'msg': '审核操作成功~~', 'data': {}}
    print(request)
    req = request.values
    id = int(req['id']) if 'id' in req and req['id'] else 0
    application = Application.query.filter(Application.id == id).first()
    application.status = 1
    db.session.add(application)
    db.session.commit()
    return jsonify(resp)


@route_application.route("/leader_application")
def leaderApplication():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Application.query.filter(Application.platform_id == g.current_user.platform_id).filter(
        Application.type == '团长')

    if 'application_status' in req and int(req['application_status']) > -1:
        query = query.filter(Application.status == int(req['application_status']))

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

    list = query.order_by(Application.create_date.desc()).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['application_status_mapping'] = app.config['APPLICATION_STATUS_MAPPING']
    resp_data['current'] = 'leader'
    if g.current_user.community_id is not None:
        return ops_render("application/leader.html")
    return ops_render("application/leader_application.html", resp_data)


@route_application.route("/leader_application/info")
def info():
    resp_data = {}
    req = request.args
    id = int(req.get('app_id', 0))
    reback_url = UrlManager.buildUrl("/leader_application")
    if id < 1:
        return redirect(reback_url)

    info = Application.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)

    resp_data['info'] = info
    resp_data['current_user'] = g.current_user
    return ops_render("application/leader_application_info.html", resp_data)


@route_application.route("/leader_application/approve", methods=['POST'])
def leaderApplicationApprove():
    resp = {'code': 200, 'msg': '审核操作成功~~', 'data': {}}
    print(request)
    req = request.values
    id = int(req['id']) if 'id' in req else 0
    member_id = int(req['member_id']) if 'member_id' in req else 0
    community_name = req['community_name'] if 'community_name' in req else ''
    province = req['province'] if 'province' in req else ''
    city = req['city'] if 'city' in req else ''
    description = req['description'] if 'description' in req else ''
    pickups = req['pickups'] if 'pickups' in req else ''
    name = req['name'] if 'name' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    email = req['email'] if 'email' in req else ''

    has_in = Community.query.filter(Community.name == community_name).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该社区名已存在，请换一个试试~~"
        return jsonify(resp)

    model_community = Community()
    model_community.platform_id = g.current_user.platform_id
    model_community.platform_name = g.current_user.platform_name
    model_community.name = community_name
    model_community.province = province
    model_community.city = city
    model_community.description = description
    model_community.pickups = pickups

    db.session.add(model_community)
    db.session.commit()

    community = Community.query.filter_by(platform_id=g.current_user.platform_id, name=community_name).first()

    model_user = User()
    model_user.platform_id = community.platform_id
    model_user.platform_name = community.platform_name
    model_user.community_id = community.id
    model_user.community_name = community.name
    model_user.email = email
    model_user.benefit = 0.00
    model_user.created_time = getCurrentDate()
    model_user.login_salt = UserService.geneSalt()
    model_user.nickname = name
    model_user.mobile = mobile
    model_user.login_name = login_name
    model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
    model_user.updated_time = getCurrentDate()

    db.session.add(model_user)
    db.session.commit()

    member = Member.query.filter_by(id=member_id).first()
    ApplicationService.changeCommunity(member.platform_id, member_id, community.id, community.name)

    application = Application.query.filter_by(id=id).first()
    application.status = 1
    db.session.add(application)
    db.session.commit()

    return jsonify(resp)


@route_application.route("/community_application")
def communityChangeApplication():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = CommunityChangeLog.query.filter(CommunityChangeLog.platform_id == g.current_user.platform_id)

    if 'application_status' in req and int(req['application_status']) > -1:
        query = query.filter(CommunityChangeLog.status == int(req['application_status']))

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

    list = query.order_by(CommunityChangeLog.create_date.desc()).all()[offset:limit]
    print(list)

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['application_status_mapping'] = app.config['APPLICATION_STATUS_MAPPING']
    resp_data['current'] = 'community'
    if g.current_user.community_id is not None:
        return ops_render("application/leader.html")
    return ops_render("application/community_application.html", resp_data)


@route_application.route("/community_application/approve", methods=['POST'])
def communityApplicationApprove():
    resp = {'code': 200, 'msg': '审核操作成功~~', 'data': {}}
    print(request)
    req = request.values
    id = int(req['id']) if 'id' in req and req['id'] else 0
    application = CommunityChangeLog.query.filter(CommunityChangeLog.id == id).first()
    platform_id = application.platform_id
    member_id = application.member_id
    new_community_id = application.new_community_id
    new_community_name = application.new_community_name

    rt = ApplicationService.changeCommunity(platform_id, member_id, new_community_id, new_community_name)
    if rt:
        application.status = 1
        db.session.add(application)
        db.session.commit()
        return jsonify(resp)
    else:
        resp['code'] = -1
        resp['msg'] = '审批发生错误'
        return resp


@route_application.route("/set", methods=["GET", "POST"])
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
