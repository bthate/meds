# meds/plugins/system.py
#
#

""" system services. """

from meds.mods.clock import Repeater
from meds.scheduler import launcher
from meds.mods import cmnds

import types

def register(mods):
    mods.register("syncer", syncerd) 
    mods.register("reload", reload)

def init(*args, **kwargs):
    todo = Repeater(60, syncerd, name="syncerd")
    launcher.launch(todo.start)

def syncerd(*args, **kwargs):
    for name, plug in cmnds.handlers.items():
        if type(plug) not in [types.ModuleType]: continue
        syncer = getattr(plug, "sync", None)
        if syncer: syncer()

def reload(event): cmnds.reload(event.rest)
