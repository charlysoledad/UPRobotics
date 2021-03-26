import os
from os.path import abspath, dirname, exists, join
import tornado.httpserver
import tornado.websocket
import tornado.web
from tornado.ioloop import IOLoop

import socket

from . import NonCachingStaticFileHandler, WSHandler

import logging

logger = logging.getLogger("dashboard")

log_datefmt = "%H:%M:%S"
log_format = "%(asctime)s:%(msecs)03d %(levelname)-8s: %(name)-20s: %(message)s"

def main():


    www_dir = abspath(os.getcwd())
    index_html = join(www_dir, "index.html")

    if not exists(www_dir):
        logger.error("Directory '%s' does not exist!", www_dir)
        exit(1)

    if not exists(index_html):
        logger.warn("%s not found", index_html)

    app = tornado.web.Application(
        [
            (r"/ws", WSHandler),
            (r"/()", NonCachingStaticFileHandler, {"path": index_html}),
            (r"/(.*)", NonCachingStaticFileHandler, {"path": www_dir}),
        ]
    )

    
    # Start the app
    logger.info("Listening on http://localhost:%s/", '8888')

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at {}***'.format(myIP))
    IOLoop.current().start()
 
if __name__ == "__main__":
    main()
 