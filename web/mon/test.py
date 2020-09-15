import json

from flask import Blueprint,  request, jsonify
# import nmap3
# from application import app, db
# from common.Helper import getCurrentDate,  ops_render
# from common.models.Monitor import Monitor
#
# def nmapip():
#     info=Monitor.query.all()
#     ip=''
#     for item in info:
#         ip=ip+item.IpAdd+' '
#     print(ip)
#     nmap = nmap3.NmapHostDiscovery(
#
#     )
#     results = nmap.nmap_no_portscan(ip)
#     print(results)
#     db.session.execute(
#         Monitor.__table__.update(),
#         [{'IsOk':'0'}]
#     )
#     db.session.commit()
#
#     for i in range(0,len(results['hosts'])):
#         ip=results['hosts'][i]['addr']
#         status= 1 if results['hosts'][1]['state'] =='up' else '0'
#         mon=Monitor.query.filter_by(IpAdd=ip).first()
#         if mon:
#             mon.UpdateTime = getCurrentDate()
#             mon.IsOk=status
#             db.session.add(mon)
#             db.session.commit()
#     return 'ok'
#
#
# info=Monitor.query.all()
# if info is None:
#     exit(1)
# ip=''
# for item in info:
#     ip=ip+item.IpAdd+' '
# nmap = nmap3.NmapHostDiscovery(
# )
# results = nmap.nmap_no_portscan(ip)
# db.session.execute(
#     Monitor.__table__.update(),
#     [{'IsOk':'0'}]
# )
# db.session.commit()
# if results:
#     exit(1)
# for i in range(0,len(results['hosts'])):
#     ip=results['hosts'][i]['addr']
#     status= 1 if results['hosts'][1]['state'] =='up' else '0'
#     mon=Monitor.query.filter_by(IpAdd=ip).first()
#     if mon:
#         mon.UpdateTime = getCurrentDate()
#         mon.IsOk=status
#         db.session.add(mon)
#         db.session.commit()


