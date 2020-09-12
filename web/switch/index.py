import json
import time

from flask import Blueprint, render_template, request, jsonify

from application import app, db
from common.GetMac import GetMac
from common.Helper import getCurrentDate, ops_render
from common.models.Arp import ARP
from common.models.Mac import MAC
from common.models.Sw import Sw

route_sw = Blueprint('sw_page', __name__)


@route_sw.route('/')
def index():
    resp_data = {}
    info = Sw.query.all()
    resp_data['info'] = info
    return ops_render('switch/index.html', resp_data)


@route_sw.route('/set', methods=['POST', 'GET'])
def set():
    default_pwd = "******"
    if request.method == 'GET':
        resp_date = {}
        req = request.values
        info = None
        swid = int(req.get('id', 0))
        if swid:
            info = Sw.query.filter_by(id=swid).first()
        resp_date['info'] = info
        return ops_render('switch/set.html', resp_date)

    resp = {'code': 200, 'msg': '设置成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req or 'id' == None else 0
    swip = req['ipaddr'] if 'ipaddr' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    iscore = req['iscore'] if 'iscore' in req else 0
    note = req['note'] if 'note' in req else ''

    if swip is None:
        resp['code'] = -1
        resp['msg'] = '交换机输入错误'
        return jsonify(resp)
    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '交换机登陆名输入错误'
        return jsonify(resp)
    if login_pwd is None or len(login_pwd) < 2:
        resp['code'] = -1
        resp['msg'] = '交换机登陆密码输入格式错误'
        return jsonify(resp)
    if id != '':
        sw_info = Sw.query.filter_by(id=id).first()
        if sw_info:
            model_sw = sw_info
        else:
            model_sw = Sw()
        model_sw.IsCore = iscore
        model_sw.User = login_name
        model_sw.Note = note
        model_sw.CreateTime = getCurrentDate()
        if login_pwd != default_pwd:
            model_sw.Passwd = login_pwd
        db.session.add(model_sw)
        db.session.commit()
        return jsonify(resp)

    for item in json.loads(swip):
        has_in = Sw.query.filter(Sw.ipaddr == item, Sw.id != id).first()
        if has_in:
            resp['code'] = -1
            resp['msg'] = '交换机%s已存在，请更改' % item
            return jsonify(resp)
        db.session.execute(
            Sw.__table__.insert(),
            [{'Passwd': login_pwd, 'User': login_name, 'Ipaddr': item, 'iscore': iscore,
              'create_time': getCurrentDate()}]
        )
        db.session.commit()
    return jsonify(resp)


@route_sw.route('/ops', methods=['POST'])
def ops():
    resp = {'code': 200, 'msg': '设置成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的交换机~~"
        return jsonify(resp)
    if act != 'remove':
        resp['code'] = -1
        resp['msg'] = "操作不正确~~"
        return jsonify(resp)
    sw_info = Sw.query.filter_by(id=id).first()
    if not sw_info:
        resp['code'] = -1
        resp['msg'] = "帐号不存在~~"
        return jsonify(resp)
    db.session.delete(sw_info)
    db.session.commit()
    return jsonify(resp)


@route_sw.route('/scan', methods=['POST'])
def scan():
    resp = {'code': 200, 'msg': '扫描完成', 'data': {}}
    req = request.values
    swid = req['id'] if 'id' in req or 'id' == None else 0

    if swid == 0:
        resp['code'] = -1
        resp['msg'] = '没有需要扫描的交换机'
        return resp
    getmac = GetMac()
    getmac.get(json.loads(swid))
    # for item in json.loads(swid):
    #     if item is None:
    #         continue
    #     info = Sw.query.filter_by(id=item).first()
    #     print(info)
    #     if info is None:
    #         continue
    #     comm = []
    #     comm.extend(app.config['BASE_COMM'])
    #     if info.IsCore == 0:
    #         comm.extend(app.config['MAC_COMM'])
    #     else:
    #         comm.extend(app.config['ARP_COMM'])
    #     print(comm)
    #     list = telnetdo(HOST=info.IpAdd, USER=info.User, PASS=info.Passwd, COMMAND=comm)
    #     print(list)
    #     if list.find('GE') < 0 and list.find('Eth') < 0:
    #         status(id=item, status=1)
    #         app.logger.info('-------11')
    #         continue
    #
    #     isok = getFormat(reslt=list, ip=info.IpAdd, iscore=info.IsCore)
    #     if not isok:
    #         status(id=item, status=1)
    #         continue
    #     status(id=item, status=0)
    return resp


@route_sw.route('/info')
def info():
    resp_data = {}
    req = request.values
    swid = req['id'] if 'id' in req or 'id' == None else 0
    sw_info = Sw.query.filter_by(id=swid).first()
    mac_info = db.session.query(MAC, ARP).outerjoin(ARP, ARP.macadd == MAC.macadd).filter(MAC.swip == sw_info.ipaddr).order_by(MAC.port).all()
    # mac_info= MAC.query.filter_by(IpAdd=sw_info.IpAdd).first()
    resp_data['info'] = sw_info
    resp_data['macinfo'] = mac_info
    return ops_render('switch/info.html', resp_data)


# def status(id=0, status=1):
#     info = Sw.query.filter_by(id=id).first()
#     info.status = status
#     info.update_time = getCurrentDate()
#     db.session.add(info)
#     db.session.commit()
#     return True
