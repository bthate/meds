# test_base.py
#
#

## IMPORTS

from meds.object import Object
from meds.bots.test import TestBot

import unittest

## Test_Base class

class Test_Base(unittest.TestCase):

    def test_construct(self):
        o = Object()
        self.assertEqual(type(o), Object)

    def test_settingattribute(self):
        o = Object()
        o.bla = "mekker"
        self.assertEqual(o.bla, "mekker")

    def test_checkattribute(self):
        o = Object()
        self.failUnlessRaises(AttributeError)

    def test_undersopzet(self):
        o = Object()
        o._bla = "mekker"
        self.assertEqual(o._bla, "mekker")

    def test_update(self):
        o1 = Object()
        o1._bla = "mekker"
        o2 = Object()
        o2._bla = "blaet"
        o1.update(o2)
        self.assertEqual(o1._bla, "blaet")

    def test_iter(self):
        o1 = Object()
        o1.bla1 = 1
        o1.bla2 = 2
        o1.bla3 = 3
        res = sorted(list(o1))
        self.assertEqual(res, ["bla1","bla2","bla3"])
