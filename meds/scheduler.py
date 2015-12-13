# scheduler.py
#
#

""" the schaeduler. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.errors import EDISPATCHER, EDISCONNECT, EFUNC, EREGISTER, EJSON, EATTRIBUTE
from meds.misc import elapsed, name, get_exception
from meds.object import Object
from meds.mods import Mods

import collections
import threading
import logging
import random
import types
import queue
import time
import os

class Task(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.type = "Task"
        self._ready = threading.Event()
        self._queue = queue.Queue()
        self._start = time.time()
        self._last = time.time()
        self._status = "start"
        self.kwargs = kwargs
        self.setDaemon(True)
        self.once = True
        
    def __iter__(self):
        for x in dir(self): yield x

    def isSet(self): return self._ready.isSet()

    def ready(self): self._ready.set()

    def clear(self): self._ready.clear()

    def wait(self, sec=180.0): self._ready.wait(sec)

    def put(self, func, *args):
        self._queue.put_nowait((func, args))
        return self

    def run(self):
        self._status = "working"
        while self._status:
            _func, args  = self._queue.get()
            if not self._status: break
            if not _func: break
            self.clear()
            self._name = name(_func)
            self.setName(self._name)
            self._begin = time.time()
            try: _func(*args)
            except Exception as ex: logging.error("& %s %s" % (str(ex), get_exception()))
            self._status = "ready"
            self._last = time.time()
            logging.info("! Task.finish %s %.6ss" % (self._name, self._last - self._begin))
            try: args[0].ready()
            except IndexError: pass
            if "once" in self and self.once: break

    def exit(self):
        self._status = ""
        self.put(None, None)

class Launcher(Object):

    cc = "!"
    default = ""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._status = "init"
        self.tasks = []

    def launch(self, *args, **kwargs):
        logging.info("! %s.launch %s" % (self.type, args[0].__name__))
        t = Task(**kwargs)
        t.start()
        t.once = True
        return t.put(*args, **kwargs)

    def kill(self, name):
        for thr in self.running(name):
            if "exit" in dir(thr): thr.exit()
            elif "cancel" in dir(thr): thr.cancel() 
            else: thr.join(1.0)

    def running(self, name=""):
        for thr in threading.enumerate():
            if str(thr).startswith("<_"): continue
            if name and name not in str(thr): continue
            yield thr

class Scheduler(Object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue = queue.Queue()
        self._status = "init"
        self._start = time.time()

    def dispatch(self, event):
        from meds.mods import cmnds
        func = cmnds.get(event.cmnd)
        if func: launcher.launch(func, event)
        else: event.ready()

    def put(self, event):
        if self._status == "init": launcher.launch(self.loop) ; self._status = "loop"
        self._queue.put_nowait(event)

    def loop(self): 
        logging.warn("# Scheduler.loop")
        self._status = "running" 
        while self._status:
            event = self._queue.get()
            if event: self.dispatch(event)

    def stop(self): self._status = "" ; self.put(None)

launcher = Launcher()
scheduler = Scheduler()
