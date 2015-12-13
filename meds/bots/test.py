# test.py
#
#

""" test commands and classes. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.scheduler import Scheduler, scheduler, launcher
from meds.object import Object
from meds.errors import EOWNER
from meds.event import Event
from meds.bots import fleet
from meds.mods import cmnds
from meds.misc import name
from meds.cfg import cfg

import unittest
import logging
import queue
import time
import sys
import os

def register(mods):
    mods.register('deadline', deadline)
    mods.register('exception', exception)
    mods.register("flood", flood)
    mods.register('forced', forced)
    mods.register('html', html)
    mods.register("runcmnds", runcmnds)
    mods.register('unicode', unicode)
    mods.register('wrongxml', wrongxml)
    mods.register("workdir", workdir)

class Test(unittest.TestCase): pass

class TestBot(Scheduler):

    testing = True
    cc = "!"
    default = ""
    channels = ["#test", ]
    _queue = queue.Queue()

    def announce(self, txt): self.out(txt)

    def out(self, txt):
        if "verbose" in cfg.main and cfg.main.verbose: print(txt)

    def say(self, channel, txt): self.out(txt)

    def event(self, txt=""): 
        e = Event(txt=txt)
        e.txt = txt
        e.origin = "test@bot"
        e._bot = self
        e.parse()
        return e
        
def flood(event):
    txt = "b" * 5000
    event.announce(txt)

def forced(event):
    for bot in fleet:
        try: bot._sock.shutdown(2)
        except: event.reply("%s bot doesn't have a _sock attribute" % name(bot))

def exception(event):
    if event.origin != cfg.main.owner: event.reply("EOWNER %s" % event.origin) ; return 
    event.reply("raising exception.")
    raise Exception('test exception')

def wrongxml(event):
    event.reply('sending bork xml')
    for bot in fleet: bot.out('<message asdfadf/>')

def unicode(event): event.reply(outtxt)

def deadline(event):
    try: nrseconds = int(event.rest)
    except: event.reply("need number of seconds to sleep.") ; return
    event.reply('starting %s sec sleep' % nrseconds)
    time.sleep(nrseconds)

def workdir(event): event.workdir = "bla.test" ; event.save() ; event.reply(event._path)

def html(event):
    event.reply('<span style="font-family: fixed; font-size: 10pt"><b>YOOOO BROEDERS</b></span>')

def cmndrun(event):
    for cmnd in sorted(list(cmnds.handlers.keys())):
        if cmnd in exclude: continue
        e = Event()
        e.txt = ("!" + cmnd)
        e._bot = event._bot
        e.workdir = "test.data"
        e.origin = "test@bot"
        e.parse()
        logging.warn("< %s" % e.txt)
        scheduler.dispatch(e)

def runcmnds(event):
    if cfg.main.owner not in event.origin: event.reply("EOWNER %s" % event.origin) ; return
    bot = TestBot()
    bot.workdir = "test.data"
    try: nrloops = int(event.args[0])
    except: nrloops = 1
    for x in range(nrloops): launcher.launch(cmndrun, event)

exclude = ["fetcher", "test", "runcmnds"]
outtxt = u"Đíť ìš éèñ ëņċøďıńğŧęŝţ· .. にほんごがはなせません .. ₀0⁰₁1¹₂2²₃3³₄4⁴₅5⁵₆6⁶₇7⁷₈8⁸₉9⁹ .. ▁▂▃▄▅▆▇▉▇▆▅▄▃▂▁ .. .. uǝʌoqǝʇsɹǝpuo pɐdı ǝɾ ʇpnoɥ ǝɾ"
