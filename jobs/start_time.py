import atexit
import fcntl

from jobs.nmap import nmap


def start_timer():
    # 定义锁文件
    f = open(" /var/www/logs/automation.lock", "wb")
    try:
        # 开启排斥(劝告锁),非阻塞锁,锁文件存在则不创建新的对象
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # 开启定时任务
        nmap()

        import uwsgi
        # 使用main_loop阻塞进程,防止进程挂起
        while True:
            sig = uwsgi.signal_wait()
    except Exception as e:
        pass
    # 给文件解锁
    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
    # 注册程序退出时的回调函数
    atexit.register(unlock)

start_timer()