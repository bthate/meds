# misc.py
#
#

""" misc. functions. """

from meds.defines import YELLOW, ENDC, allowedchars, headertxt, dirmask, filemask, basic_types
from meds.opts import make_opts, opts_defs
from meds import __version__
from stat import *

import urllib.request, urllib.error, urllib.parse
import html.parser
import itertools
import traceback
import threading
import calendar
import datetime
import logging
import hashlib
import _thread
import base64
import socket
import types
import http
import time
import json
import glob
import sys
import os
import re

def shutdown(name=""):
    logging.warn("# shutdown")
    for thr in threading.enumerate():
        if str(thr).startswith("<_"): continue
        if name and name not in str(thr): continue
        if "stop" in dir(thr): thr.stop()
        elif "exit" in dir(thr): thr.exit()
        elif "cancel" in dir(thr): thr.cancel()
        else: thr.join(0.1)

def get_exception(*args, **kwargs):
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = ""
    for i in trace:
        fname = i[0]
        linenr = i[1]
        func = i[2]
        plugfile = fname[:-3].split(os.sep)
        mod = []
        for i in plugfile[::-1]:
            mod.append(i)  
            if i == "meds": break
        ownname = '.'.join(mod[::-1])
        result += "%s:%s %s | " % (ownname, linenr, func)
    del trace
    return "%s%s: %s" % (result, exctype, excvalue)

def signature(obj): return str(hashlib.sha1(bytes(str(obj), "utf-8")).hexdigest())

def dumps(obj, *args, **kwargs): return json.dumps(obj, default=smooth, *args, **kwargs)

def urled(obj):
    from meds.cfg import cfg
    if "_path" in obj: fn = os.sep.join(obj._path.split(os.sep)[-2:])
    else: fn = ""
    return "http://%s:%s/%s" % (cfg.rest.hostname, cfg.main.port, fn)

def parse_cli(name="MEDS"):
    from meds.cfg import cfg
    from meds.log import loglevel
    opts, args = make_opts(opts_defs)
    cfg.main.args = args
    cfg.main.update(vars(opts))
    if not cfg.main.workdir: cfg.main.workdir = os.path.expanduser("~/.meds")
    if cfg.main.shell: hello(name, **cfg.main)
    loglevel(cfg.main.loglevel, colors=cfg.main.colors)
    
def root(obj):
    from meds.cfg import cfg
    path = cfg.main.workdir
    path = os.path.abspath(path)
    check_permissions(path)
    return path

def path(obj):
    if "workdir" in obj: p = obj.workdir
    else: p = root(obj)
    if "prefix" in obj: p = j(p, obj.prefix)
    return os.path.abspath(p) 

def selector(obj, keys):
    for key in keys:
        if key == "time": continue
        if key in obj: return True
        if not getattr(obj, key, None): return False
    return True

def wanted(obj, want):
    go = True
    for key, value in want.items():
        if key == "format": continue
        if key not in obj: continue
        if value.startswith("-"): continue
        if value not in str(obj[key]): go = False ; break 
    return go

def notwanted(obj, notwant):
    for key, value in notwant.items():
        if key == "format": continue
        if key not in obj: continue
        if value in obj[key]: return True
    return False

def days(obj):
    t1 = time.time()
    t2 = timed(obj)
    if t2:
        time_diff = float(t1 - t2)
        return elapsed(time_diff)

def dated(obj):
    val = ""
    if "Date" in obj: val = obj.Date
    elif "date" in obj: val = obj.date
    elif "published" in obj: val = obj.published
    elif "added" in obj: val = obj.added
    elif "saved" in obj: val = obj.saved
    elif "timed" in obj: val = obj.timed
    return val

def timed(obj):
    t = short_date(dated(obj))
    if t: t = to_time(t)
    if not t and "_path" in obj: t = fn_time(obj._path)
    if not t: t = fn_time(rtime())
    return t

def search(obj, name):
    l = []
    for key in obj.keys():
        if name in key: l.append(key)
    return l

