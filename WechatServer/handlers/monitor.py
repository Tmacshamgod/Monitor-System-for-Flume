import tornado.web
import urllib2
import json

corpid = "wx8d2439c37d3956d3"
corpsecret = "kBfCY4UeJb2CZJK7dweTtS5lion8ngi_i4ybwIK9cl97M1nDv2qxrf8sQ4XhZti1"
url1 = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (corpid, corpsecret)
url2 = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s"

class MonitorHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(urllib2.urlopen(url1).read())

    def post(self):
        token = json.loads(urllib2.urlopen(url1).read())['access_token']
        url = url2%token
        level = self.get_argument('level', None)
        content = json.loads(self.request.body)
        message = content['message']
        msgtype = content['msgtype']
        msgbody = {
                    "touser": "jeff",
                    "msgtype": msgtype,
                    "agentid": 0,
                    "text":
                        {
                            "content": 'ip: %s, '
                                       'role: %s, '
                                       'message: %s.'
                                       %(message['ip'],
                                         message['role'],
                                         message['content'])
                        },
                    "safe": "0"}
        if level == 'error':
            http_body = json.dumps(msgbody)
            self.write(urllib2.urlopen(url, http_body).read())



