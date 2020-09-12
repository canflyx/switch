import json

from flask import Blueprint, render_template, request, jsonify

from application import app, db
from common.Helper import getCurrentDate, ops_render
from common.models.Monitor import Monitor
from common.models.Sw import Sw

from multiprocessing import Queue

from threading import Thread
import subprocess


route_test = Blueprint('test_page', __name__)



@route_test.route('/ip')
def ip():
    num_threads = 10
    q = Queue()

    def pingme(i, queue):
        while True:
            ip = queue.get()
            ret = subprocess.call('ping -c 1 %s' % i, shell=True, stdout=open('e:\\git\\ip.txt', 'w'),
                                  stderr=subprocess.STDOUT)
            if ret == 0:
                print('%s-%s is up!' % i)
            elif ret == 1:
                print('%s is down...' % i)
            queue.task_done()

    for i in range(num_threads):
        t = Thread(target=pingme, args=(i, q))  # 多线程调用
        t.setDaemon(True)  # 设置守护线程
        t.start()
    info = Monitor.query.all()
    for i in info:
        q.put(i.IpAddr)  # 上传列表
    q.join()
    print('完成')
    return 'ok'



# @route_test.route('/tt')
# def tt():
    #return nmapip()
    # HOST = '172.17.3.1'
    # USER = 'daika'
    # PASS = 'Daik@2018'
    # iscore = '1'
    # comm = app.config['BASE_COMM']
    # comm.extend(app.config['ARP_COMM'])
    # list = telnetdo(HOST=HOST, USER=USER, PASS=PASS, COMMAND=comm)
    # if list.find('GE') < 0 or list.find('Eth') < 0:
    #     return
    # print(len(list))
    # # isok = getFormat(reslt=list, ip=HOST, iscore=1)
    #
    # # if isok:
    # #    return True
    # return False


@route_test.route('/test')
def test():
    # f = open('e:\\git\\order\\1.txt', 'r')
    # HOST='192.168.0.1'
    # ss=getFormat(reslt=f.readlines(),ip=HOST)
    # f.close()
    resp = {'code': 200, 'msg': '设置成功', 'data': {}}
    sw_info = Sw.query.all()
    for item in sw_info:
        comm = app.config['BASE_COMM']
        print('---------------')
        print(item.IsCore)
        print(item.IsCore == 0)
        if item.IsCore == 0:
            comm.extend(app.config['MAC_COMM'])
        else:
            comm.extend(app.config['ARP_COMM'])
        print(comm)
        list = telnetdo(HOST=item.IpAdd, USER=item.User, PASS=item.Passwd, COMMAND=comm)
        info = Sw.query.filter_by(Id=item.Id).first()
        if list.find('GE') < 0 or list.find('Eth') < 0:
            info.status = 1
            resp['data'] = {item.IpAdd: False}
        else:
            isok = getFormat(reslt=list, ip=item.IpAdd, iscore=item.IsCore)
            if isok:
                resp['data'] = {item.IpAdd: True}
                info.status = '0'

            else:
                resp['data'] = {item.IpAdd: False}
                info.status = 1

        info.UpdateTime = getCurrentDate()
        db.session.add(info)
        db.session.commit()

    return jsonify(resp)
