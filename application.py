import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_executor import Executor


class Application(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):
        super(Application, self).__init__(import_name, template_folder=template_folder, root_path=root_path,
                                          static_folder=None)
        self.config.from_pyfile('config/setting.py')
        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__, template_folder=os.getcwd() + "/web/templates/")
EXECUTOR_MAX_WORKERS = 15
executor = Executor(app)
manager = Manager(app)

from common.UrlManager import UrlManager

app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
