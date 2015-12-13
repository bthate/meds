# store.py
#
#

""" read files from disk. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.misc import path, timed, fn_time, short_date, selector, wanted, notwanted
from meds.object import Object
from meds.event import Event
from meds.cfg import cfg

import logging
import mailbox
import time
import glob
import os

class Store(Object):

    def list(self, path, *args, **kwargs):
        p = Event(kwargs).parse()
        if args: prefix = args[0]
        else: prefix = ""
        res = []
        if not path.endswith(os.sep): path += os.sep
        if prefix and os.path.isdir(path + prefix + os.sep): path += prefix + os.sep
        if "*" not in path: path += "*"
        for fnn in sorted(glob.glob(path)):
            if not prefix and p.time not in fnn: continue
            if os.path.isdir(fnn): res.extend(self.list(fnn, **kwargs)) ; continue
            else: res.append(fnn) 
        return res 

    def all(self, *args, **kwargs):
        p = path(self)
        return sorted(self.list(p, *args, **kwargs), key=lambda x: fn_time(x))

    def selected(self, event):
        objs = []
        uniqlist = []
        start = time.time()
        for fn in self.all(*event.args):
            try: obj = Object().load(fn)
            except: logging.warn("fail %s" % fn) ; continue
            if "deleted" in obj and obj.deleted: continue
            if not selector(obj, event.args): continue
            if not wanted(obj, event.want): continue
            if notwanted(obj, event.notwant): continue
            yield obj

    def first(self, *args, **kwargs):
        fns = self.all(*args, **kwargs)
        for fn in fns:
            obj = Object().load(fn)
            if "deleted" in obj and obj.deleted: continue
            if args and len(args) > 1 and args[1] != obj.get(args[0], ""): continue
            return obj

    def last(self, *args, **kwargs):
        fns = self.all(*args, **kwargs)[::-1]
        res = None
        for fn in fns[::-1]:
            obj = Object().load(fn)
            if "deleted" in obj and obj.deleted: continue
            if args and len(args) > 1 and args[1] != obj.get(args[0], ""): continue
            res = obj
        return res

