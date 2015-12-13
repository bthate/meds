# info.py
#
#

""" runtime information. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.misc import search, dumps, slice, elapsed, name
from meds.errors import EOWNER
from meds.object import Object
from meds.store import Store
from meds.cfg import cfg as maincfg
from meds.scheduler import launcher

import threading
import logging
import types
import time
import os

def register(mods):
    mods.register("ps", ps)
    mods.register("cfg", cfg)
    mods.register("pid", pid)
    mods.register("cmnds", cmnds)
    mods.register("uptime", uptime)

def uptime(event): event.reply("uptime is %s" % elapsed(time.time() - event._bot._start))

def pid(event): event.reply(os.getpid())

def cmnds(event):
    from meds.mods import cmnds
    if not event.rest:
       result = set([x.split(".")[-1] for x in cmnds.handlers.keys()])
       event.reply(", ".join(sorted(result)))
       return
    name = ""
    keys = search(cmnds.handlers, event.rest)
    if keys: event.reply(", ".join(keys))

def cfg(event):
    store = Store()
    if event._bot.type != "CLI":
        bcfg = store.last("cfg", event._bot.type.lower())
        if not bcfg or "owner" not in bcfg or event.userhost != bcfg.owner: event.reply("EOWNER %s" % event.userhost) ; return
    obj = maincfg
    if event.args:
        ctype = event.args[0]
        obj = store.last("cfg", ctype)
        if not obj: obj = maincfg.get(ctype, None)
    try: 
        key = event.args[1]
        value = event.args[2]
        if key in obj:
            if type(obj[key]) in [list, tuple]: obj[key].append(value)
            else: obj[key] = value
            obj.prefix = "cfg"
            obj.sync()
    except IndexError: pass
    if obj: event.show(obj)

def ps(event):
    results = []
    nr = 1
    for thr in sorted(launcher.running(), key=lambda x: str(x)):
        obj = Object() 
        obj.update(vars(thr))
        txt = thr.name.strip()
        if event.rest and event.rest not in txt: continue
        try: obj = obj.__class__.__self__
        except: pass
        if "_error" in obj: txt += " %s" % obj._error.strip()
        if "_status" in obj: txt += " %s" % obj._status.strip()
        if "_start" in obj: txt += " %s" % elapsed(int(time.time()) - int(obj._start))
        if "sleep" in obj and "_last" in obj: txt += " next %s/%s" % (elapsed(int(obj.sleep) - int(time.time() - int(obj._last))), elapsed(int(obj.sleep)))
        event.reply("%s %s" % (nr, txt.strip()))
        nr += 1