def match(obj, txt):
    for key in obj.keys():
        if txt not in key: continue
        return obj[key]

def slice(obj, keys=[]):
    if not obj: return
    from meds.object import Object
    o = Object()
    if not keys: keys = obj.keys()
    for key in keys:
        if key.startswith("_"): continue
        try: val = obj[key]
        except KeyError: continue
        try: val.keys() ; o[key] = slice(val)
        except: o[key] = val
    return o

def list_files(*args, **kwargs):
    path = args[0]
    if len(args) > 1: prefix = args[1]
    else: prefix = ""
    res = []
    nr = 0
    if "nr" in kwargs: nr += kwargs["nr"]
    if not path.endswith(os.sep): path += os.sep
    if prefix and os.path.isdir(path + prefix): path += prefix
    if "*" not in path: path += "*"
    for fnn in glob.glob(path):
        if os.path.isdir(fnn):
            kwargs["nr"] = nr
            res.extend(list_files(fnn, **kwargs)) ; continue
        if "time" in kwargs and kwargs["time"] not in fnn: continue
        if fnn: res.append(fnn)
        nr += 1
    return res 

def touch(fname):
    try: fd = os.open(fname, os.O_RDONLY | os.O_CREAT) ; os.close(fd)
    except Exception as ex: logging.error(get_exception())

def check_permissions(ddir, dirmask=dirmask, filemask=filemask):
    uid = os.getuid()
    gid = os.getgid()
    try: stat = os.stat(ddir)
    except OSError: cdir(ddir) ; stat = os.stat(ddir)
    if stat.st_uid != uid: os.chown(ddir, uid, gid)
    if os.path.isfile(ddir): mask = filemask
    else: mask = dirmask
    m = oct(S_IMODE(stat.st_mode))
    if m != oct(mask): os.chmod(ddir, mask)

def cdir(path):
    res = "" 
    for p in path.split(os.sep):
       res += "%s%s" % (p, os.sep)
       padje = os.path.abspath(os.path.normpath(res))
       if os.path.isdir(padje): continue
       try: os.mkdir(padje)
       except FileExistsError: pass
       except OSError as ex: logging.error(get_exception())
    return True

def high(target, file_name):
    highest = 0
    for i in os.listdir(target):
        if file_name in i:
            try: seqnr = i.split('.')[-1]
            except IndexError: continue  
            try:
                if int(seqnr) > highest: highest = int(seqnr)
            except ValueError: pass
    return highest

def highest(target, filename):
    nr = high(target, filename)
    return "%s.%s" % (filename, nr+1)

def j(*args):
     if not args: return
     todo = list(map(str, filter(None, args)))
     return os.path.join(*todo)

def mj(*args):
     if not args: return
     todo = list(map(str, filter(None, args)))
     return os.path.join(*todo).replace(os.sep, ".")

def dj(*args):
     if not args: return
     todo = list(map(str, filter(None, args)))
     return os.path.join(*todo).replace(os.sep, "_")

def aj(sep=None, *args): return os.path.abspath(*j(sep, *args))

def locked(func, *args, **kwargs):

    lock = _thread.allocate_lock()

    def lockedfunc(*args, **kwargs):
        lock.acquire()
        res = None
        try: res = func(*args, **kwargs)
        finally:
            try: lock.release()
            except: pass
        return res
    return lockedfunc

def objname(obj): return " ".join(repr(obj).split()[0:2])[1:]

def name(obj):
     res = " ".join(repr(obj).split()[2:3])
     if "." not in res: res = " ".join(repr(obj).split()[1:2])
     return res

def matching(keys, value):
    for key in keys:
        if key in value: return True
    return False

def get_source(mod, package):
    import pkg_resources as p
    source = os.path.abspath(p.resource_filename(mod, package))
    return source

def stripbadchar(s): return "".join([c for c in s if ord(c) > 31 or c in allowedchars])

def enc_char(s):
    result = []
    for c in s:
        if c in allowedchars: result.append(c)
        else: result.append(enc_name(c))
    return "".join(result)

