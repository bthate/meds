# xmpp.py
#
#

""" xmpp bot. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.scheduler import launcher, scheduler
from meds.misc import get_exception
from meds.object import Object
from meds.store import Store
from meds.event import Event
from meds.bots import Bot
from meds.cfg import cfg

import threading
import logging
import getpass
import queue

def init(mods):
    store = Store()
    cfg = store.last("cfg", "xmpp")
    if not cfg: cfg = cfg.xmpp ; cfg.save()
    password = getpass.getpass()
    xmpp = XMPP(cfg.user, password)
    xmpp.update(cfg)
    launcher.launch(xmpp.core)
    launcher.launch(xmpp.loop)
    launcher.launch(xmpp.start)

class XMPP(Bot):

    cc = "none"
    default = ""

    def __init__(self, jid, password):
        super().__init__()
        import sleekxmpp
        self._queue = queue.Queue()
        self.type = self.__class__.__name__
        self.client = sleekxmpp.clientxmpp.ClientXMPP(jid, password)
        self.register("session_start", self.session_start)
        self.register("message", self.messaged)
        self.register('disconnected', self.disconnected)
        self.register('connected', self.connected)
        self.register('presence_available', self.presenced)
        self.register('presence_dnd', self.presenced)
        self.register('presence_xa', self.presenced)
        self.register('presence_chat', self.presenced)
        self.register('presence_away', self.presenced)
        self.register('presence_unavailable', self.presenced)
        self.register('presence_subscribe', self.presenced)
        self.register('presence_subscribed', self.presenced)
        self.register('presence_unsubscribe', self.presenced)
        self.register('presence_unsubscribed', self.presenced)
        self.register('groupchat_message', self.messaged)
        self.register('groupchat_presence', self.presenced)
        self.register('groupchat_subject', self.presenced)
        self.register('failed_auth', self.failedauth)
        self.client.exception = self.exception
        self.client.use_signals()
        self._connected = threading.Event()
        self.channels = []
        self.user = jid

    def register(self, key, value):
        logging.info("# %s.register %s" % (self.type, key))
        self.client.add_event_handler(key, value)

    def start(self):
        try: self.connect()
        except: raise

    def exit(self):
        self.client.disconnect()
        super().stop()
        self._queue.put(None)

    def dispatch(self, event):
        if event.cmnd: self.handlers[event.cmnd](event)

    def event(self): return self._queue.get()

    def core(self): self.client.process()

    def say(self, jid, txt):
        txt = str(txt)
        self.client.send_message(jid, txt)
        logging.info("> %s.say %s" % (self.type, jid))

    def announce(self, txt):
        for channel in self.channels: self.say(channel, txt)

    def out(self, txt):
        logging.info("> %s.write %s" % (self.type,  txt))
        self.client.send_raw(txt)

    def connect(self):
        logging.warn("# %s.connect %s" % (self.type, self.user))
        if cfg.main.openfire:
            logging.warn("# %s.openfire" % self.type)
            self.client.ssl_version = ssl.PROTOCOL_SSLv3
            self.client.connect((self.server, cfg.xmpp.port), use_ssl=True)
        else: self.client.connect()

    def session_start(self, data):
        self.client.send_presence()
        self.ready()
        logging.warn("# %s.session %s" % (self.type, self.user))
         
    def exception(self, data):
        self._error = data
        logging.error("^ %s.error %s"% (self.type, str(data)))

    def failedauth(self, data):
        self._error = data
        logging.error("^ %s.auth %s" % (self.type, str(data)))

    def failure(self, data):
        self._error = data
        logging.error("^ %s.error %s" % (self.type, str(data)))

    def disconnected(self, data):
        self._connected.clear()
        self._status = "disconnect"
        logging.warn("^ %s.disconnect %s" % (self.type, self.user))

    def connected(self, data): 
        self._status = "connected"
        self._connected.set()
        logging.warn("# %s.connected %s" % (self.type, self.user))

    def messaged(self, data):
        from meds.mods import cmnds
        logging.debug("< %s.read %s" % (self.type, data))
        m = Event()
        m.update(data)
        m._bot = self
        if m.type == "error": logging.error("^ %s" % m.error) ; return
        m.cc = self.cc
        m["from"] = str(m["from"])
        if self.user in m["from"]: logging.info("< %s.%s %s" % (self.type, m.type, m["from"])) ; return
        m.origin = m["from"]
        m.channel = m.origin
        m.to = m.origin
        m.element = "message"
        m.txt = m["body"]
        if '<delay xmlns="urn:xmpp:delay"' in str(data):
            logging.info("# %s.ignore %s %s" % (self.type, m.type, m.origin))
            return
        logging.info("< %s.%s %s" % (self.type, m.type, m.origin))
        m.parse()
        func = cmnds.get(m.cmnd)
        if func: func(m)

    def presenced(self, data):
        from meds.mods import cmnds
        logging.debug("< %s.read %s" % (self.type, data))
        o = Event()
        o.update(data)
        o._bot = self
        o["from"] = str(o["from"])
        o.origin = o["from"]
        if "txt" not in o: o.txt = ""
        o.element = "presence"
        if o.type == 'subscribe':
            pres = Event({'to': o["from"], 'type': 'subscribed'})
            self.client.send_presence(pres)
            pres = Event({'to': o["from"], 'type': 'subscribe'})
            self.client.send_presence(pres)
        elif o.type == "unavailable" and o.origin in self.channels: self.channels.remove(o.origin)
        elif o.origin != self.user and o.origin not in self.channels: self.channels.append(o.origin)
        o.no_dispatch = True
        logging.info("< %s.%s %s" % (self.type, o.type, o.origin))
        o.parse()
        func = cmnds.get(o.cmnd)
        if func: func(o)
