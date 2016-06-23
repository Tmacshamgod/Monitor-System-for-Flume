import urllib2
import json

class eagle:
    def __init__(self, last_time, flag):
        self.__last_time = last_time
        self.__flag = flag

    def alert(self, level, ip, role, content):
        url = 'http://10.5.0.66:8888/monitor?level=%s' % level
        values = {
                    "message":
                    {
                        "ip": ip,
                        "role": role,
                        "content": content
                    },
                    "msgtype": "text"
                }
        http_body = json.dumps(values)
        print urllib2.urlopen(url, http_body).read()

    def monitor(self, ip, currentTime):
        if currentTime is None:
            return None, None, None
        url = 'http://10.5.0.66:11003/sampling?ip=%s&topic=flume_agent_monitor&start=%s&count=100' % (ip, currentTime)
        resp = urllib2.urlopen(url).read()
        values = json.loads(resp)
        if len(values) == 0:
            return currentTime, [], []
        value = values[-1:][0]
        return value['timestamp'], value['points'], value['percentage']

    def callback(self, ip, role, threshold, level='error', content='server crashed'):
        last, points, percentages = self.monitor(ip, self.__last_time)
        import ast
        percentages = ast.literal_eval(str(percentages))

        if percentages is not None and percentages:
            percentage1 = percentages[0] if len(percentages) > 0 else 0.0
            percentage2 = percentages[1] if len(percentages) > 1 else 0.0
            percentage3 = percentages[2] if len(percentages) > 2 else 0.0
        else:
            percentage1 = 0.0
            percentage2 = 0.0
            percentage3 = 0.0

        if points is not None and points:
            output = points[2]
            point = points[0] + points[1] + points[2]
        else:
            output = 0
            point = 0

        if last is None or last == self.__last_time or point == 0:
            if self.__flag:
                self.alert(level, ip, role, content)
                self.__flag = False
        elif output < threshold:
            if self.__flag:
                content = "output is below threshold"
                self.alert(level, ip, role, content)
                self.__flag = False
        elif percentage1 > 80 or percentage2 > 80 or percentage3 > 80:
            if self.__flag:
                content = "channel is above 80%"
                self.alert(level, ip, role, content)
                self.__flag = False
        else:
            self.__flag = True
        self.__last_time = last

    def test(self, level, ip, role, content):
        print "ip %s" % ip
