import sys
import webservice
import loop_check

def start_to_monitor():
    return loop_check.start_loop_query()

def start_http_server(port):
    return webservice.start(port)

def main(args):
    if not start_to_monitor():
        print "failed to start monitoring"
    return start_http_server(11003)

if __name__ == "__main__":
    main(sys.argv)