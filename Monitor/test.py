import tornado.ioloop

def callback():
    print "DO SOMETHING HERE"


if __name__ == "__main__":
    interval_ms = 1000
    main_loop = tornado.ioloop.IOLoop.instance()
    scheduler = tornado.ioloop.PeriodicCallback(callback, interval_ms)
    scheduler.start()
    main_loop.start()