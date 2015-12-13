# entry.py
#
#

""" entry commands. """

from meds.object import Object

def register(mods):
    mods.register("log", log)
    mods.register("todo", todo)
    mods.register("status", status)
    mods.register("rss", rss)

def log(event):
    o = Object(event)
    o.prefix = "log" 
    o.log = event.rest
    path = o.save()   
    event.ok(1)

def todo(event):
    o = Object(event)
    o.prefix = "todo"
    o.todo = event.rest
    path = o.save()
    event.ok(1)

def status(event):
    o = Object(event)
    o.prefix = "status"
    o.status = event.rest
    path = o.save()
    event.ok(1)

def rss(event):
    o = Object(event)
    o.prefix = "rss" 
    o.rss = event.rest
    o.service = "rss" 
    path = o.save()   
    event.ok(1)
