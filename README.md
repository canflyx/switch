# 程序介绍

本程序通过交换机的登陆获取对应的ARP地址，MAC地址等信息，方便管理员快速查找端口对应的IP地址或根据IP找到对应的交换机。


# 文件介绍

- 数据库文件：app.db

- 配置文件：config/setting
  - 交换机交互命令
    - BASE_COMM 公用命令，默认是华为交换机配置
    - MAC_COMM 接入交换机命令 获取接入交换机端口MAC地址
    - ARP_COMM  核心交换机命令  获取MAC对应IP地址

- 程序入口 manage.py