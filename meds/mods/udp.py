# meds/udp.py
#
#

""" relay txt through a udp port listener. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.scheduler import launcher
from meds.rijndael import rijndael
from meds.object import Object
from meds.bots import fleet
from meds.misc import name
from meds.cfg import cfg

import logging
import socket
import time

crypt = rijndael(cfg.udp.seed)

objs = Object()

def init(mods):
    objs.udp = UDP()
    launcher.launch(objs.udp.start)

def stop():
    if "udp" in objs: objs.udp.exit()
    
class UDP(Object):

    def __init__(self):
        Object.__init__(self)
        self._status = "start"
        self._start = time.time()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try: self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except: pass
        self._sock.setblocking(1)

    def start(self):
        self._sock.bind((cfg.udp.host, cfg.udp.port))
        logging.warn("# UDP/start %s:%s" % (cfg.udp.host, cfg.udp.port)) 
        self.ready()
        self._status = "ok"
        while self._status:
            input, addr = self._sock.recvfrom(64000)
            if not self._status: break
            input = str(input.rstrip(), "utf-8")
            data = ""
            for i in range(int(len(input)/16)):
                txt = input[i*16:i*16+16]
                try: data += crypt.decrypt(txt)
                except Exception as ex: logging.error(get_exception()) ;  break
            if not data: break
            self.output(data, addr)
        
    def exit(self):
        logging.warn("# exit %s" % name(self))
        self._status = ""
        self._sock.settimeout(1.0)
        self._sock.sendto(bytes("bla", "utf-8"), (cfg.udp.host, cfg.udp.port))

    def output(self, input, addr):
        passwd, text = input.split(" ", 1)
        text = text.replace("\00", "")
        if passwd == cfg.udp.password:
            for bot in fleet: bot.announce(text)