def enc_needed(s): return [c for c in s if c not in allowedchars]

def enc_name(input): return str(base64.urlsafe_b64encode(bytes(input, "utf-8")), "utf-8")

def split_txt(what, l=375):
    txtlist = []
    start = 0
    end = l
    length = len(what)
    for i in range(int(length/end+1)):
        endword = what.find(' ', end)
        if endword == -1: endword = length
        res = what[start:endword]
        if res: txtlist.append(res)
        start = endword
        end = start + l
    return txtlist

def copyright(): return "Copyright 2015, Bart Thate"

def hello(descr, **kwargs):
    from meds import __version__
    version = kwargs.get("version", __version__)
    txt = kwargs.get("txt", "")
    colors = kwargs.get("colors", "")
    if colors: print("%s%s #%s %s%s\n" % (YELLOW, descr, version, txt, ENDC))
    else: print("%s #%s %s\n" % (descr, version, txt))

def list_eggs(filter="meds"):
    for f in sys.path:
        if ".egg" not in f: continue
        if filter and filter not in f: continue
        yield f
 
def show_eggs(filter="meds"):
    path = list(list_eggs(filter))[0]

def stripped(input):
    try: return input.split("/")[0]
    except: return input

def feed(text):
    from meds.object import Object
    result = []
    chunks = text.split("\r\n")
    for chunk in chunks:
        obj = Object().feed(chunk)
        result.append(obj)
    return result

def run_sed(filename, sedstring):
    f = open(filename, 'r')
    tmp = filename + '.tmp'
    fout = open(tmp, 'w')
    if sedstring:
        char = "#"
        seds = sedstring.split(char)
        fr = seds[1]
        to = seds[2]
        for line in f:
            l = re.sub(fr, to, line)
            fout.write(l)
    else:
        for line in f:
            l = re.sub("\t", "    ", line.rstrip() + "\n")
            fout.write(l)
    fout.flush()
    fout.close()
    try: os.rename(tmp, filename)
    except WindowsError: os.remove(filename) ; os.rename(tmp, filename)

def resolve_ip(hostname=None, timeout=1.0):
    oldtimeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try: ip = socket.gethostbyname(hostname or socket.gethostname())
    except socket.timeout: ip = None
    socket.setdefaulttimeout(oldtimeout)
    return ip

def resolve_host(ip=None, timeout=1.0):
    oldtimeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try: host = socket.gethostbyaddr(ip or resolve_ip())[0]
    except socket.timeout: host = None
    socket.setdefaulttimeout(oldtimeout)
    return host

def pretty(a):
    if type(a) not in basic_types: return objname(a)
    else: return bytes("%s\n" % a, "utf-8")

def smooth(a):
    if type(a) not in basic_types: return objname(a)
    else: return a

def full(a):
    if type(a) not in basic_types: return str(a)
    else: return a

def verzin(a):
    if type(a) is float and not a.is_integer(): return short_date(time.ctime(a))
    if type(a) not in basic_types: return str(type(a))
    else: return a

def unique(a): return list(set(a))

def intersect(a, b): return list(set(a) & set(b))

def union(a, b): return list(set(a) | set(b))

def make_signature(data):
    return str(hashlib.sha1(bytes(str(data), "utf-8")).hexdigest())

def verify_signature(data, signature):
    fromdisk = json.loads(data)
    signature2 = make_signature(fromdisk["data"])
    return signature2 == signature


timere = re.compile('(\S+)\s+(\S+)\s+(\d+)\s+(\d+):(\d+):(\d+)\s+(\d+)')
bdmonths = ['Bo', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthint = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12 
           }

## TIME

def fn_time(daystr):
    try:
        daystr = daystr.replace("_", ":")
        datestr = " ".join(daystr.split(os.sep)[-2:])
        datestr = datestr.split(".")[0]
        t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
        return t
    except: return 0

