import server_infos
import tornado.ioloop
from eagle import eagle


def create_task(ip, role, threshold, obj):
    tornado.ioloop.PeriodicCallback(lambda: obj.callback(ip, role, threshold), 1000 * 60).start()


def start_loop():
    servers = server_infos.load_servers()
    if not servers:
        return False
    for ip, attr in servers.iteritems():
        role = attr.get("role")
        threshold = attr.get("threshold")
        create_task(ip, role, threshold, eagle('', True))
    return True


if __name__ == "__main__":
    if not start_loop():
        print "failed to create task"
    tornado.ioloop.IOLoop.instance().start()
