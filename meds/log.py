# log.py
#
#

""" logging infrastructure. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.defines import BOLD, BLA, BLUE, RED, GREEN, YELLOW, ENDC, homedir, logdir, datefmt, format, format_large, LEVELS
from meds.misc import cdir, j

import logging.handlers
import logging
import os

class Formatter(logging.Formatter):

    def format(self, record):
        target = str(record.msg)
        if not target: target = " "
        if target[0] in [">", ]:  target = "%s%s%s%s" % (BLUE, target[0], ENDC, target[1:])
        elif target[0] in ["<", ]: target = "%s%s%s%s" % (GREEN, target[0], ENDC, target[1:])
        elif target[0] in ["!", ]: target = "%s%s%s%s" % (BLUE, target[0], ENDC, target[1:])
        elif target[0] in ["#", ]: target = "%s%s%s%s" % (BLA, target[0], ENDC, target[1:])
        elif target[0] in ["^", ]: target = "%s%s%s%s" % (YELLOW, target[0], ENDC, target[1:])
        elif target[0] in ["-", ]: target = "%s%s%s%s" % (BOLD, target[0], ENDC, target[1:])
        elif target[0] in ["&", ]: target = "%s%s%s%s" % (RED, target[0], ENDC, target[1:])
        record.msg = target
        return logging.Formatter.format(self, record)

class FormatterClean(logging.Formatter):

    def format(self, record):
        target = str(record.msg)
        if not target: target = " "
        if target[0] in [">", "<", "!", "#", "^", "-", "&"]: target = target[2:]
        record.msg = target
        return logging.Formatter.format(self, record)

def log(level, error):
    l = LEVELS.get(str(level).lower(), logging.NOTSET)
    logging.log(l, error)

def loglevel(loglevel, colors=True):
    logger = logging.getLogger("")
    if colors: formatter = Formatter(format, datefmt=datefmt)
    else: formatter = FormatterClean(format, datefmt=datefmt)
    level = LEVELS.get(str(loglevel).lower(), logging.NOTSET)
    filehandler = None
    logger.setLevel(level)
    if logger.handlers:
        for handler in logger.handlers: logger.removeHandler(handler)
    if not os.path.exists(logdir): cdir(logdir)
    try: filehandler = logging.handlers.TimedRotatingFileHandler(j(logdir, "meds.log"), 'midnight')
    except Exception as ex: logging.error(ex)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    if colors: ch.setFormatter(formatter)
    else: ch.setFormatter(formatter)
    logger.addHandler(ch)
    if filehandler:
        ch.setFormatter(formatter)
        filehandler.setLevel(level)
        logger.addHandler(filehandler)
    global enabled
    enabled = True
    return logger