def rtime(): return str(datetime.datetime.now()).replace(" ", os.sep).replace(":", "_")
def hms(): return str(datetime.datetime.today()).split()[1].split(".")[0]
def day(): return str(datetime.datetime.today()).split()[0]
def to_day(daystr): return time.mktime(time.strptime(daystr, "%Y-%m-%d"))

def to_time(daystr):
    daystr = daystr.replace("_", ":")
    return time.mktime(time.strptime(daystr, "%Y-%m-%d %H:%M:%S"))

def short_date(*args, **kwargs):
    # Mon, 25 Oct 2010 18:05:33 -0700 (PDT)
    # ['13', 'Oct', '2012', '20:43:46', '+0300']
    date = args[0]
    if not date: return None
    date = date.replace("_", ":")
    res = date.split()
    ddd = ""
    try:
        if "+" in res[3]: raise ValueError
        if "-" in res[3]: raise ValueError
        int(res[3])
        ddd = "{:4}-{:#02}-{:#02} {:6}".format(res[3], monthint[res[2]], int(res[1]), res[4])
    except (IndexError, KeyError, ValueError):
        try:
            if "+" in res[4]: raise ValueError
            if "-" in res[4]: raise ValueError
            int(res[4])
            ddd = "{:4}-{:#02}-{:02} {:6}".format(res[4], monthint[res[1]], int(res[2]), res[3])
        except (IndexError, KeyError, ValueError):
            try: ddd = "{:4}-{:#02}-{:02} {:6}".format(res[2], monthint[res[1]], int(res[0]), res[3])
            except (IndexError, KeyError):
                try: ddd = "{:4}-{:#02}-{:02}".format(res[2], monthint[res[1]], int(res[0]))
                except (IndexError, KeyError): ddd = ""
    return ddd.replace(":", "_")

def elapsed(seconds,short=True):
    txt = ""
    nsec = int(float(seconds))
    year = 365*24*60*60
    week = 7*24*60*60
    day = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    days = int(nsec/day)
    nsec -= days*day
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    sec = nsec - minutes*minute
    if years: txt += "%sy" % years
    if weeks: days += weeks * 7
    if days: txt += "%sd" % days
    txt += " "
    if hours: txt += "%sh" % hours 
    if minutes: txt += "%sm" % minutes
    if sec and not hours: txt += "%ss" % sec
    if txt: return txt.strip()
    else: return "0s"

def get_day(daystr):
    try:
        dmyre = re.search('(\d+)-(\d+)-(\d+)', daystr)
        (day, month, year) = dmyre.groups()
        day = int(day)
        month = int(month)
        year = int(year)
        if day <= calendar.monthrange(year, month)[1]:
            date = "%s %s %s" % (day, bdmonths[month], year)
            return time.mktime(time.strptime(date, "%d %b %Y"))
    except AttributeError: return 0
    except ValueError: return 0

def get_hour(daystr):
    try:
        hmsre = re.search('(\d+):(\d+):(\d+)', daystr)
        hours = 60 * 60 * (int(hmsre.group(1)))
        hoursmin = hours  + int(hmsre.group(2)) * 60
        hms = hoursmin + int(hmsre.group(3))
    except AttributeError: pass
    except ValueError: pass
    try:
        hmre = re.search('(\d+):(\d+)', daystr)
        hours = 60 * 60 * (int(hmre.group(1)))
        hms = hours + int(hmre.group(2)) * 60
    except AttributeError: return 0
    except ValueError: return 0
    return hms

def today():
    today = day()
    ttime = time.strptime(today, "%Y-%m-%d")
    result = time.mktime(ttime)
    return result

def get_frame(search="code"):
    result = {}
    frame = sys._getframe(1)
    search = str(search)
    for i in dir(frame):
        if search in i:
            target = getattr(frame, i)
            for j in dir(target):
                result[j] = getattr(target, j)
    return result

def get_strace(*args, **kwargs):
    result = ""
    try: depth = args[0]
    except IndexError: depth = 1
    loopframe = sys._getframe(depth)
    if not loopframe: return result
    while 1:
        try: frame = loopframe.f_back
        except AttributeError: break
        if not frame: break
        linenr = frame.f_lineno
        func = frame.f_code.co_name
        result += "%s:%s | " % (func, linenr)
        loopframe = frame
    del loopframe
    return result[:-3]

