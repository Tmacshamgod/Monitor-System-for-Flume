import json

import tornado.ioloop
import tornado.web
import pub.common.error as error

import topic_mgr

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class SamplingHandler(tornado.web.RequestHandler):
    def get(self):
        topic = self.get_argument("topic",None)
        ip = self.get_argument("ip",None)
        if not topic or not ip:
            return self.write(error.pack_errinfo_json(error.ERROR_PARAM_ARG_MISSING,"topic"))
        start_time = self.get_argument("start",None)
        if start_time:
            start_time = float(start_time)/1000
        count = int(self.get_argument("count",10))
        if(count > 200):
            count = 200
        err,points = topic_mgr.get_sampling_points(topic,ip,start_time,count)
        if err:
            self.write(error.pack_errinfo_json(error.ERROR_INTERNAL_SERVER_ERROR,err))
        else:
            content = json.dumps(points)
            self.write(content)

class RolesHandler(tornado.web.RequestHandler):
    def get(self):
        role_list = []
        import plugin
        for role in plugin.roles.roles:
            item = {
                        "ip":role[0],
                        "role":role[1]
                    }
            role_list.append(item)
        content = json.dumps(role_list)
        self.write(content)


def start(port):
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"^/static/(.*)",tornado.web.StaticFileHandler,{"path":"./statics/"}),
        (r"/sampling",SamplingHandler),
        (r"/roles",RolesHandler),
    ])
    application.listen(port)
    tornado.ioloop.IOLoop.current().start()
