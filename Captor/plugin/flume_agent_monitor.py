import time
import json
import functools
import tornado.curl_httpclient
import roles

_client = tornado.curl_httpclient.CurlAsyncHTTPClient()

_agent_handlers = {}


class AgentHandler(object):
    def __init__(self):
        self.__prev_entry_count = None
        self.__prev_output_count = None

    def handle(self, final_handler, response):
        if response.error:
            return final_handler(str(response.error), None)
        try:
            content = response.body
            ret = json.loads(content)
            current = time.time()
            entry_count = int(ret["SOURCE.source1"]["EventReceivedCount"])
            stock = int(ret["CHANNEL.ch1"]["ChannelSize"])
            channel_percentage = []
            for i in range(3):
                channel_percentage.append(0.0)
                channel_name = "CHANNEL.ch" + str(i + 1)
                if ret.has_key(channel_name):
                    channel_percentage[i] = float(ret[channel_name]["ChannelFillPercentage"])

            output_count = 0
            for i in range(30):
                sink_name = "SINK.sink" + str(i + 1)
                if ret.has_key(sink_name):
                    output_count += int(ret[sink_name]["EventDrainSuccessCount"])
            if self.__prev_entry_count is None:
                self.__prev_entry_count = entry_count
                entry_count = 0
            else:
                tp = entry_count
                entry_count = entry_count - self.__prev_entry_count
                if entry_count < 0:
                    entry_count = 0
                self.__prev_entry_count = tp
            if self.__prev_output_count is None:
                self.__prev_output_count = output_count
                output_count = 0
            else:
                tp = output_count
                output_count = output_count - self.__prev_output_count
                if output_count < 0:
                    output_count = 0
                self.__prev_output_count = tp
            final_handler(None, current, entry_count, stock, output_count, channel_percentage)
        except Exception, e:
            final_handler(str(e), None)


def get_ip_list():
    return [item[0] for item in roles.roles]


for ip in get_ip_list():
    _agent_handlers[ip] = AgentHandler()


def collect(ip, final_handler):
    url = "http://%s/metrics" % ip
    req = tornado.httpclient.HTTPRequest(url, headers={"Connection": "Keep-Alive"})
    agent_handler = _agent_handlers.get(ip)
    if agent_handler:
        _client.fetch(req, functools.partial(agent_handler.handle, final_handler))
