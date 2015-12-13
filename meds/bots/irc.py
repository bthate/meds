# irc.py
#
#

""" internet relay chat bot. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.misc import split_txt, get_exception
from meds.scheduler import launcher, scheduler
from meds.errors import EDISCONNECT
from meds.object import Object
from meds.store import Store
from meds.event import Event
from meds.bots import Bot
from meds.cfg import cfg

from meds import __version__

import logging
import _thread
import random
import socket
import queue
import time
import ssl
import sys
import re
import io

def init(mods):
    store = Store()
    ncfg = store.last("cfg", "irc")
    if not ncfg: ncfg = cfg.irc ; ncfg.save()
    bot = IRC(ncfg)
    bot.connecting()
    launcher.launch(bot.push)
    launcher.launch(bot.loop)
    launcher.launch(bot.start)

class IRC(Bot):

    default = ""
    marker = "\r\n"
    cc = "!"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = _thread.allocate_lock()
        self._outqueue = queue.Queue()
        self._sock = None
        self._buffer = []
        self._lastline = ""
        self._error = ""
        self._status = "start"
        self.handlers = Object()
        self.type = self.__class__.__name__
        self.register("004", self.connected)
        self.register("ERROR", self.errored)
        self.register("366", self.h366)
        self.register("433", self.h433)
        self.register("513", self.h513)
        self.register("PING", self.pinged)
        self.register("PONG", self.ponged)
        self.register("QUIT", self.quited)
        self.register("INVITE", self.invited)
        self.register("PRIVMSG", self.privmsged)
        self.register("NOTICE", self.noticed)
        self.register("JOIN", self.joined)
        self.channels = []
        self.encoding = "utf-8"
        if "realname" not in self: self.realname = "meds"
        if "username" not in self: self.username = "meds"
        if "server" not in self: self.server = "localhost"
        if "port" not in self: self.port = 6667
        if "nick" not in self: self.nick = "meds"
        if "channel" in self: self.channels.append(self.channel)

    def register(self, key, value): self.handlers[key] = value

    def dispatch(self, event):
        if event.cmnd in self.handlers: self.handlers[event.cmnd](event)
        
    def exit(self): self.quit()

    def parse(self, txt):
        rawstr = str(txt)
        logging.debug("< %s/parse %s" % (self.type, rawstr))
        obj = Event()
        obj._bot = self
        obj.arguments = rawstr.split(":")[0].split()
        if not obj.arguments: obj.arguments = rawstr.split(":")[1].split()
        obj.txt = rawstr.split(":", 2)[-1]
        if rawstr[0] == ":": obj.origin = obj.arguments[0] ; obj.cmnd = obj.arguments[1]
        else: obj.origin = self.server ; obj.cmnd = obj.arguments[0]
        try: obj.nick, obj.userhost = obj.origin.split("!")
        except: pass
        obj.target = obj.arguments[-1]
        if obj.target.startswith("#"): obj.channel = obj.target
        return obj

    def event(self):
        if not self._buffer: self.some()
        line = self._buffer.pop(0)
        return self.parse(line.rstrip())

    def some(self):
        if "ssl" in self and self.ssl: inbytes = self._sock.read()
        else: inbytes = self._sock.recv(512)
        txt = str(inbytes, self.encoding)
        if txt == "": raise EDISCONNECT()
        self._lastline += txt
        splitted = self._lastline.split(self.marker)
        for s in splitted[:-1]:
            self._buffer.append(s)
            if "PING" not in s or "PONG" not in s: logging.info("< %s.read %s" % (self.type, s.strip()))
        self._lastline = splitted[-1]

    def push(self):
        while self._status:
            args = self._outqueue.get()
            if not args or not self._status: break
            self.output(*args)

    def announce(self, txt):
        for channel in self.channels: self._outqueue.put((channel, txt))

    def say(self, channel, txt): self._outqueue.put((channel, txt))
 
    def output(self, channel, txt):
        txt_list = split_txt(txt)
        for txt in txt_list:
            nr = 0
            for t in txt.split("\n"):
                if not t: continue
                tt = t.strip()
                if not tt: continue
                self.privmsg(channel, tt)
                if nr: time.sleep(3.0)
                nr += 1

    def out(self, txt):
        if not txt.endswith(self.marker): txt += self.marker
        txt = txt[:512]
        txt = bytes(txt, "utf-8")
        logging.info("> %s.out %s" % (self.type, txt))
        try:
            if 'ssl' in self and self.ssl: self._sock.write(txt)
            else: self._sock.send(txt)
        except: pass

    def connecting(self):
        self._status = "connect"
        res = None
        while self._status:
            try: self.connect() ; break
            except Exception as ex: logging.error(get_exception()) ; time.sleep(10)
        self._status = "ok"
        time.sleep(1)
        self.logon()
        return res

    def connect(self):
        self.stopped = False
        logging.warn("# %s.connect to %s" % (self.type, self.server))
        if "ipv6" in self: self._oldsock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else: self._oldsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = self.bind()
        self._oldsock.settimeout(60)
        self._oldsock.connect((self.server, int(str(self.port or 6667))))
        self.blocking = True
        self._oldsock.setblocking(self.blocking)
        self._oldsock.settimeout(700.0)
        self.fsock = self._oldsock.makefile("r")
        if 'ssl' in self and self['ssl']: self._sock = ssl.wrapsocket(self._oldsock)
        else: self._sock = self._oldsock
        return True

    def logon(self, *args):
        self.out("NICK %s" % self.nick or "meds")
        self.out("USER %s localhost %s :%s" % (self.username or "meds", self.server or "localhost", self.realname or "meds"))

    def bind(self):
        server = self.server
        try: self._oldsock.bind((server, 0))
        except socket.error:
            if not server:
                try: socket.inet_pton(socket.AF_INET6, self.server)
                except socket.error: pass
                else: server = self.server
            if not server:
                try: socket.inet_pton(socket.AF_INET, self.server)
                except socket.error: pass
                else: server = self.server
            if not server:
                ips = []
                try:
                    for item in socket.getaddrinfo(self.server, None):
                        if item[0] in [socket.AF_INET, socket.AF_INET6] and item[1] == socket.SOCK_STREAM:
                            ip = item[4][0]
                            if ip not in ips: ips.append(ip)
                except socket.error: pass
                else: server = random.choice(ips)
        return server

    def close(self):
        if 'ssl' in self and self['ssl']: self.oldsock.shutdown(1) ; self.oldsock.close()
        else: self._sock.shutdown(1) ; self._sock.close()
        self.fsock.close()

    def join(self, channel, password=""):
        logging.warn("# %s.join %s" % (self.type, channel)) 
        if password: self.out('JOIN %s %s' % (channel, password))
        else: self.out('JOIN %s' % channel)

    def joinall(self):
        for channel in self.channels: self.join(channel)

    def part(self, channel):
        self.out('PART %s' % channel)
        if channel in self.channels:
            self.channels.remove(channel)
            self.save()

    def donick(self, name): self.out('NICK %s\n' % name[:16]) ; self.nick = name

    def who(self, channel): self.out('WHO %s' % channel)

    def names(self, channel): self.out('NAMES %s' % channel)

    def whois(self, nick): self.out('WHOIS %s' % nick)

    def privmsg(self, channel, txt): self.out('PRIVMSG %s :%s' % (channel, txt))

    def voice(self, channel, nick): self.out('MODE %s +v %s' % (channel, nick))

    def doop(self, channel, nick): self.out('MODE %s +o %s' % (channel, nick))

    def delop(self, channel, nick): self.out('MODE %s -o %s' % (channel, nick))

    def quit(self, reason='https://pikacode.com/bart/meds'): self.out('QUIT :%s' % reason)

    def notice(self, channel, txt): self.out('NOTICE %s :%s' % (channel, txt))

    def ctcp(self, nick, txt): self.out("PRIVMSG %s :\001%s\001" % (nick, txt))

    def ctcpreply(self, channel, txt): self.out("NOTICE %s :\001%s\001" % (channel, txt))

    def action(self, channel, txt): self.out("PRIVMSG %s :\001ACTION %s\001" % (channel, txt))

    def getchannelmode(self, channel): self.out('MODE %s' % channel)

    def settopic(self, channel, txt): self.out('TOPIC %s :%s' % (channel, txt))

    def ping(self, txt): self.out('PING :%s' % txt)

    def pong(self, txt): self.out('PONG :%s' % txt)

    def noticed(self, event): pass

    def connected(self, event):
        if "servermodes" in self: self.out("MODE %s %s" % (self.nick, self.servermodes))
        logging.warn("# %s.connected with %s" % (self.type, self.server))
        self.joinall()

    def invited(self, event): self.join(event.channel)

    def joined(self, event):
        if event.channel not in self.channels: self.channels.append(event.channel)

    def errored(self, event):
        logging.error("%s.error %s" % (self.type, event.txt))
        self._error = event.txt.strip()
        self._status = "error"

    def pinged(self, event):
        self.pongcheck = True
        self.pong(event.txt)

    def ponged(self, event): pass 

    def quited(self, event):
        if "Ping timeout" in event.txt and event.nick == self.nick: self.connecting()

    def privmsged(self, event):
        if event.txt.startswith("\001DCC"): self.dccconnect(event) ; return
        elif event.txt.startswith("\001VERSION"): self.ctcpreply(event.nick, "VERSION MEDS #%s - http://pypi.python.org/pypi/meds" % __version__) ; return
        if event.txt and event.txt[0] == self.cc or event.txt.startswith(self.nick):
            event.parse()
            scheduler.put(event)

    def ctcped(self, event): pass

    def h366(self, event): pass 

    def h433(self, event): self.donick(event.target + "_")
      
    def h513(self, event): self.out("PONG %s" % event.arguments[6])

    def dcced(self, event, s):
        s.send(bytes('Welcome to MEDS ' + event.nick + " !!\n", self.encoding))
        launcher.launch(self.dccloop, event, s)

    def dccloop(self, event, s):
        from meds.mods import cmnds
        sockfile = s.makefile('rw')
        s.setblocking(True)
        while 1:
            try:
                res = sockfile.readline()
                if not res: break
                res = res.rstrip()
                logging.info("< %s.loop %s" % (self.type, event.origin))
                e = Event()
                e._bot = self
                e.txt = res
                e.outer = sockfile
                e.origin = event.origin
                e.parse()
                func = cmnds.get(e.cmnd)
                if func: func(e)
            except socket.timeout: time.sleep(0.01)
            except socket.error as ex:
                if ex.errno in [socket.EAGAIN, ]: continue
                else: raise
            except Exception as ex: logging.error(get_exception())
        sockfile.close()

    def dccconnect(self, event):
        event.parse()
        try:
            addr = event.args[2] ; port = event.args[3][:-1]
            port = int(port)
            if re.search(':', addr): s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            else: s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((addr, port))
        except Exception as ex: logging.error(get_exception()) ; return
        self.dcced(event, s)
