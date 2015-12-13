# cfg.py
#
#

""" default config."""

__copyright__ = "Copyright 2015, Bart Thate"

from meds.object import Object

import socket
import os

class Config(Object): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = self.__class__.__name__

#:
xmpp = Config()
xmpp.prefix = "cfg"
xmpp.user = "meds@localhost"
xmpp.server = "localhost"
xmpp.username = "meds"
xmpp.channel = "#meds"
xmpp.nick = "meds"
xmpp.cfg = "xmpp"
xmpp.port = 5222
xmpp.owner = ""

#:
irc = Config()
irc.type = "irc"
irc.prefix = "cfg"
irc.server = "localhost"
irc.username = "meds"
irc.channel = "#meds"
irc.nick = "meds"
irc.cfg = "irc"
irc.owner = ""

main = Config()
main.path = False
main.prefix = "cfg"
main.colors = False
main.debug = False
main.background = False
main.openfire = True
main.shell = False
main.init = ""
main.workdir = os.path.expanduser("~/.meds")
main.loglevel = "error"
main.packages = ["meds.mods", "meds.bots"]
main.default = ["meds.mods.clock", "meds.mods.system"]
main.modules = ""
main.exclude = ["meds.bots.test", ]
main.cfg = "main"
main.args = []

#:
udp = Config()
udp.prefix = "cfg"
udp.cfg = "udp"
udp.host = "localhost"
udp.port = 5500
udp.password = "boh"
udp.seed = "blablablablablaz" # needs to be 16 chars wide

#:
rest = Config()
rest.prefix = "cfg"
rest.cfg = "rest"
rest.hostname = socket.getfqdn()
rest.port = 10102

#:
rss = Config()
rss.cfg = "rss"
rss.keys_list = ["published", "title", "summary", "link"]
rss.display_list = ["published", "title", "link"]
rss.sleeptime = 600
rss.ignore = []
rss.nosave = []

#:
cli = Config()
cli.welcome = "mogge!!"
cli.cfg = "cli"

#:
cfg = Config()
cfg.main = main
cfg.xmpp = xmpp
cfg.rest = rest
cfg.irc = irc
cfg.udp = udp
cfg.rss = rss
cfg.cli = cli
