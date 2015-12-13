# test_attributes.py
#
#

## IMPORTS

from meds.object import Object

import unittest
import logging
import time

## TESTS

class Test_Attribute(unittest.TestCase):

    def timed(self):
        with self.assertRaises((AttributeError, )):
            o = Object()
            o.timed2

    def timed2(self):
        o = Object()
        o.date = time.ctime(time.time())
        self.assert_(o.timed())
