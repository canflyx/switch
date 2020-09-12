from application import app
from web.switch.index import route_sw
from web.static import route_static
from web.mon.index import route_mon
from web.index.index import route_index
from web.switch.test import route_test


app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_sw, url_prefix="/switch")
app.register_blueprint(route_mon, url_prefix="/mon")
app.register_blueprint(route_static, url_prefix='/static')
app.register_blueprint(route_test, url_prefix='/test')
