SERVER_PORT = 8800
DEBUG = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SQLALCHEMY_ENCONDING = "utf-8"
DEBUG = True
BASE_COMM = ['sys\n', 'user-interface vty 0 4\n', 'screen-length 0\n']
MAC_COMM=['dis mac-address\n', 'undo screen-length\n']
ARP_COMM=['dis arp\n','undo screen-length\n']
QUIT_COMM=['undo screen-length\n', 'quit\n','quit\n', 'quit\n']
PAGE_SIZE = 50
PAGE_DISPLAY = 10
JOBS = [
    {
        'id': 'autosubimit',
        'func': '__main__:print_job',
        'args': None,
        'trigger': 'interval',
        'seconds': 20
    }]
SCHEDULER_API_ENABLED = True
