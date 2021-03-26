from os.path import abspath, dirname, join
import json

from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError

import logging

from uprwebsocket.udp_socket import *
#from uprwebsocket.http_socket import *

logger = logging.getLogger("net2js")

__all__ = ["WSHandler", "NonCachingStaticFileHandler"]

class WSHandler(WebSocketHandler):
    def open(self):
        #print('new connection')
        logger.info("UPRWebsocket opened")
        #UPD_Connect()
        self.ioloop = IOLoop.current()
      
    def on_message(self, data):
        #print('data received:  {}'.format(data))
        # Reverse Message and send it back
        #sendData(data)
        #sendJson(data)
        #self.write_message("UDP recived: {}".format(data))
        self.write_message("Recived {}".format(data));


    def send_msg(self, msg):
        try:
            self.write_message(msg, False)
        except WebSocketClosedError:
            logger.warn("websocket closed when sending message")
 
    def on_close(self):
        logger.info("UPRWebsocket closed")
        #print('connection closed')

    def send_msg_threadsafe(self, data):
        self.ioloop.add_callback(self.send_msg, data)

 
    def check_origin(self, origin):
        return True


class NonCachingStaticFileHandler(StaticFileHandler):
    """
        This static file handler disables caching, to allow for easy
        development of your Dashboard
    """

    # This is broken in tornado, disable it
    def check_etag_header(self):
        return False

    def set_extra_headers(self, path):
        # Disable caching
        self.set_header(
            "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
        )
