# test_cmnds.py
#
#

""" test for all command. """

from meds.scheduler import launcher
from meds.bots.test import TestBot
from meds.log import loglevel
from meds.event import Event
from meds.cfg import cfg
from meds.mods import cmnds

import unittest
import logging

loglevel(cfg.main.loglevel or "error")

cfg.main.workdir = "test.data"
bot = TestBot()
cmnds.init()
events = []

class Test_Cmnd(unittest.TestCase):

    def test_cmnds(self):
        for cmnd in sorted(cmnds.handlers.keys()):
            if cmnd in ["test", "fetcher"]: continue
            event = Event()
            event.txt = cmnd + " arg1" 
            event._bot = bot
            event.origin = "tester@bot"
            event.parse()
            logging.warn("< %s" % event.txt)
            func = cmnds.get(event.cmnd)
            if func: launcher.launch(func, event)
            events.append(event)
        for event in events: event.wait(3.0) 
