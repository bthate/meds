# meds/bots/__init__.py
#
#

""" base class. """

from meds.misc import make_opts, opts_defs, hello
from meds.errors import EIMPLEMENTED, EDISCONNECT
from meds.scheduler import Scheduler, launcher, scheduler
from meds.object import OO, Object
from meds.log import loglevel
from meds.mods import cmnds
from meds.cfg import cfg

import logging
import time
import os

class Bot(Scheduler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channels = []
        self.type = self.__class__.__name__
        self.handlers = Object()
        fleet.append(self)

    def start(self):
        logging.warn("# %s.start" % self.type)
        self._start = time.time() 
        self._status = "ready"
        while self._status:
            try:
                event = self.event()
                if event: self.dispatch(event)
            except EDISCONNECT: time.sleep(5) ; self.connecting() ; continue
            except (EOFError, KeyboardInterrupt): raise

    def cmnd(self, txt, bot=None): 
        from meds.event import Event
        event = Event()
        event.origin = "user@bot"
        event._bot = self
        event.txt = txt
        event.parse()
        scheduler.put(event)
        return event

    def event(self): raise EIMPLEMENTED

    def exit(self): raise EIMPLEMENTED

    def out(self, txt): raise EIMPLEMENTED

    def say(self, channel, txt): raise EIMPELMENTED

    def announce(self, txt): raise EIMPLEMENTED

    def join(self, channel): raise ENOMETHOD("join")

    def joinall(self):
        for channel in self.channels: self.join(channel)

fleet = OO()
