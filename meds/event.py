# event.py
#
#

""" event passed on to commands. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.object import Object
from meds.errors import ENOTSET
from meds.misc import days

import time

class Event(Object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = self.__class__.__name__
        self.cmnd = ""
        self.rest = ""
        self.args = []
        self.default = False
        self.want = Object()
        self.notwant = Object()
        self.switch = Object() 

    def __getattr__(self, name):
        try: return super().__getattr__(name)
        except AttributeError: pass
        try: return self[name]
        except: return ""

    def announce(self, txt):
        from meds.bots import fleet
        for bot in fleet: bot.announce(txt)

    def reply(self, txt):
        if "channel" in self: self.say(self.channel, txt)
        elif "origin" in self: self.say(self.origin, txt)
        else: self.say("", txt)

    def say(self, channel, txt):
        if "outer" in self: self.outer.write(str(txt) + "\n") ; self.outer.flush() ; return
        if "_bot" not in self: raise ENOTSET("_bot")
        self._bot.say(channel, txt)

    def ok(self, txt=""): self.reply("ok %s" % txt)

    def show(self, obj, sep="\n"):
        self.reply("".join(["%s=%s%s" % (a, obj[a], sep) for a in sorted(obj.keys())]))

    def display(self, obj, keys, txt=""):
        for key in keys:
            try: 
                val = str(getattr(obj, str(key), ""))
                if val: txt += " " + val
            except: pass
        txt = txt.rstrip() 
        txt += " - %s" % days(obj)
        self.reply(txt.strip())

    def parse(self, txt=""):
        if self.args: return
        txt = self.txt or txt
        splitted = txt.split()
        c = 0
        for word in splitted:
            if not c:
                if word[0] == "!": word = word[1:] ; self.cmnd = word
                else: self.cmnd = word
                c += 1
                continue
            if word.startswith("+"):
                try: self.karma = int(word)
                except ValueError: self.karma = 0
            if "http" in word: self.args.append(word) ; self.rest += " " + word ; continue
            try:
                key, value = word.split("=", 1)
                pre = key[0]
                op = key[-1]
                post = value[-1]
                last = word[-1] 
                if key == "i":  
                    try: self.index = int(value)
                    except: pass
                if post == "-": value = value[:-1]
                if key.startswith("!"): key = key[1:] ; self.switch[key] = value ; continue
                if op == "-": key = key[:-1] ; self.notwant[key] = value
                else: self.want[key] = value
                if post == "-" : continue   
                self.args.append(key)
            except (IndexError, ValueError) as ex:
                self.args.append(word)
                self.rest += " " + word
        self.rest = self.rest.strip()  
        return self
