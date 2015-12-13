# desk.py
#
#

""" basic commands. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds import __version__, __copyright__, txt

from meds.defines import reason_txt

import threading
import logging
import types
import time
import os

def register(mods):
    mods.register("test", test)
    mods.register("version", version)
    mods.register('copyright', copyright)
    mods.register("ping", ping)
    mods.register("reason", reason)

def ping(event): event.reply("pong")

def copyright(event): event.reply(__copyright__)

def version(event): event.reply("MEDS #%s - %s" % (__version__, txt.strip()))

def test(event): event.reply("hello %s" % event.origin)

def reason(event): event.reply(reason_txt)

