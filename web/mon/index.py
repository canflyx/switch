import json

from flask import Blueprint,  request, jsonify

from application import app, db
from common.Helper import getCurrentDate,  ops_render
from common.models.Monitor import Monitor


route_mon= Blueprint('mon_page', __name__)


@route_mon.route('/')
def index():
    resp_data = {}
    info = Monitor.query.all()
    resp_data['info'] = info
    return ops_render('mon/index.html', resp_data)


@route_mon.route('/set', methods=['POST','GET'])
def set():
    if request.method == 'GET':
        resp_date = {}
        info = None
        resp_date['info'] = info
        return ops_render('mon/set.html', resp_date)
    resp = {'code': 200, 'msg': '设置成功', 'data': {}}
    req = request.values
    ip = req['ipaddr'] if 'ipaddr' in req else ''
    note=req['note'] if 'note' in req else ''

    if ip is None:
        resp['code'] = -1
        resp['msg'] = 'ip输入错误'
        return jsonify(resp)

    for item in json.loads(ip):
        has_in = Monitor.query.filter(Monitor.ipaddr == item).first()
        if has_in:
            resp['code'] = -1
            resp['msg'] = 'IP地址:%s 已存在，请更改' % item
            return jsonify(resp)
        db.session.execute(
            Monitor.__table__.insert(),
            [{'ipaddr': item, 'create_time': getCurrentDate(),'note': note}]
        )
        db.session.commit()
    return jsonify(resp)


@route_mon.route('/ops', methods=['POST'])
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
