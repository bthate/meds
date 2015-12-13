# opts.py
#
#

""" command line options. """

__copyright__ = "Copyright 2015, Bart Thate"

from meds.defines import homedir
from meds import __version__

import optparse
import logging
import time
import os

opts_defs = [
              ('', '--debug', 'store_true', False, 'debug',  "enable debug mode."),
              ('', '--path', 'store_true', False, 'path',  "show syspath"),
              ('-b', '--background', 'store_true', False, 'background',  "switch to background mode."),
              ('-c', '--colors', 'store_true', False, 'colors',  "turn on color mode"),
              ('-d', '--workdir', 'string',  "", 'workdir',  "working directory."),
              ('-e', '--onerror', 'store_true', False, 'onerror',  "raise on error"),
              ('-i', '--init', 'string', "", 'init',  "whether to initialize plugins."),
              ('-l', '--loglevel', 'string', "error", 'loglevel',  "loglevel."),
              ('-m', '--modules', 'string', "", 'modules',  "list of modules to use."),
              ('-n', '--nowait', 'store_false', True, 'nowait', 'use blocking mode'),
              ('-o', '--owner', 'string', "", 'owner',  "userhost/JID of the bot owner"),
              ('', '--openfire', 'store_true', False, 'openfire', 'use openfire to connect to XMPP.'),
              ('-p', '--port', 'string', "10102", 'port',  "port to run HTTP server on."),
              ('-s', '--shell', 'store_true', False, 'shell',  "enable shell mode."),
              ('-v', '--verbose', 'store_true', False, 'verbose', 'use verbose mode.'),
              ('', '--skip', "string", "", "skip", "list of items to skip.")
          ]

opts_defs_sed = [
              ('-d', '--dir', 'string', "", 'dir_sed',  "directory to work with."),
              ('-l', '--loglevel', 'string', "error", 'loglevel',  "loglevel"),
          ]  

opts_defs_udp = [
              ('-p', '--port', 'string', "10102", 'port',  "port to run API server on"),
              ('-l', '--loglevel', 'string', "error", 'loglevel',  "loglevel"),
          ]

opts_defs_doctest = [
              ('-e', '--onerror', 'store_true', False, 'onerror',  "raise on error"),
              ('-v', '--verbose', 'store_true', False, 'verbose',  "use verbose"),
              ('-l', '--loglevel', 'string', "error", 'loglevel',  "loglevel"),
          ]

def make_opts(options):
    parser = optparse.OptionParser(usage='usage: %prog [options]', version=str(__version__))
    for option in options:
        type, default, dest, help = option[2:]
        if "store" in type:
            try: parser.add_option(option[0], option[1], action=type, default=default, dest=dest, help=help)
            except Exception as ex: logging.error("^ Opts/error %s option %s" % (str(ex), option)) ; continue
        else:
            try: parser.add_option(option[0], option[1], type=type, default=default, dest=dest, help=help)
            except Exception as ex: logging.error("^ Opts/error %s option %s" % (str(ex), option)) ; continue
    args = parser.parse_args()
    return args

