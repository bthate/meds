# meds/bots/cli.py
#
#

""" console line interface bot. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.scheduler import scheduler, launcher
from meds.misc import parse_cli
from meds.object import Object
from meds.event import Event
from meds.mods import cmnds
from meds.bots import Bot
from meds.cfg import cfg

import logging
import time
import sys

class CLI(Bot):

    cc = "none"
    default = ""

    def dispatch(self, event): scheduler.put(event) ; event.wait()

    def event(self):
        event = Event()
        event._bot = self
        event.txt = input(self.prompt())
        event.origin = "root@shell"
        event.parse()
        return event

    def out(self, txt):
        sys.stdout.write(str(txt))
        sys.stdout.write("\n")

    def announce(self, txt): self.out(txt)

    def say(self, channel, txt): self.out(txt)

    def prompt(self): 
        from meds.defines import GREEN, ENDC
        date = time.ctime(time.time()).split()[-2]
        if cfg.main.colors: txt = "%s %s<%s " % (date, GREEN, ENDC) 
        else: txt = "%s < " % date
        return txt

    def start(self):
        parse_cli()
        cmnds.init()
        if not cfg.main.shell:
            txt = " ".join(cfg.main.args)
            if txt: event = self.cmnd(txt) ; event.wait()
            return
        super().start()
        
    def join(self, channel): pass
