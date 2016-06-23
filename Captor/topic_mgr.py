import json
import redis_client
import time

_MAX_TIME = time.time() + 3600*24*365*10
_topics = {}

def load_topics():
    topic_file = "conf/topics.json"
    try:
        topics = json.load(open(topic_file,"r"))
        if not topics:
            return None
        global _topics
        for topic in topics:
            topic_name = topic.get("topic_name")
            if not topic_name:
                return None
            module_name = topic.get("module_name")
            if not module_name:
                return None
            time_interval = topic.get("time_interval")
            if not time_interval:
                return None
            rows = topic.get("rows")
            if not rows:
                rows = 1000
            _topics[topic_name] = {"module_name":module_name,"time_interval":time_interval,"rows":rows}
            return _topics
    except Exception,e:
        print str(e)
        return None


def initialize():
    topics = load_topics()
    if not topics:
        return False
    global _topics
    for topic in topics:
        topic_name = topic.get("topic_name")
        if not topic_name:
            return False
        module_name = topic.get("module_name")
        if not module_name:
            return False
        time_interval = topic.get("time_interval")
        if not time_interval:
            return False
        rows = topic.get("rows")
        if not rows:
            rows = 1000
        _topics[topic_name] = {"module_name":module_name,"time_interval":time_interval,"rows":rows}
    return True

def get_sampling_points(topic,ip,start_time,count):
    zset_key = ":".join((topic,ip))
    try:
        client = redis_client.client
        if not start_time:
            points = client.zrange(zset_key,-count,-1,withscores=True)
        else:
            points = client.zrangebyscore(zset_key,start_time+0.001,_MAX_TIME,start=0,num=count,withscores=True)
        segs = []
        for v,s in points:
            item = {
                        "timestamp": int(1000*s),
                        "points": [float(x) for x in v.split(":")[:-2]],
                        "percentage": v.split(":")[-2:-1][0]
                }
            segs.append(item)
        return (None,segs)
    except Exception,e:
        print str(e)
        return (str(e),None)

def add_sampling_point(topic,ip,t,*point):
    try:
        attr = _topics.get(topic)
        if not attr:
            return False
        zset_key = ":".join((topic,ip))
        segs = map(str,point)
        segs.append(str(t))
        value = ":".join(segs)
        client = redis_client.client
        client.zadd(zset_key, t,value)
        if client.zcard(zset_key) > attr.get("rows"):
            client.zremrangebyrank(zset_key,0,0)
    except Exception,e:
        print str(e)