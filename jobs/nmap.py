import nmap3

from application import app, db
from common.models.Monitor import Monitor
from common.Helper import getCurrentDate

def nmap():
    with app.app_context():

        info = Monitor.query.all()
        print(info.id)
        if info is None:
            exit(1)
        ip = ''
        for item in info:
            ip = ip + item.IpAdd + ' '
        nmap = nmap3.NmapHostDiscovery(
        )
        results = nmap.nmap_no_portscan(ip)
        db.session.execute(
            Monitor.__table__.update(),
            [{'isok': '0'}]
        )
        db.session.commit()
        if results:
            exit(1)
        for i in range(0, len(results['hosts'])):
            ip = results['hosts'][i]['addr']
            status = 1 if results['hosts'][i]['state'] == 'up' else '0'
            mon = Monitor.query.filter_by(ipaddr=ip).first()
            if mon:
                mon.update_time = getCurrentDate()
                mon.isok = status
                db.session.add(mon)
                db.session.commit()

