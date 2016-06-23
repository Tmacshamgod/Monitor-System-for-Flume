import json

_servers = {}

def load_servers():
    server_file = "conf/server.json"
    try:
        servers = json.load(open(server_file, "r"))
        if not servers:
            return None
        global _servers
        for server in servers:
            ip = server.get("ip")
            if not ip:
                return None
            role = server.get("role")
            if not role:
                return None
            threshold = server.get("threshold")
            if not threshold:
                threshold = 1000
            _servers[ip] = {
                                "role": role,
                                "threshold": threshold
                           }
        return _servers
    except Exception, e:
        print str(e)
        return None