# object.py
#
#

""" dict with dotted name access. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.errors import EJSON, ENOTSET, EATTRIBUTE
from meds.misc import urled, root, signature, dumps, slice
from meds.misc import list_files, cdir
from meds.misc import fn_time, rtime
from meds.misc import path as dopath
from meds.misc import locked, headertxt, j
from meds.misc import locked

import threading
import hashlib
import logging
import inspect
import errno
import fcntl
import types
import json
import time
import os

class OO(list): pass

class Object(dict):

    def __getattribute__(self, name):
        try: val = self[name]
        except KeyError: val = super().__getattribute__(name)
        return val

    def __getattr__(self, name):
        if name == "modname": return self.__class__.__module__
        if name == "name": return repr(self)
        if name == "url": return urled(self)
        if name == "type": return self.__class__.__name__
        if name == "_ready":  self._ready = threading.Event()
        if name not in self: raise AttributeError(name)
        return self[name]

    def __setitem__(self, name, value):
        return dict.__setitem__(self, name, value)

    def __setattr__(self, name, value):
        try:
            val = super().__getattribute__(name)
            if inspect.ismethod(val): raise AttributeSet        
        except: pass
        return dict.__setitem__(self, name, value)

    def __contains__(self, name):    
        try: self[name] ; return True
        except KeyError: return False

    def search(self, name):
        for key in self.keys():
            if key.startswith("_"): continue
            if name == key.split(".")[-1]: yield key

    def blaet(self): return self.json(indent=4, sort_keys=True)

    def json(self, *args, **kwargs): return dumps(self, *args, **kwargs)

    def load(self, path=""):
        if not path: path = self._path
        ondisk = self.read(path)
        fromdisk = json.loads(ondisk)
        if "data" in fromdisk: self.update(fromdisk["data"])
        else: self.update(fromdisk)
        if "saved" in fromdisk: self.saved = fromdisk["saved"]
        self._path = path
        return self

    def read(self, path):
        try: f = open(path, "r", encoding="utf-8")
        except IOError as ex:
            if ex.errno == errno.ENOENT: return "{}"
            raise
        res = ""
        for line in f:
            if not line.strip().startswith("#"): res += line
        if not res.strip(): return "{}"
        f.close()
        return res

    def prepare(self):
        todisk = Object()
        todisk.data = slice(self)
        todisk.saved_from = self.__class__.__module__
        todisk.type = self.__class__.__name__
        todisk.saved = self.saved = time.ctime(time.time())
        todisk.signature = signature(todisk.data)
        try: result = dumps(todisk, indent=4, ensure_ascii=False, sort_keys=True)
        except TypeError: raise NoJSON()
        return result

    def save(self, stime=""):
        if not stime: stime = rtime()
        path = j(dopath(self), stime)
        self.sync(path)
        return stime

    @locked
    def sync(self, path=""):
        if not path:
            try: path = self._path
            except AttributeError: pass
        if not path: path = self._path = j(dopath(self), rtime())
        logging.warn("! sync %s" % path)
        d, fn = os.path.split(path)
        cdir(d)
        todisk = self.prepare()
        datafile = open(os.path.abspath(path) + ".tmp", 'w')
        fcntl.flock(datafile, fcntl.LOCK_EX | fcntl.LOCK_NB)
        datafile.write(headertxt % "%s characters" % len(todisk))
        datafile.write(todisk)
        datafile.write("\n")
        fcntl.flock(datafile, fcntl.LOCK_UN)
        datafile.close()
        os.rename(path + ".tmp", path)
        return path

    def isSet(self): return self._ready.isSet()

    def ready(self): logging.info("! %s.ready" % self.type) ; self._ready.set()

    def clear(self): self._ready.clear()

    def wait(self, sec=180.0): logging.info("! %s.wait" % self.type) ; self._ready.wait(sec)
