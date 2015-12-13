# store.py
#
#

""" read files from disk. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.misc import path, timed, fn_time, short_date
from meds.object import Object
from meds.store import Store
from meds.cfg import cfg

import logging
import mailbox
import glob
import os

def register(mods):
    mods.register("deleted", deleted)
    mods.register("dump", dump)
    mods.register("find", find)
    mods.register("first", first)
    mods.register("last", last)
    mods.register("mbox", mbox)
    mods.register("rm", rm)
    mods.register("restore", restore)

def first(event):
    store = Store()
    res = store.first(*event.args)
    if res: event.display(res, list(event.args))

def last(event):
    store = Store()
    res = store.last(*event.args)
    if res: event.display(res, list(event.args))

def find(event):
    if not event.args: return
    nr = 1
    store = Store()
    for obj in store.selected(event): event.display(obj, event.args, str(nr)) ; nr += 1
      
def dump(event):
    if not event.args: return
    store = Store()
    objs = store.selected(event)
    for obj in objs: event.reply(obj.json())

def rm(event):
    try: key, match = event.rest.split(" ", 1)
    except ValueError: return
    nr = 0
    store = Store()
    for fn in store.all(key):
        obj = Object().load(fn)
        if key not in obj: continue
        if match not in obj[key]: continue
        obj.deleted = True
        obj.sync()
        nr += 1
    event.ok(nr)

def restore(event):
    try: key, match = event.args
    except ValueError: return
    nr = 0
    store = Store()
    for fn in store.all(*event.args):
        obj = Object().load(fn)
        if key not in obj: continue
        if match not in obj[key]: continue
        if "deleted" not in obj: continue
        obj.deleted = False
        obj.sync()
        nr += 1
    p.ok(nr)

def deleted(event):
    if not event.args: return
    store = Store()
    key = event.args[0]
    nr = 0
    for fn in store.all(key):
       obj = Object().load(fn) 
       if "deleted" not in obj: continue
       res = obj.get(key, "")
       if res: event.reply(res)
       nr += 1

def mbox(event):
    if not event.args: return
    fn = os.path.expanduser(event.args[0])
    nr = 0
    try: object = mailbox.Maildir(fn, create=False)
    except: 
        try: object = mailbox.mbox(fn, create=False)
        except: event.reply("need a mbox or maildir.") ; return
    for m in object:
        o = Object()
        o.update(m.items())
        try: sdate = os.sep.join(short_date(o.Date).split())
        except AttributeError: sdate = None
        o.text = bytes()
        for load in m.walk():
            if load.get_content_type() == 'text/plain': o.text += load.get_payload(decode=True)
        o.text = str(o.text, "latin-1")
        o.prefix = "email"
        if sdate: o.save(sdate)
        else: o.save()
        nr += 1
    event.ok(nr)
    return nr

