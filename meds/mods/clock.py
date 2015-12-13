# clock.py
#
#

""" timer, repeater and other clock based classes. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.misc import get_day, get_hour, today
from meds.object import Object
from meds.event import Event
from meds.store import Store
from meds.scheduler import launcher

import threading
import logging
import time

def register(mods): mods.register("timer", timer)

def init(mods):
    store = Store()
    for fn in store.all("timer"):
        o = Event().load(fn)
        if "time" not in o: continue
        if time.time() < int(o.time):
            timer = Timer(int(o.time), o)
            launcher.launch(timer.start)

class Timer(Object):

    def __init__(self, time_alarm, event):
        super().__init__()
        self.sleep = time_alarm - time.time()
        self.event = event

    def start(self):
        self._timer = threading.Timer(self.sleep, self.echo)
        self._timer.setDaemon(True)
        self._timer.setName(self.echo.__name__)
        self._timer._start = time.time()
        self._timer._last = time.time()
        self._timer._status = "ok"
        self._timer.sleep = self.sleep
        self._timer.start()

    def echo(self):
        kernel.announce(self.event.txt)
        self.event.done = True
        self.event.sync()

    def exit(self):
        self._timer._status = "stopped"
        self._timer.cancel()

class Repeater(Object):

    def __init__(self, sleep, func, **kwargs):
        if not sleep: raise ValueError()
        e = Event(**kwargs)
        super().__init__()
        self.func = func
        self.sleep = sleep
        self._start = time.time()
        self._status = "start"
        self._name = e.name or func.__name__
       
    def start(self):
        self._timer = threading.Timer(self.sleep, self.run)
        self._timer.setDaemon(True)
        self._timer.setName(self._name)
        self._timer._nrs = Object()
        self._timer._nrs.loops = 0
        self._timer._start = time.time()
        self._timer._last = time.time()
        self._timer._status = "ok"
        self._timer.sleep = self.sleep
        self._timer.start()

    def run(self, **kwargs):
        self.start()
        self._timer._status = "ok"
        self._timer._nrs.loops += 1
        event = Event()
        event.name = self._name
        event.origin = "clock@bot"
        self.func(event.parse())
 
    def exit(self):
        self._status = ""
        self._timer.cancel()

def timer(event):
    if not event.rest: return
    day = get_day(event.rest) or today()
    hour = get_hour(event.rest)
    target = day + get_hour(event.rest)
    if time.time() > target: event.reply("already passed given time.") ; return
    event.reply("time is %s" % time.ctime(target))
    e = Event()
    e._bot = event._bot
    e.services = "clock"
    e.prefix = "timer"
    e.txt = event.rest
    e.time = target
    e.done = False
    e.save()
    timer = Timer(target, e.parse())
    launcher.launch(timer.start)
    e.ok()
