# mods.py
#
#

""" runtime namespace. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.object import Object
from meds.log import loglevel
from meds.misc import hello
from meds.cfg import cfg

import importlib
import logging
import pkgutil
import queue
import os

class Mods(Object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = self.__class__.__name__
        self.handlers = Object()

    def init(self):
        self.clear()
        for mod in cfg.main.packages:
            if mod: self.walk(mod, cfg.main.modules) 
        for mod in cfg.main.modules.split(","):
            if not mod: continue
            self[mod] = self.load(mod)
        for mod in cfg.main.init.split(","):
            if not mod: continue
            for m in self.search(mod):
                self[m] = self.load(m)  
        for mod in cfg.main.default:
            if not mod: continue
            self.call(mod, "register")
            self.call(mod, "init")
        for mod in cfg.main.modules.split(","):
            if not mod: continue
            for m in self.search(mod):
                self.call(m, "register")
                self.call(m, "init")
        for mod in cfg.main.init.split(","):
            if not mod: continue
            for m in self.search(mod): self.call(m, "init")
        self.ready()

    def register(self, key, val): self.handlers[key] = val ; logging.info("! %s.register %s" % (self.type, key))

    def call(self, name, funcname):
        logging.info("! %s.%s %s" % (self.type, funcname, name.split(".")[-1]))
        func = getattr(self[name], funcname, None)
        if func: func(self)

    def load(self, name, package=None, force=False):
        if name in self and not force: mod = importlib.reload(self[name])
        else: mod = importlib.import_module(name, package)
        return mod

    def get(self, cmnd):
        if cmnd in self.handlers: return self.handlers[cmnd] 

    def reload(self, name):
        for n in self.search(name):
            self.call(n, "stop")
            self[n] = self.load(name)
            self.call(n, "register")
            self.call(n, "init")
     
    def walk(self, name, force=[]):
        from meds.cfg import cfg
        self[name] = mod = self.load(name)
        if "__path__" in dir(mod):
            for pkg in sorted(pkgutil.walk_packages(mod.__path__, name + ".")):
                n = pkg[1]
                if n in cfg.main.exclude and n not in force: logging.warn("skip %s" % n) ; continue
                self[n] = self.load(n)
                self.call(n, "register")
        return self[name]

cmnds = Mods()
