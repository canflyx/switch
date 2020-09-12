import json

from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from application import app, db
from common.Helper import getCurrentDate, ops_render, iPagination
from common.models.Mac import MAC
from common.models.Arp import ARP
from common.models.Monitor import Monitor
from common.models.Sw import Sw

route_index = Blueprint('index_page', __name__)


@route_index.route('/')
def index():
    req = request.values
    resp_data = {}
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = db.session.query(MAC, ARP).outerjoin(ARP, ARP.macadd == MAC.macadd)
    if 'mix_kw' in req:
        rule = or_(MAC.macadd.like("%{0}%".format(req['mix_kw'])), ARP.ipaddr.like("%{0}%".format(req['mix_kw'])))
        # query = query.filter(rule)
        query = query.filter(rule)
    # query = MAC.query.join(ARP, MAC.MacAdd == ARP.MacAdd).all()

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
    # list = query.order_by(MAC.Id.desc()).all()[offset:limit]
    # list=query.outerjion(ARP).all()[offset:limit]
    list = query.order_by(MAC.swip).all()[offset:limit]

    resp_data['info'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    return ops_render('index/index.html', resp_data)


@route_index.route('/set', methods=['POST', 'GET'])
def set():
    if request.method == 'GET':
        resp_date = {}
        info = None
        resp_date['info'] = info
        return ops_render('mon/set.html', resp_date)
    resp = {'code': 200, 'msg': '设置成功', 'data': {}}
    req = request.values
    ip = req['ipaddr'] if 'ipaddr' in req else ''
    if ip is None:
        resp['code'] = -1
        resp['msg'] = '交换机输入错误'
        return jsonify(resp)

    for item in json.loads(ip):
        has_in = Monitor.query.filter(Monitor.ipaddr == item).first()
        if has_in:
            resp['code'] = -1
            resp['msg'] = 'IP地址:%s 已存在，请更改' % item
            return jsonify(resp)
        db.session.execute(
            Monitor.__table__.insert(),
            [{'ipaddr': item, 'create_time': getCurrentDate(), 'update_time': getCurrentDate()}]
        )
        db.session.commit()
    return jsonify(resp)


@route_index.route('/ops', methods=['POST'])
def ops():
    resp = {'code': 200, 'msg': '设置成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)
    if act != 'remove':
        resp['code'] = -1
        resp['msg'] = "操作不正确~~"
        return jsonify(resp)
    mon_info = Monitor.query.filter_by(id=id).first()
    if not mon_info:
        resp['code'] = -1
        resp['msg'] = "帐号不存在~~"
        return jsonify(resp)
    db.session.delete(mon_info)
    db.session.commit()
    return jsonify(resp)