def get_feed(url):
    from meds.object import Object
    import feedparser as fp
    result = {}
    try: data = get_url(url)
    except Exception as ex: error("%s %s" % (url, get_exception())) ; return
    result = fp.parse(data)
    if "entries" in result:
        for entry in result["entries"][::-1]: yield Object(entry)

def get_url(*args, **kwargs):
    req = urllib.request.Request(args[0], headers={"User-Agent": useragent()})
    resp = urllib.request.urlopen(req)
    data = resp.read()
    logging.info("- %s %s %s" % (resp.status, resp.reason, args[0]))
    return data

def get_url2(url, myheaders={}, postdata={}, keyfile=None, certfile="", port=80):
    headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'Accept': 'text/plain; text/html; application/json', 'User-Agent': useragent()}
    headers.update(myheaders)
    urlparts = urllib.parse.urlparse(url)
    if "https" in url: connection = http.client.HTTPSConnection(urlparts[1]) # keyfile, certfile)
    else: connection = http.client.HTTPConnection(urlparts[1])
    connection.connect()
    connection.request("GET", urlparts[2], None, headers)
    resp = connection.getresponse()
    data = resp.read()
    logging.info("- %s %s %s" % (resp.status, resp.reason, url))
    connection.close()
    return data

def need_redirect(resp):
    if resp.status == 301 or resp.status == 302: url = resp.getheader("Location") ; return url

def useragent(): return 'Mozilla/5.0 (X11; Linux x86_64) MEDS %s +http://pikacode.com/bart/meds)' % __version__

def unescape(text): return html.parser.HTMLParser().unescape(text)

def extract_div(search, data):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(data) 
    divs = soup('div')
    for div in divs:
       if div.get(search): return div

def get_encoding(data):
    if hasattr(data, 'info') and 'content-type' in data.info and 'charset' in data.info['content-type'].lower():
        charset = data.info['content-type'].lower().split('charset', 1)[1].strip()
        if charset[0] == '=':
            charset = charset[1:].strip()
            if ';' in charset: return charset.split(';')[0].strip()
            return charset
    if '<meta' in data.lower():
        metas = re.findall('<meta[^>]+>', data, re.I | re.M)
        if metas:
            for meta in metas:
                test_http_equiv = re.search('http-equiv\s*=\s*[\'"]([^\'"]+)[\'"]', meta, re.I)
                if test_http_equiv and test_http_equiv.group(1).lower() == 'content-type':
                    test_content = re.search('content\s*=\s*[\'"]([^\'"]+)[\'"]', meta, re.I)
                    if test_content:
                        test_charset = re.search('charset\s*=\s*([^\s\'"]+)', meta, re.I)
                        if test_charset: return test_charset.group(1)
    try:
        test = chardet.detect(data)
        if 'encoding' in test: return test['encoding']
    except: pass
    return sys.getdefaultencoding()

def parse_url(*args, **kwargs):
    """

    Attribute       Index   Value                   Value if not present
    scheme          0       URL scheme specifier    empty string
    netloc          1       Network location part   empty string
    path            2       Hierarchical path       empty string
    query           3       Query component         empty string
    fragment        4       Fragment identifier     empty string

    """
    url = args[0]
    parsed = urllib.parse.urlsplit(url)
    target = parsed[2].split("/")
    if "." in target[-1]: basepath = "/".join(target[:-1]) ; file = target[-1]
    else: basepath = parsed[2] ; file = None
    if basepath.endswith("/"): basepath = basepath[:-1]
    base = urllib.parse.urlunsplit((parsed[0], parsed[1], basepath , "", ""))
    root = urllib.parse.urlunsplit((parsed[0], parsed[1], "", "", ""))
    return (basepath, base, root, file)

def strip_html(text):
    import bs4
    soup = bs4.BeautifulSoup(text)
    return soup.get_text()
