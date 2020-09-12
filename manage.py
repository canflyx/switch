from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler

from application import app, manager
from flask_script import Server
from jobs.nmap import nmap
import www

manager.add_command("runserver",
                    Server(host="0.0.0.0", port=app.config['SERVER_PORT'], use_debugger=True, use_reloader=True))
app.config['JSON_AS_ASCII'] = False




def print_job():
    nmap()
def main():
    # app.config['JOBS']
    # scheduler = APScheduler()
    # scheduler.init_app(app)
    # scheduler.start()
    manager.run()



if __name__ == '__main__':
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()