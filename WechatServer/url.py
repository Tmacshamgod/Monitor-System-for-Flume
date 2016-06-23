import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from handlers.hello import HelloHandler
from handlers.monitor import MonitorHandler

url = [
    (r'/', HelloHandler),
    (r'/monitor', MonitorHandler),
]