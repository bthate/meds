# meds/rss.py0
#
#

""" rss module. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.misc import slice, get_url, strip_html, need_redirect, get_feed, short_date, matching, locked
from meds.mods.clock import Repeater
from meds.object import Object
from meds.store import Store
from meds.cfg import cfg
from meds.scheduler import launcher
from meds.bots import fleet
import logging
import time

seen = Object()
seen.list = []
seen.results = "rss"
seen.prefix = "results"

objs = Object()

def register(mods): mods.register("fetcher", fetcher)

def stop():
    if "rss" in objs: objs.rss.exit()

def init(mods):
    global seen
    store = Store()
    rss = store.last("results", "rss")
    if rss: seen = rss
    rss = Repeater(600, fetcher, name="rss.fetch")
    launcher.launch(rss.start)

def display(entry):
    result = ""
    for key in cfg.rss.display_list:
        if key not in entry: continue
        if key == "summary": data = strip_html(entry[key])
        else: data = entry[key]
        if entry.get(key, None): result += "%s - " % data
    return result[:-3]

def fetch(obj):
    global seen
    counter = 0
    for o in get_feed(obj.rss):
        if o.link in seen.list: continue
        seen.list.append(o.link)
        s = slice(o, cfg.rss.keys_list)
        s.services = "rss"
        s.prefix = "feeds"
        s.short = short_date(time.ctime())
        if not matching(cfg.rss.nosave, o.link): s.save()
        for bot in fleet: bot.announce(display(s))
        counter += 1
    return counter
    
def fetcher(event):
    result = []
    thrs = []
    store = Store()
    for fn in store.all("rss"):
        obj = Object().load(fn)
        if "deleted" in obj and obj.deleted: continue
        if "rss" not in obj: continue
        if "http" not in obj.rss: continue
        if cfg.rss.ignore and cfg.rss.ignore in obj.rss: continue
        fetch(obj)
    seen.sync()
    return result

