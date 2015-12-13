# meds/rest.py
#
#

""" rest interface. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.scheduler import launcher
from meds.object import Object
from meds.store import Store
from meds import __version__
from meds.misc import root
from meds.cfg import cfg

import logging
import time

from http.server import HTTPServer, BaseHTTPRequestHandler

port = 10102
server = None
store = Store()

def init(mods):
    server = REST((cfg.rest.hostname, int(cfg.main.port or cfg.rest.port)), RESTHandler)
    launcher.launch(server.start)

class REST(HTTPServer, Object):

    allow_reuse_address = True
    daemon_thread = True

    def __init__(self, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        Object.__init__(self)
        self.host = args[0]
        self._status = "start"
        self._last = time.time()
        self._start = time.time()

    def exit(self):
        logging.warn("# REST/end")
        self._status = ""
        time.sleep(0.2)
        self.shutdown()

    def start(self): 
        logging.warn("# REST/start http://%s:%s" % self.host)
        self._status = "ok"
        self.ready()
        self.serve_forever()

    def request(self):
        self._last = time.time()

    def error(self, request, addr):
        ex = get_exception()
        logging.warn('# REST/error %s error %s' % (addr, ex))

class RESTHandler(BaseHTTPRequestHandler):

    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self._ip = self.client_address[0]
        self._size = 0

    def write_header(self, type='text/plain'):
        self.send_response(200)
        self.send_header('Content-type', '%s; charset=%s ' % (type, "utf-8"))
        self.send_header('Server', __version__)
        self.end_headers()

    def do_GET(self):
        filename = ""
        for fn in store.all():
            if fn.endswith(self.path): filename = fn ; break
        try: f = open(fn, "r") ; txt = f.read() ; f.close()
        except (TypeError, FileNotFoundError): self.send_response(404) ; self.end_headers() ; return
        txt = txt.replace("\\n", "\n")
        txt = txt.replace("\\t", "\t")
        self.write_header()
        self.wfile.write(bytes(txt, "utf-8"))
        self.wfile.flush()

    def log(self, code): logging.warn('# REST/log %s code %s path %s' % (self.address_string(), code, self.path))

