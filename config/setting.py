# flask运行相关参数
SERVER_PORT = 8800
DEBUG = False
# 数据库连接相关参数
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SQLALCHEMY_ENCONDING = "utf-8"
DEBUG = True
# 交换机操作命令集（分为核心交换机和接入交换机，可依据品牌和型号自行更改）
BASE_COMM = ['sys\n', 'user-interface vty 0 4\n', 'screen-length 0\n']
MAC_COMM = ['dis mac-address\n', 'undo screen-length\n']
ARP_COMM = ['dis arp\n', 'undo screen-length\n']
QUIT_COMM = ['undo screen-length\n', 'quit\n', 'quit\n', 'quit\n']
# 显示分页参数
PAGE_SIZE = 50
PAGE_DISPLAY = 10

