import collections
import sys
# import pexpect
import time
import threading

from common.models.Mac import MAC
from common.models.Arp import ARP
from common.Helper import getCurrentDate
from application import db, app,executor
from common.models.Sw import Sw
# from concurrent.futures import ThreadPoolExecutor


class GetMac():

    def __getformat(self, reslt, ip, iscore):
        if len(reslt) < 10:
            app.logger.info('-------1')
            return False
        a = {}
        b = []
        # 读取每行，格式化形成一个mac:端口的列表和端口表
        xlist = reslt.split('\r\n')
        for item in xlist:
            if str(item).find('GE') != -1 or str(item).find('Eth') != -1:
                list = item.split(' ')
                while '' in list:
                    list.remove('')
                print(iscore)
                if iscore == 1:
                    arp_info = ARP.query.filter_by(ipaddr=list[0]).first()
                    if arp_info:
                        arp_info.macadd = list[1]
                        arp_info.update_time = getCurrentDate()
                        db.session.add(arp_info)
                        db.session.commit()
                    else:
                        db.session.execute(
                            ARP.__table__.insert(),
                            [{'ipaddr': list[0], 'macadd': list[1], 'swip': ip, 'update_time': getCurrentDate()}]
                        )
                        db.session.commit()
                else:
                    b.append(list[2])
                    a[list[0]] = list[2]
        if iscore == 1:
            return True
        if len(b) < 1:
            return False
        # ss=getFormat(reslt=f,ip=HOST)
        c = collections.Counter(b)
        nums_dict = dict(collections.Counter(b))
        # 保留只有1个MAC的键值
        li = []
        for k, v in nums_dict.items():
            if v == 1:
                li.append(k)
        # 从a中选出只有一个的mac和端口对应

        for key in a:
            if str(a[key]).isalnum():
                continue
            if a[key] in li:
                mac_info = MAC.query.filter_by(macadd=key).first()
                if mac_info:
                    mac_info.port = a[key]
                    mac_info.update_time = getCurrentDate()
                    db.session.add(mac_info)
                    db.session.commit()
                else:
                    db.session.execute(
                        MAC.__table__.insert(),
                        [{'port': a[key], 'macadd': key, 'swip': ip, 'update_time': getCurrentDate()}]
                    )
                db.session.commit()
        return True

# 根据 HOST USER PASS 及 COMMAND 命令参数
    def __telnetdo(self, HOST, USER, PASS, COMMAND):
        if not HOST:
            return
        try:
            import telnetlib
            tn = telnetlib.Telnet(HOST, timeout=5)
            # with telnetlib.Telnet(HOST, timeout=10) as tn:
            tn.set_debuglevel(2)
            tn.read_until(b"Username:", timeout=3)
            tn.write(USER.encode('ascii') + b'\n')
            if PASS:
                # msg.append(tn.expect(['Password:'], 5))
                tn.read_until(b"Password:", timeout=3)
                tn.write(PASS.encode('ascii') + b'\n')
                # msg.append(tn.expect([USER], 5))
            tn.read_until(b'[Y/N]:', timeout=2)
            tn.write(b'n\n')
            tn.read_until(b'>', timeout=3)
            for i in COMMAND:
                tn.write(i.encode('ascii'))
                time.sleep(2)
            f = tn.read_very_eager().decode('ascii')
            tn.write(b"quit\n")
            tn.write(b"quit\n")
            tn.write(b"quit\n")
            tn.close()
            print('quit over')
        except:
            f = "error"
        return f

    # def __getip(self, swids):
    #     swips = []
    #     for item in swids:
    #         info = Sw.query.filter_by(id=item).first()
    #         if info is None:
    #             continue
    #         swips.append(info.swip)
    #     return swips

    def __status(self, id, status):
        info = Sw.query.filter_by(id=id).first()
        info.status = status
        info.update_time = getCurrentDate()
        db.session.add(info)
        db.session.commit()
        return True

    # 对传入的交换机列表 swids 进行处理.
    # 对处理进行多线程改造
    def get(self, id,ipaddr,user,passwd,comm,iscore):
        # for item in swids:
        #     info = Sw.query.filter_by(id=item).first()
        #     if info is None:
        #         continue
        #     comm = []
        #     comm.extend(app.config['BASE_COMM'])
        #     if info.iscore == 0:
        #         comm.extend(app.config['MAC_COMM'])
        #     else:
        #         comm.extend(app.config['ARP_COMM'])
        resault = self.__telnetdo(ipaddr, user, passwd, comm)
        if resault.find('GE') < 0 and resault.find('Eth') < 0:
            self.__status(id, 1)
            return
        isok = self.__getformat(resault,ipaddr, iscore)
        if not isok:
            self.__status(id, 1)
            return
        self.__status(id, 0)

    def threads(self, swids):
        # t = ThreadPoolExecutor(5)
        for item in swids:
            info = Sw.query.filter_by(id=item).first()
            if info is None:
                continue
            comm = []
            comm.extend(app.config['BASE_COMM'])
            if info.iscore == 0:
                comm.extend(app.config['MAC_COMM'])
            else:
                comm.extend(app.config['ARP_COMM'])
            # t.submit(self.get,(item,info.ipaddr, info.user, info.passwd, comm,info.iscore))
            executor.submit(self.get,item,info.ipaddr, info.user, info.passwd, comm,info.iscore)
            # self.get(item,info.ipaddr, info.user, info.passwd, comm,info.iscore)