import tornado.web

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World")
    def post(self):
        self.write(self.request.body)
