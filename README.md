# 程序介绍
重新用 GO+VUE 写了一个桌面可运行程序。就不用部署服务器啥的了。

https://github.com/canflyx/gosw/

​	本程序通过交换机的登陆获取对应的ARP地址，MAC地址等信息，方便管理员快速查找端口对应的IP地址或根据IP找到对应的交换机。本系统数据库文件使用sqlite系统。配置文件详见/config/setting.py文件

​	mac地址、交换机扫描可同时运行于windows和linux，主机监控只能运行于Linux，依赖于Linux的nmap,crontab包。远程登陆依赖于telnetlib包

 **​        提示：交换机的扫描使用Flask-Executor异步进行。** 
    感谢**编程浪子**的《Python Flask构建微信小程序订餐系统》等相关视频。手艺粗糙,技术肤浅，不适用于老鸟、傻X
## windows安装：

1. 安装python3,pip，并配置path,详细baidu，google

2.  解压至某目录如：

   ```
    d:\switch
   ```

   

3. 安装python虚拟环境如:

   ```
   python -m venv sw-env
   ```

   

4. 进入虚拟目录并安装组件

   ```
   sw-env\Scripts\activate.bat
   pip install -r requirements.txt
   ```

   

5. 运行系统
   
    ```
    python manage.py runserver
    ```
    
    如果使用uwsgi或长期运行，请参考网上其它flask创建配置。
    

## ubuntu,debian安装

1. 安装python3环境及组件

   ```
   sudo apt install python3 pip nmap 
   ```

   安装虚拟环境及组件

   参考windows 3-4安装步骤，自行baidu,google   

3. 运行系统

   ```
   python3 manage.py runserver
   or   
   uwsgi --ini sw/uwsgi.ini                                              
   ```
   
   如果使用uwsgi或长期运行，uwsgi.ini为uwsgi运行文件。其它请参考网上其它flask创建配置。    


# 文件介绍

- 数据库文件：app.db 

- 配置文件：config/setting
  - 交换机交互命令
    - BASE_COMM 公用命令，默认是华为交换机配置
    - MAC_COMM 接入交换机命令 获取接入交换机端口MAC地址
    - ARP_COMM  核心交换机命令  获取MAC对应IP地址

- 程序入口 manage.py

界面预览：
主界面
![avatar](readme/index.png)
搜索
![avatar](readme/index-mac.png)
交换机界面
![avatar](readme/sw-index.png)
交换机信息
![avatar](readme/sw-info.png)
交换机添加
![avatar](readme/sw-add.png)
监控界面
![avatar](readme/mon-index.png)
