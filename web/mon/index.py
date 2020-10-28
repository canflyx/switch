import getpass
import json
import os
import re

from flask import Blueprint, request, jsonify

from application import app, db
from common.CrontabUpdate import CrontabUpdate
from common.Helper import getCurrentDate, ops_render, get_time
from common.models.MonLog import MonLog
from common.models.Monitor import Monitor

route_mon = Blueprint('mon_page', __name__)


@route_mon.route('/')
def index():
    resp_data = {}
    info = Monitor.query.all()
    resp_data['info'] = info
    return ops_render('mon/index.html', resp_data)


@route_mon.route('/set', methods=['POST', 'GET'])
def set():
    if request.method == 'GET':
        resp_date = {}
        info = None
        resp_date['info'] = info
        return ops_render('mon/set.html', resp_date)
    resp = {'code': 200, 'msg': '设置成功', 'data': {}}
    req = request.values
    ip = req['ipaddr'] if 'ipaddr' in req else ''
    note = req['note'] if 'note' in req else ''

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
            [{'ipaddr': item, 'create_time': getCurrentDate(), 'note': note}]
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


@route_mon.route('/info')
def info():
    resp_data = {}
    req = request.values
    id = req['id'] if 'id' in req or 'id' != None else 0
    log_info = MonLog.query.filter_by(mon_id=id).limit(10)
    mon_info = Monitor.query.filter_by(id=id).first()
    # mac_info= MAC.query.filter_by(IpAdd=sw_info.IpAdd).first()
    resp_data['info'] = log_info
    resp_data['moninfo'] = mon_info
    return ops_render('mon/info.html', resp_data)


@route_mon.route('/cron', methods=['POST', 'GET'])
def cron():
    resp = {'code': 200, 'msg': '配置成功', 'data': {}}
    req = request.values
    crontime = req['time'] if 'time' in req else 0
    act = req['act'] if 'act' in req else ''
    if os.name != 'posix':
        resp['code'] = -1
        resp['msg'] = "监控只能运行于linux系统"
        return jsonify(resp)
    crontab_update = CrontabUpdate()
    commont_name = app.config['COMM_NAME']
    user = getpass.getuser()
    if act == 'stop':
        crontab_update.del_crontab_jobs(commont_name, user)
        resp['code'] = 200
        resp['msg'] = "删除成功"
        return jsonify(resp)
    if not crontime:
        resp['code'] = -1
        resp['msg'] = "未选择正确时间~~"
        return jsonify(resp)
    time_str = get_time(int(crontime))
    cmmand_line = re.findall('([\S]*?)web', os.path.abspath(__file__))[0] + '/cron.sh'
    crontab_update.del_crontab_jobs(commont_name, user)
    crontab_update.add_crontab_job(cmmand_line, time_str, commont_name, user)
    return jsonify(resp)

