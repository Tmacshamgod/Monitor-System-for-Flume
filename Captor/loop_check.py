import time
import functools
import tornado.ioloop
import json

import redis_client
import topic_mgr

class LoopCallbackObj(object):
    def __init__(self,cb_func,interval,topic,ip):
        self.__cb_func = cb_func
        self.__interval = interval
        self.__topic = topic
        self.__ip = ip

    def timeout(self):
        #invoke callback function
        self.__cb_func(self.__ip,self.handle)

    def handle(self,err,ts,*args):
        try:
            if err:
                print "http error:",err
            else:
                topic_mgr.add_sampling_point(self.__topic,self.__ip,ts,*args)
        except Exception,e:
            print str(e)
        tornado.ioloop.IOLoop.instance().add_timeout(time.time() + self.__interval,self.timeout)

        
    def start(self,immediately):
        if immediately:
            self.timeout()
        else:
            tornado.ioloop.IOLoop.instance().add_timeout(time.time() + self.__interval,self.timeout)

def add_loop_task(module_name,interval,topic,ip,immediately=False):
    try:
        import importlib
        m = importlib.import_module("plugin."+module_name)
        cb_func = m.collect
    except Exception,e:
        print str(e)
    cb_obj = LoopCallbackObj(cb_func,interval,topic,ip)
    cb_obj.start(immediately)

def start_loop_query():
    topics = topic_mgr.load_topics()
    if not topics:
        return False
    for topic_name,attr in topics.iteritems():
        module_name = attr.get("module_name")
        import importlib
        m = importlib.import_module("plugin."+ module_name)
        ip_list = m.get_ip_list()
        for ip in ip_list:
            add_loop_task(module_name,attr.get("time_interval"),topic_name,ip,True)
    return True
