# errors.py
#
#

""" possible exceptions. """

__copyright__ = "Copyright 2015, Bart Thate"

## FOUTJES

class Error(BaseException): pass

class ENOMETHOD(Error): pass

class EDISPATCHER(Error): pass

class EATTRIBUTE(Error): pass

class ENOTSET(Error): pass

class ESIGNATURE(Error): pass

class EIMPLEMENTED(Error): pass

class EJSON(Error): pass

class EDISCONNECT(Error): pass

class ECONNECT(Error): pass

class EFILE(Error): pass

class EARGUMENT(Error): pass

class ETYPE(Error): pass

class EOWNER(Error): pass

class EFUNC(Error): pass

class EREGISTER(Error): pass

