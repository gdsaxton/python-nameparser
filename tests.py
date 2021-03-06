#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run this file to run the tests, e.g "python tests.py" or "./tests.py".
Post a ticket and/or clone and fix it. Pull requests with tests gladly accepted.
http://code.google.com/p/python-nameparser/issues/entry
http://code.google.com/p/python-nameparser/source/createClone
"""

import logging

from nameparser import HumanName, u


log = logging.getLogger('HumanName')

import unittest


class HumanNameTestBase(unittest.TestCase):
    def m(self, actual, expected, hn):
        """assertEquals with a better message"""
        try:
            self.assertEqual(actual, expected, u"'%s' != '%s' for '%s'\n%s" % (
                actual,
                expected,
                hn.full_name,
                hn
            ))
        except UnicodeDecodeError:
            self.assertEquals(actual, expected)


class HumanNameBruteForceTests(HumanNameTestBase):
    def test_utf8(self):
        hn = HumanName("de la Véña, Jüan")
        self.m(hn.first, u"Jüan", hn)
        self.m(hn.last, u"de la Véña", hn)

    def test_u(self):
        hn = HumanName(u"de la Véña, Jüan")
        self.m(hn.first, u"Jüan", hn)
        self.m(hn.last, u"de la Véña", hn)

    def test_escaped_u(self):
        hn = HumanName(u'B\xe4ck, Gerald')
        self.m(hn.first, u"Gerald", hn)
        self.m(hn.last, u"B\xe4ck", hn)

    def test_len(self):
        hn = HumanName("Doe-Ray, Dr. John P., CLU, CFP, LUTC")
        self.m(len(hn), 5, hn)
        hn = HumanName("John Doe")
        self.m(len(hn), 2, hn)

    def test_comparison(self):
        hn1 = HumanName("Doe-Ray, Dr. John P., CLU, CFP, LUTC")
        hn2 = HumanName("Dr. John P. Doe-Ray, CLU, CFP, LUTC")
        self.assertTrue(hn1 == hn2)
        self.assertTrue(not hn1 is hn2)
        self.assertTrue(hn1 == "Dr. John P. Doe-Ray CLU, CFP, LUTC")
        hn1 = HumanName("Doe, Dr. John P., CLU, CFP, LUTC")
        hn2 = HumanName("Dr. John P. Doe-Ray, CLU, CFP, LUTC")
        self.assertTrue(not hn1 == hn2)
        self.assertTrue(not hn1 == 0)
        self.assertTrue(not hn1 == "test")
        self.assertTrue(not hn1 == ["test"])
        self.assertTrue(not hn1 == {"test": hn2})

    def test_assignment_to_full_name(self):
        hn = HumanName("John A. Kenneth Doe, Jr.")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.suffix, "Jr.", hn)
        hn.full_name = "Juan Velasquez y Garcia III"
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test_assignment_to_attribute(self):
        hn = HumanName("John A. Kenneth Doe, Jr.")
        hn.last = "de la Vega"
        self.m(hn.last, "de la Vega", hn)
        hn.title = "test"
        self.m(hn.title, "test", hn)
        hn.first = "test"
        self.m(hn.first, "test", hn)
        hn.middle = "test"
        self.m(hn.middle, "test", hn)
        hn.suffix = "test"
        self.m(hn.suffix, "test", hn)

    def test_comparison_case_insensitive(self):
        hn1 = HumanName("Doe-Ray, Dr. John P., CLU, CFP, LUTC")
        hn2 = HumanName("dr. john p. doe-Ray, CLU, CFP, LUTC")
        self.assertTrue(hn1 == hn2)
        self.assertTrue(not hn1 is hn2)
        self.assertTrue(hn1 == "Dr. John P. Doe-ray clu, CFP, LUTC")

    def test_slice(self):
        hn = HumanName("Doe-Ray, Dr. John P., CLU, CFP, LUTC")
        self.m(list(hn), [u'Dr.', u'John', u'P.', u'Doe-Ray', u'CLU, CFP, LUTC'], hn)
        self.m(hn[1:], [u'John', u'P.', u'Doe-Ray', u'CLU, CFP, LUTC'], hn)
        self.m(hn[1:-1], [u'John', u'P.', u'Doe-Ray'], hn)

    def test_conjunction_names(self):
        hn = HumanName("johnny y")
        self.m(hn.first, "johnny", hn)
        self.m(hn.last, "y", hn)

    def test_prefix_names(self):
        hn = HumanName("vai la")
        self.m(hn.first, "vai", hn)
        self.m(hn.last, "la", hn)

    def test_blank_name(self):
        hn = HumanName()
        self.m(hn.first, "", hn)
        self.m(hn.last, "", hn)

    def test1(self):
        hn = HumanName("John Doe")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)

    def test2(self):
        hn = HumanName("John Doe, Jr.")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test3(self):
        hn = HumanName("John Doe III")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "III", hn)

    def test4(self):
        hn = HumanName("Doe, John")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)

    def test5(self):
        hn = HumanName("Doe, John, Jr.")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test6(self):
        hn = HumanName("Doe, John III")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "III", hn)

    def test7(self):
        hn = HumanName("John A. Doe")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)

    def test8(self):
        hn = HumanName("John A. Doe, Jr.")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test9(self):
        hn = HumanName("John A. Doe III")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)
        self.m(hn.suffix, "III", hn)

    def test10(self):
        hn = HumanName("Doe, John A.")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)

    def test11(self):
        hn = HumanName("Doe, John A., Jr.")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test12(self):
        hn = HumanName("Doe, John A., III")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)
        self.m(hn.suffix, "III", hn)

    def test13(self):
        hn = HumanName("John A. Kenneth Doe")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A. Kenneth", hn)

    def test14(self):
        hn = HumanName("John A. Kenneth Doe, Jr.")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test15(self):
        hn = HumanName("John A. Kenneth Doe III")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.suffix, "III", hn)

    def test16(self):
        hn = HumanName("Doe, John. A. Kenneth")
        self.m(hn.first, "John.", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A. Kenneth", hn)

    def test17(self):
        hn = HumanName("Doe, John. A. Kenneth, Jr.")
        self.m(hn.first, "John.", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test18(self):
        hn = HumanName("Doe, John. A. Kenneth III")
        self.m(hn.first, "John.", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.suffix, "III", hn)

    def test19(self):
        hn = HumanName("Dr. John Doe")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.title, "Dr.", hn)

    def test20(self):
        hn = HumanName("Dr. John Doe, Jr.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test21(self):
        hn = HumanName("Dr. John Doe III")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "III", hn)

    def test22(self):
        hn = HumanName("Doe, Dr. John")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)

    def test23(self):
        hn = HumanName("Doe, Dr. John, Jr.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test24(self):
        hn = HumanName("Doe, Dr. John III")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "III", hn)

    def test25(self):
        hn = HumanName("Dr. John A. Doe")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)

    def test26(self):
        hn = HumanName("Dr. John A. Doe, Jr.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test27(self):
        hn = HumanName("Dr. John A. Doe III")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)
        self.m(hn.suffix, "III", hn)

    def test28(self):
        hn = HumanName("Doe, Dr. John A.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)

    def test29(self):
        hn = HumanName("Doe, Dr. John A. Jr.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test30(self):
        hn = HumanName("Doe, Dr. John A. III")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "A.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "III", hn)

    def test31(self):
        hn = HumanName("Dr. John A. Kenneth Doe")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)

    def test32(self):
        hn = HumanName("Dr. John A. Kenneth Doe, Jr.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test33(self):
        hn = HumanName("Al Arnold Gore, Jr.")
        self.m(hn.middle, "Arnold", hn)
        self.m(hn.first, "Al", hn)
        self.m(hn.last, "Gore", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test34(self):
        hn = HumanName("Dr. John A. Kenneth Doe III")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "III", hn)

    def test35(self):
        hn = HumanName("Doe, Dr. John A. Kenneth")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)

    def test36(self):
        hn = HumanName("Doe, Dr. John A. Kenneth Jr.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test37(self):
        hn = HumanName("Doe, Dr. John A. Kenneth III")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "III", hn)

    def test38(self):
        hn = HumanName("Juan de la Vega")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)

    def test39(self):
        hn = HumanName("Juan de la Vega, Jr.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test40(self):
        hn = HumanName("Juan de la Vega III")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.suffix, "III", hn)

    def test41(self):
        hn = HumanName("de la Vega, Juan")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)

    def test42(self):
        hn = HumanName("de la Vega, Juan, Jr.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test43(self):
        hn = HumanName("de la Vega, Juan III")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.suffix, "III", hn)

    def test44(self):
        hn = HumanName("Juan Velasquez y Garcia")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)

    def test45(self):
        hn = HumanName("Juan Velasquez y Garcia, Jr.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test46(self):
        hn = HumanName("Juan Velasquez y Garcia III")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test47(self):
        hn = HumanName("Velasquez y Garcia, Juan")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)

    def test48(self):
        hn = HumanName("Velasquez y Garcia, Juan, Jr.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test49(self):
        hn = HumanName("Velasquez y Garcia, Juan III")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test50(self):
        hn = HumanName("Dr. Juan de la Vega")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)

    def test51(self):
        hn = HumanName("Dr. Juan de la Vega, Jr.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test52(self):
        hn = HumanName("Dr. Juan de la Vega III")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.suffix, "III", hn)

    def test53(self):
        hn = HumanName("de la Vega, Dr. Juan")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)

    def test54(self):
        hn = HumanName("de la Vega, Dr. Juan, Jr.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test55(self):
        hn = HumanName("de la Vega, Dr. Juan III")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.suffix, "III", hn)

    def test56(self):
        hn = HumanName("Dr. Juan Velasquez y Garcia")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)

    def test57(self):
        hn = HumanName("Dr. Juan Velasquez y Garcia, Jr.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test58(self):
        hn = HumanName("Dr. Juan Velasquez y Garcia III")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test59(self):
        hn = HumanName("Velasquez y Garcia, Dr. Juan")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)

    def test60(self):
        hn = HumanName("Velasquez y Garcia, Dr. Juan, Jr.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test61(self):
        hn = HumanName("Velasquez y Garcia, Dr. Juan III")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test62(self):
        hn = HumanName("Juan Q. de la Vega")
        self.m(hn.first, "Juan", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.last, "de la Vega", hn)

    def test63(self):
        hn = HumanName("Juan Q. de la Vega, Jr.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test64(self):
        hn = HumanName("Juan Q. de la Vega III")
        self.m(hn.first, "Juan", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.suffix, "III", hn)

    def test65(self):
        hn = HumanName("de la Vega, Juan Q.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.last, "de la Vega", hn)

    def test66(self):
        hn = HumanName("de la Vega, Juan Q., Jr.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test67(self):
        hn = HumanName("de la Vega, Juan Q. III")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.suffix, "III", hn)

    def test68(self):
        hn = HumanName("Juan Q. Velasquez y Garcia")
        self.m(hn.middle, "Q.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)

    def test69(self):
        hn = HumanName("Juan Q. Velasquez y Garcia, Jr.")
        self.m(hn.middle, "Q.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test70(self):
        hn = HumanName("Juan Q. Velasquez y Garcia III")
        self.m(hn.middle, "Q.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test71(self):
        hn = HumanName("Velasquez y Garcia, Juan Q.")
        self.m(hn.middle, "Q.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)

    def test72(self):
        hn = HumanName("Velasquez y Garcia, Juan Q., Jr.")
        self.m(hn.middle, "Q.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test73(self):
        hn = HumanName("Velasquez y Garcia, Juan Q. III")
        self.m(hn.middle, "Q.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test74(self):
        hn = HumanName("Dr. Juan Q. de la Vega")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.last, "de la Vega", hn)

    def test75(self):
        hn = HumanName("Dr. Juan Q. de la Vega, Jr.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test76(self):
        hn = HumanName("Dr. Juan Q. de la Vega III")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.suffix, "III", hn)

    def test77(self):
        hn = HumanName("de la Vega, Dr. Juan Q.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.title, "Dr.", hn)

    def test78(self):
        hn = HumanName("de la Vega, Dr. Juan Q., Jr.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.suffix, "Jr.", hn)
        self.m(hn.title, "Dr.", hn)

    def test79(self):
        hn = HumanName("de la Vega, Dr. Juan Q. III")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, u"de la Vega", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.suffix, "III", hn)
        self.m(hn.title, "Dr.", hn)

    def test80(self):
        hn = HumanName("Dr. Juan Q. Velasquez y Garcia")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)

    def test81(self):
        hn = HumanName("Dr. Juan Q. Velasquez y Garcia, Jr.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test82(self):
        hn = HumanName("Dr. Juan Q. Velasquez y Garcia III")
        self.m(hn.middle, "Q.", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test83(self):
        hn = HumanName("Velasquez y Garcia, Dr. Juan Q.")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "Q.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)

    def test84(self):
        hn = HumanName("Velasquez y Garcia, Dr. Juan Q., Jr.")
        self.m(hn.middle, "Q.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test85(self):
        hn = HumanName("Velasquez y Garcia, Dr. Juan Q. III")
        self.m(hn.middle, "Q.", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test86(self):
        hn = HumanName("Juan Q. Xavier de la Vega")
        self.m(hn.first, "Juan", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.last, "de la Vega", hn)

    def test87(self):
        hn = HumanName("Juan Q. Xavier de la Vega, Jr.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test88(self):
        hn = HumanName("Juan Q. Xavier de la Vega III")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.suffix, "III", hn)

    def test89(self):
        hn = HumanName("de la Vega, Juan Q. Xavier")
        self.m(hn.first, "Juan", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.last, "de la Vega", hn)

    def test90(self):
        hn = HumanName("de la Vega, Juan Q. Xavier, Jr.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test91(self):
        hn = HumanName("de la Vega, Juan Q. Xavier III")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.suffix, "III", hn)

    def test92(self):
        hn = HumanName("Dr. Juan Q. Xavier de la Vega")
        self.m(hn.first, "Juan", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.last, "de la Vega", hn)

    def test93(self):
        hn = HumanName("Dr. Juan Q. Xavier de la Vega, Jr.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test94(self):
        hn = HumanName("Dr. Juan Q. Xavier de la Vega III")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.suffix, "III", hn)

    def test95(self):
        hn = HumanName("de la Vega, Dr. Juan Q. Xavier")
        self.m(hn.first, "Juan", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.last, "de la Vega", hn)

    def test96(self):
        hn = HumanName("de la Vega, Dr. Juan Q. Xavier, Jr.")
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test97(self):
        hn = HumanName("de la Vega, Dr. Juan Q. Xavier III")
        self.m(hn.first, "Juan", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.last, "de la Vega", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.suffix, "III", hn)

    def test98(self):
        hn = HumanName("Juan Q. Xavier Velasquez y Garcia")
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)

    def test99(self):
        hn = HumanName("Juan Q. Xavier Velasquez y Garcia, Jr.")
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test100(self):
        hn = HumanName("Juan Q. Xavier Velasquez y Garcia III")
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test101(self):
        hn = HumanName("Velasquez y Garcia, Juan Q. Xavier")
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)

    def test102(self):
        hn = HumanName("Velasquez y Garcia, Juan Q. Xavier, Jr.")
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test103(self):
        hn = HumanName("Velasquez y Garcia, Juan Q. Xavier III")
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test104(self):
        hn = HumanName("Dr. Juan Q. Xavier Velasquez y Garcia")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)

    def test105(self):
        hn = HumanName("Dr. Juan Q. Xavier Velasquez y Garcia, Jr.")
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test106(self):
        hn = HumanName("Dr. Juan Q. Xavier Velasquez y Garcia III")
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test107(self):
        hn = HumanName("Velasquez y Garcia, Dr. Juan Q. Xavier")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)

    def test108(self):
        hn = HumanName("Velasquez y Garcia, Dr. Juan Q. Xavier, Jr.")
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test109(self):
        hn = HumanName("Velasquez y Garcia, Dr. Juan Q. Xavier III")
        self.m(hn.middle, "Q. Xavier", hn)
        self.m(hn.first, "Juan", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.last, "Velasquez y Garcia", hn)
        self.m(hn.suffix, "III", hn)

    def test110(self):
        hn = HumanName("John Doe, CLU, CFP, LUTC")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "CLU, CFP, LUTC", hn)

    def test111(self):
        hn = HumanName("John P. Doe, CLU, CFP, LUTC")
        self.m(hn.first, "John", hn)
        self.m(hn.middle, "P.", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.suffix, "CLU, CFP, LUTC", hn)

    def test112(self):
        hn = HumanName("Dr. John P. Doe-Ray, CLU, CFP, LUTC")
        self.m(hn.first, "John", hn)
        self.m(hn.middle, "P.", hn)
        self.m(hn.last, "Doe-Ray", hn)
        self.m(hn.title, "Dr.", hn)
        self.m(hn.suffix, "CLU, CFP, LUTC", hn)

    def test113(self):
        hn = HumanName("Doe-Ray, Dr. John P., CLU, CFP, LUTC")
        self.m(hn.title, "Dr.", hn)
        self.m(hn.middle, "P.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe-Ray", hn)
        self.m(hn.suffix, "CLU, CFP, LUTC", hn)

    def test114(self):
        hn = HumanName("Hon Oladapo")
        self.m(hn.first, "Hon", hn)
        self.m(hn.last, "Oladapo", hn)

    def test115(self):
        hn = HumanName("Hon. Barrington P. Doe-Ray, Jr.")
        self.m(hn.title, "Hon.", hn)
        self.m(hn.middle, "P.", hn)
        self.m(hn.first, "Barrington", hn)
        self.m(hn.last, "Doe-Ray", hn)

    def test116(self):
        hn = HumanName("Doe-Ray, Hon. Barrington P. Jr., CFP, LUTC")
        self.m(hn.title, "Hon.", hn)
        self.m(hn.middle, "P.", hn)
        self.m(hn.first, "Barrington", hn)
        self.m(hn.last, "Doe-Ray", hn)
        self.m(hn.suffix, "Jr., CFP, LUTC", hn)

    def test117(self):
        hn = HumanName("Rt. Hon. Paul E. Mary")
        self.m(hn.title, "Rt. Hon.", hn)
        self.m(hn.first, "Paul", hn)
        self.m(hn.middle, "E.", hn)
        self.m(hn.last, "Mary", hn)

    def test118(self):
        hn = HumanName("Maid Marian")
        self.m(hn.title, "Maid", hn)
        self.m(hn.first, "Marian", hn)

    def test119(self):
        hn = HumanName("Lord God Almighty")
        self.m(hn.title, "Lord", hn)
        self.m(hn.first, "God", hn)
        self.m(hn.last, "Almighty", hn)

    def test_last_name_is_also_title(self):
        hn = HumanName("Amy E Maid")
        self.m(hn.first, "Amy", hn)
        self.m(hn.middle, "E", hn)
        self.m(hn.last, "Maid", hn)

    def test_last_name_is_also_title2(self):
        hn = HumanName("Duke Martin Luther King, Jr.")
        self.m(hn.title, "Duke", hn)
        self.m(hn.first, "Martin", hn)
        self.m(hn.middle, "Luther", hn)
        self.m(hn.last, "King", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test_last_name_is_also_title3(self):
        hn = HumanName("John King")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "King", hn)

    def test_title_with_conjunction(self):
        hn = HumanName("Secretary of State Hillary Clinton")
        self.m(hn.title, "Secretary of State", hn)
        self.m(hn.first, "Hillary", hn)
        self.m(hn.last, "Clinton", hn)

    def test_compound_title_with_conjunction(self):
        hn = HumanName("Cardinal Secretary of State Hillary Clinton")
        self.m(hn.title, "Cardinal Secretary of State", hn)
        self.m(hn.first, "Hillary", hn)
        self.m(hn.last, "Clinton", hn)

    def test_title_is_title(self):
        hn = HumanName("Coach")
        self.m(hn.title, "Coach", hn)


class HumanNameConjunctionTestCase(HumanNameTestBase):
    # Last name with conjunction
    def test117(self):
        hn = HumanName('Jose Aznar y Lopez')
        self.m(hn.first, "Jose", hn)
        self.m(hn.last, "Aznar y Lopez", hn)

    # Potential conjunction/prefix treated as initial (because uppercase)
    def test_uppercase_middle_initial_conflict_with_conjunction(self):
        hn = HumanName('John E Smith')
        self.m(hn.first, "John", hn)
        self.m(hn.middle, "E", hn)
        self.m(hn.last, "Smith", hn)

    def test_lowercase_middle_initial_with_period_conflict_with_conjunction(self):
        hn = HumanName('john e. smith')
        self.m(hn.first, "john", hn)
        self.m(hn.middle, "e.", hn)
        self.m(hn.last, "smith", hn)

    # The conjunction "e" can also be an initial
    def test_lowercase_first_initial_conflict_with_conjunction(self):
        hn = HumanName('e j smith')
        self.m(hn.first, "e", hn)
        self.m(hn.middle, "j", hn)
        self.m(hn.last, "smith", hn)

    def test_lowercase_middle_initial_conflict_with_conjunction(self):
        hn = HumanName('John e Smith')
        self.m(hn.first, "John", hn)
        self.m(hn.middle, "e", hn)
        self.m(hn.last, "Smith", hn)

    def test_lowercase_middle_initial_and_suffix_conflict_with_conjunction(self):
        hn = HumanName('John e Smith, III')
        self.m(hn.first, "John", hn)
        self.m(hn.middle, "e", hn)
        self.m(hn.last, "Smith", hn)
        self.m(hn.suffix, "III", hn)

    def test_lowercase_middle_initial_and_nocomma_suffix_conflict_with_conjunction(self):
        hn = HumanName('John e Smith III')
        self.m(hn.first, "John", hn)
        self.m(hn.middle, "e", hn)
        self.m(hn.last, "Smith", hn)
        self.m(hn.suffix, "III", hn)

    def test_lowercase_middle_initial_comma_lastname_and_suffix_conflict_with_conjunction(self):
        hn = HumanName('Smith, John e, III, Jr')
        self.m(hn.first, "John", hn)
        self.m(hn.middle, "e", hn)
        self.m(hn.last, "Smith", hn)
        self.m(hn.suffix, "III, Jr", hn)

    def test_two_initials_conflict_with_conjunction(self):
        hn = HumanName('E.T. Smith')
        self.m(hn.first, "E.", hn)
        self.m(hn.middle, "T.", hn)
        self.m(hn.last, "Smith", hn)

    def test_couples_names(self):
        hn = HumanName('John and Jane Smith')
        self.m(hn.first, "John and Jane", hn)
        self.m(hn.last, "Smith", hn)

    def test_couples_names_with_conjunction_lastname(self):
        hn = HumanName('John and Jane Aznar y Lopez')
        self.m(hn.first, "John and Jane", hn)
        self.m(hn.last, "Aznar y Lopez", hn)

    def test_couple_titles(self):
        hn = HumanName('Mr. and Mrs. John and Jane Smith')
        self.m(hn.title, "Mr. and Mrs.", hn)
        self.m(hn.first, "John and Jane", hn)
        self.m(hn.last, "Smith", hn)

    def test_title_with_three_part_name_last_initial_is_suffix_uppercase_no_period(self):
        hn = HumanName("King John Alexander V")
        self.m(hn.title, "King", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "V", hn)

    def test_four_name_parts_with_suffix_that_could_be_initial_lowercase_no_period(self):
        hn = HumanName("larry james edward johnson v")
        self.m(hn.first, "larry", hn)
        self.m(hn.middle, "james edward", hn)
        self.m(hn.last, "johnson", hn)
        self.m(hn.suffix, "v", hn)

    @unittest.expectedFailure
    def test_four_name_parts_with_suffix_that_could_be_initial_uppercase_no_period(self):
        hn = HumanName("Larry James Johnson I")
        self.m(hn.first, "Larry", hn)
        self.m(hn.middle, "James", hn)
        self.m(hn.last, "Johnson", hn)
        # if it's in upper case, we currently assume it's an initial
        # it's not really clear if we can assume it's one or the other.
        # If they really are the "first", they are probably used to using a 
        # comma to avoid confusion. Humans know that "Johnson" is a last name,
        # but that wouldn't really be a "simple" nameparser. 
        self.m(hn.suffix, "I", hn)

    # tests for Rev. title (Reverend)
    def test124(self):
        hn = HumanName("Rev. John A. Kenneth Doe")
        self.m(hn.title, "Rev.", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)

    def test125(self):
        hn = HumanName("Rev John A. Kenneth Doe")
        self.m(hn.title, "Rev", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)

    def test126(self):
        hn = HumanName("Doe, Rev. John A. Jr.")
        self.m(hn.title, "Rev.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test127(self):
        hn = HumanName("Buca di Beppo")
        self.m(hn.first, "Buca", hn)
        self.m(hn.last, "di Beppo", hn)

    def test_le_as_last_name(self):
        hn = HumanName("Yin Le")
        self.m(hn.first, "Yin", hn)
        self.m(hn.last, "Le", hn)

    def test_le_as_last_name_with_middle_initial(self):
        hn = HumanName("Yin a Le")
        self.m(hn.first, "Yin", hn)
        self.m(hn.middle, "a", hn)
        self.m(hn.last, "Le", hn)

        # def test_te_as_prefix(self):
        #     hn = HumanName("Te Awanui-a-Rangi Black")
        #     self.m(hn.first,"Te Awanui-a-Rangi", hn)
        #     self.m(hn.last,"Black", hn)
        #
        # 'te' would be part of last name if we added 'te' to PREFIXES
        # def test_te_as_middle_name(self):
        #     hn = HumanName("ye te le")
        #     self.m(hn.first,"ye", hn)
        #     self.m(hn.middle,"te", hn)
        #     self.m(hn.last,"le", hn)
        #
        # def test_te_as_last_name(self):
        #     hn = HumanName("Yin Te")
        #     self.m(hn.first,"Yin", hn)
        #     self.m(hn.last,"Te", hn)


class HumanNameNicknameTestCase(HumanNameTestBase):
    # https://code.google.com/p/python-nameparser/issues/detail?id=33
    def test_nickname_in_parenthesis(self):
        hn = HumanName("Benjamin (Ben) Franklin")
        self.m(hn.first, "Benjamin", hn)
        self.m(hn.middle, "", hn)
        self.m(hn.last, "Franklin", hn)
        self.m(hn.nickname, "Ben", hn)
    
    def test_nickname_in_parenthesis_with_comma(self):
        hn = HumanName("Franklin, Benjamin (Ben)")
        self.m(hn.first, "Benjamin", hn)
        self.m(hn.middle, "", hn)
        self.m(hn.last, "Franklin", hn)
        self.m(hn.nickname, "Ben", hn)
    
    def test_nickname_in_parenthesis_with_comma_and_suffix(self):
        hn = HumanName("Franklin, Benjamin (Ben), Jr.")
        self.m(hn.first, "Benjamin", hn)
        self.m(hn.middle, "", hn)
        self.m(hn.last, "Franklin", hn)
        self.m(hn.suffix, "Jr.", hn)
        self.m(hn.nickname, "Ben", hn)
    
    # it would be hard to support this without breaking some of the
    # other examples with single quotes in the names.
    @unittest.expectedFailure
    def test_nickname_in_single_quotes(self):
        hn = HumanName("Benjamin 'Ben' Franklin")
        self.m(hn.first, "Benjamin", hn)
        self.m(hn.middle, "", hn)
        self.m(hn.last, "Franklin", hn)
        self.m(hn.nickname, "Ben", hn)

    def test_nickname_in_double_quotes(self):
        hn = HumanName("Benjamin \"Ben\" Franklin")
        self.m(hn.first, "Benjamin", hn)
        self.m(hn.middle, "", hn)
        self.m(hn.last, "Franklin", hn)
        self.m(hn.nickname, "Ben", hn)
    
    def test_single_quotes_on_first_name_not_treated_as_nickname(self):
        hn = HumanName("Brian O'connor")
        self.m(hn.first, "Brian", hn)
        self.m(hn.middle, "", hn)
        self.m(hn.last, "O'connor", hn)
        self.m(hn.nickname, "", hn)
    
    def test_single_quotes_on_both_name_not_treated_as_nickname(self):
        hn = HumanName("La'tanya O'connor")
        self.m(hn.first, "La'tanya", hn)
        self.m(hn.middle, "", hn)
        self.m(hn.last, "O'connor", hn)
        self.m(hn.nickname, "", hn)
    
    def test_single_quotes_on_end_of_last_name_not_treated_as_nickname(self):
        hn = HumanName("Mari' Aube'")
        self.m(hn.first, "Mari'", hn)
        self.m(hn.middle, "", hn)
        self.m(hn.last, "Aube'", hn)
        self.m(hn.nickname, "", hn)
    
    #http://code.google.com/p/python-nameparser/issues/detail?id=17
    def test_parenthesis_are_removed(self):
        hn = HumanName("John Jones (Google Docs)")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Jones", hn)
        # not testing the nicknames because we don't actually care
        # about Google Docs.
        
    def test_parenthesis_are_removed2(self):
        hn = HumanName("John Jones (Google Docs), Jr. (Unknown)")
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Jones", hn)
        self.m(hn.suffix, "Jr.", hn)


class HumanNameTitleTestCase(HumanNameTestBase):
    @unittest.expectedFailure
    def test_title_multiple_titles_with_conjunctions(self):
        # I think it finds the index of the wrong 'the'. I get confused because it
        # loops in reverse order.
        hn = HumanName("The Right Hon. the President of the Queen's Bench Division")
        self.m(hn.title, "The Right Hon. the President of the Queen's Bench Division", hn)

    @unittest.expectedFailure
    def test_conjunction_before_title(self):
        # TODO: seems fixable
        hn = HumanName('The Lord of the Universe')
        self.m(hn.title, "The Lord of the Universe", hn)

    def test_double_conjunction_on_title(self):
        hn = HumanName('Lord of the Universe')
        self.m(hn.title, "Lord of the Universe", hn)

    def test_triple_conjunction_on_title(self):
        hn = HumanName('Lord and of the Universe')
        self.m(hn.title, "Lord and of the Universe", hn)

    def test_multiple_conjunctions_on_multiple_titles(self):
        hn = HumanName('Lord of the Universe and Associate Supreme Queen of the World Lisa Simpson')
        self.m(hn.title, "Lord of the Universe and Associate Supreme Queen of the World", hn)
        self.m(hn.first, "Lisa", hn)
        self.m(hn.last, "Simpson", hn)

    def test_title_with_last_initial_is_suffix(self):
        hn = HumanName("King John V.")
        self.m(hn.title, "King", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "V.", hn)

    def test_lc_comparison_of_title(self):
        hn = HumanName("Lt.Gen. John A. Kenneth Doe IV")
        self.m(hn.title, "Lt. Gen.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.suffix, "IV", hn)

    def test_two_part_title(self):
        hn = HumanName("Lt. Gen. John A. Kenneth Doe IV")
        self.m(hn.title, "Lt. Gen.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.suffix, "IV", hn)

    def test_two_part_title_with_lastname_comma(self):
        hn = HumanName("Doe, Lt. Gen. John A. Kenneth IV")
        self.m(hn.title, "Lt. Gen.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.suffix, "IV", hn)

    def test_two_part_title_with_suffix_comma(self):
        hn = HumanName("Lt. Gen. John A. Kenneth Doe, Jr.")
        self.m(hn.title, "Lt. Gen.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A. Kenneth", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test_possible_conflict_with_middle_initial_that_could_be_suffix(self):
        hn = HumanName("Doe, Rev. John V, Jr.")
        self.m(hn.title, "Rev.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "V", hn)
        self.m(hn.suffix, "Jr.", hn)

    def test_possible_conflict_with_suffix_that_could_be_initial(self):
        hn = HumanName("Doe, Rev. John A., V, Jr.")
        self.m(hn.title, "Rev.", hn)
        self.m(hn.first, "John", hn)
        self.m(hn.last, "Doe", hn)
        self.m(hn.middle, "A.", hn)
        self.m(hn.suffix, "V, Jr.", hn)

    # 'ben' is removed from PREFIXES in v0.2.5
    # this test could re-enable this test if we decide to support 'ben' as a prefix
    # def test_ben_as_conjunction(self):
    #     hn = HumanName("Ahmad ben Husain")
    #     self.m(hn.first,"Ahmad", hn)
    #     self.m(hn.last,"ben Husain", hn)

    def test_ben_as_first_name(self):
        hn = HumanName("Ben Johnson")
        self.m(hn.first, "Ben", hn)
        self.m(hn.last, "Johnson", hn)

    def test_ben_as_first_name_with_middle_name(self):
        hn = HumanName("Ben Alex Johnson")
        self.m(hn.first, "Ben", hn)
        self.m(hn.middle, "Alex", hn)
        self.m(hn.last, "Johnson", hn)

    def test_ben_as_middle_name(self):
        hn = HumanName("Alex Ben Johnson")
        self.m(hn.first, "Alex", hn)
        self.m(hn.middle, "Ben", hn)
        self.m(hn.last, "Johnson", hn)

    # http://code.google.com/p/python-nameparser/issues/detail?id=13
    def test_last_name_also_prefix(self):
        hn = HumanName("Jane Doctor")
        self.m(hn.first, "Jane", hn)
        self.m(hn.last, "Doctor", hn)

    @unittest.expectedFailure
    def test_title_as_suffix(self):
        """
        Semantically, PhD is a title, not a suffix. 
        http://code.google.com/p/python-nameparser/issues/detail?id=7
        """
        hn = HumanName("J. Smith, PhD")
        self.m(hn.title, "PhD", hn)
        self.m(hn.first, "J.", hn)
        self.m(hn.last, "Smith", hn)


class HumanNameCapitalizationTestCase(HumanNameTestBase):
    def test_capitalization_exception_for_III(self):
        hn = HumanName('juan q. xavier velasquez y garcia iii')
        hn.capitalize()
        self.m(str(hn), 'Juan Q. Xavier Velasquez y Garcia III', hn)

    # FIXME: this test does not pass due to a known issue
    # http://code.google.com/p/python-nameparser/issues/detail?id=22
    @unittest.expectedFailure
    def test_capitalization_exception_for_already_capitalized_III_KNOWN_FAILURE(self):
        hn = HumanName('juan garcia III')
        hn.capitalize()
        self.m(str(hn), 'Juan Garcia III', hn)

    def test_capitalize_title(self):
        hn = HumanName('lt. gen. john a. kenneth doe iv')
        hn.capitalize()
        self.m(str(hn), 'Lt. Gen. John A. Kenneth Doe IV', hn)

    # Capitalization with M(a)c and hyphenated names
    def test_capitalization_with_Mac_as_hyphenated_names(self):
        hn = HumanName('donovan mcnabb-smith')
        hn.capitalize()
        self.m(str(hn), 'Donovan McNabb-Smith', hn)

    # Leaving already-capitalized names alone
    def test123(self):
        hn = HumanName('Shirley Maclaine')
        hn.capitalize()
        self.m(str(hn), 'Shirley Maclaine', hn)

    def test_capitalize_diacritics(self):
        hn = HumanName(u'matth\xe4us schmidt')
        hn.capitalize()
        self.m(u(hn), u'Matth\xe4us Schmidt', hn)

    # http://code.google.com/p/python-nameparser/issues/detail?id=15
    def test_downcasing_mac(self):
        hn = HumanName('RONALD MACDONALD')
        hn.capitalize()
        self.m(str(hn), 'Ronald MacDonald', hn)

    # http://code.google.com/p/python-nameparser/issues/detail?id=23
    def test_downcasing_mc(self):
        hn = HumanName('RONALD MCDONALD')
        hn.capitalize()
        self.m(str(hn), 'Ronald McDonald', hn)


class HumanNameOutputFormatTests(HumanNameTestBase):
    def test_formating(self):
        hn = HumanName("Rev John A. Kenneth Doe III")
        hn.string_format = "{title} {first} {middle} {last} {suffix}"
        self.assertEqual(u(hn), "Rev John A. Kenneth Doe III")
        hn.string_format = "{last}, {title} {first} {middle}, {suffix}"
        self.assertEqual(u(hn), "Doe, Rev John A. Kenneth, III")


TEST_NAMES = (
    "John Doe",
    "John Doe, Jr.",
    "John Doe III",
    "Doe, John",
    "Doe, John, Jr.",
    "Doe, John III",
    "John A. Doe",
    "John A. Doe, Jr.",
    "John A. Doe III",
    "Doe, John A.",
    "Doe, John A., Jr.",
    "Doe, John A. III",
    "John A. Kenneth Doe",
    "John A. Kenneth Doe, Jr.",
    "John A. Kenneth Doe III",
    "Doe, John A. Kenneth",
    "Doe, John A. Kenneth, Jr.",
    "Doe, John A. Kenneth III",
    "Dr. John Doe",
    "Dr. John Doe, Jr.",
    "Dr. John Doe III",
    "Doe, Dr. John",
    "Doe, Dr. John, Jr.",
    "Doe, Dr. John III",
    "Dr. John A. Doe",
    "Dr. John A. Doe, Jr.",
    "Dr. John A. Doe III",
    "Doe, Dr. John A.",
    "Doe, Dr. John A. Jr.",
    "Doe, Dr. John A. III",
    "Dr. John A. Kenneth Doe",
    "Dr. John A. Kenneth Doe, Jr.",
    "Dr. John A. Kenneth Doe III",
    "Doe, Dr. John A. Kenneth",
    "Doe, Dr. John A. Kenneth Jr.",
    "Doe, Dr. John A. Kenneth III",
    "Juan de la Vega",
    "Juan de la Vega, Jr.",
    "Juan de la Vega III",
    "de la Vega, Juan",
    "de la Vega, Juan, Jr.",
    "de la Vega, Juan III",
    "Juan Velasquez y Garcia",
    "Juan Velasquez y Garcia, Jr.",
    "Juan Velasquez y Garcia III",
    "Velasquez y Garcia, Juan",
    "Velasquez y Garcia, Juan, Jr.",
    "Velasquez y Garcia, Juan III",
    "Dr. Juan de la Vega",
    "Dr. Juan de la Vega, Jr.",
    "Dr. Juan de la Vega III",
    "de la Vega, Dr. Juan",
    "de la Vega, Dr. Juan, Jr.",
    "de la Vega, Dr. Juan III",
    "Dr. Juan Velasquez y Garcia",
    "Dr. Juan Velasquez y Garcia, Jr.",
    "Dr. Juan Velasquez y Garcia III",
    "Velasquez y Garcia, Dr. Juan",
    "Velasquez y Garcia, Dr. Juan, Jr.",
    "Velasquez y Garcia, Dr. Juan III",
    "Juan Q. de la Vega",
    "Juan Q. de la Vega, Jr.",
    "Juan Q. de la Vega III",
    "de la Vega, Juan Q.",
    "de la Vega, Juan Q., Jr.",
    "de la Vega, Juan Q. III",
    "Juan Q. Velasquez y Garcia",
    "Juan Q. Velasquez y Garcia, Jr.",
    "Juan Q. Velasquez y Garcia III",
    "Velasquez y Garcia, Juan Q.",
    "Velasquez y Garcia, Juan Q., Jr.",
    "Velasquez y Garcia, Juan Q. III",
    "Dr. Juan Q. de la Vega",
    "Dr. Juan Q. de la Vega, Jr.",
    "Dr. Juan Q. de la Vega III",
    "de la Vega, Dr. Juan Q.",
    "de la Vega, Dr. Juan Q., Jr.",
    "de la Vega, Dr. Juan Q. III",
    "Dr. Juan Q. Velasquez y Garcia",
    "Dr. Juan Q. Velasquez y Garcia, Jr.",
    "Dr. Juan Q. Velasquez y Garcia III",
    "Velasquez y Garcia, Dr. Juan Q.",
    "Velasquez y Garcia, Dr. Juan Q., Jr.",
    "Velasquez y Garcia, Dr. Juan Q. III",
    "Juan Q. Xavier de la Vega",
    "Juan Q. Xavier de la Vega, Jr.",
    "Juan Q. Xavier de la Vega III",
    "de la Vega, Juan Q. Xavier",
    "de la Vega, Juan Q. Xavier, Jr.",
    "de la Vega, Juan Q. Xavier III",
    "Juan Q. Xavier Velasquez y Garcia",
    "Juan Q. Xavier Velasquez y Garcia, Jr.",
    "Juan Q. Xavier Velasquez y Garcia III",
    "Velasquez y Garcia, Juan Q. Xavier",
    "Velasquez y Garcia, Juan Q. Xavier, Jr.",
    "Velasquez y Garcia, Juan Q. Xavier III",
    "Dr. Juan Q. Xavier de la Vega",
    "Dr. Juan Q. Xavier de la Vega, Jr.",
    "Dr. Juan Q. Xavier de la Vega III",
    "de la Vega, Dr. Juan Q. Xavier",
    "de la Vega, Dr. Juan Q. Xavier, Jr.",
    "de la Vega, Dr. Juan Q. Xavier III",
    "Dr. Juan Q. Xavier Velasquez y Garcia",
    "Dr. Juan Q. Xavier Velasquez y Garcia, Jr.",
    "Dr. Juan Q. Xavier Velasquez y Garcia III",
    "Velasquez y Garcia, Dr. Juan Q. Xavier",
    "Velasquez y Garcia, Dr. Juan Q. Xavier, Jr.",
    "Velasquez y Garcia, Dr. Juan Q. Xavier III",
    "John Doe, CLU, CFP, LUTC",
    "John P. Doe, CLU, CFP, LUTC",
    "Dr. John P. Doe-Ray, CLU, CFP, LUTC",
    "Doe-Ray, Dr. John P., CLU, CFP, LUTC",
    "Hon. Barrington P. Doe-Ray, Jr.",
    "Doe-Ray, Hon. Barrington P. Jr.",
    "Doe-Ray, Hon. Barrington P. Jr., CFP, LUTC",
    "Hon Oladapo",
    "Jose Aznar y Lopez",
    "John E Smith",
    "John e Smith",
    "John and Jane Smith",
    "Rev. John A. Kenneth Doe",
    "Donovan McNabb-Smith",
    "Rev John A. Kenneth Doe",
    "Doe, Rev. John A. Jr.",
    "Buca di Beppo",
    "Lt. Gen. John A. Kenneth Doe, Jr.",
    "Doe, Lt. Gen. John A. Kenneth IV",
    "Lt. Gen. John A. Kenneth Doe IV",
    'Mr. and Mrs. John Smith',
    'John Jones (Google Docs)',
    'john e jones',
    'john e jones, III',
    'jones, john e',
    'E.T. Smith',
    'E.T. Smith, II',
    'Smith, E.T., Jr.',
    'A.B. Vajpayee',
    'Rt. Hon. Paul E. Mary',
    'Maid Marion',
    'Amy E. Maid',
    'Jane Doctor',
    'Doctor, Jane E.',
    'dr. ben alex johnson III',
    'Lord of the Universe and Supreme King of the World Lisa Simpson',
    'Benjamin (Ben) Franklin',
    'Benjamin "Ben" Franklin',
    "Brian O'connor",
)


class HumanNameVariationTests(HumanNameTestBase):
    # test automated variations of names in TEST_NAMES.
    # Helps test that the 3 code trees work the same

    TEST_NAMES = TEST_NAMES

    def test_variations_of_TEST_NAMES(self):
        for name in self.TEST_NAMES:
            hn = HumanName(name)
            if len(hn.suffix_list) > 1:
                hn = HumanName("{title} {first} {middle} {last} {suffix}".format(**hn._dict).split(',')[0])
            nocomma = HumanName("{title} {first} {middle} {last} {suffix}".format(**hn._dict))
            lastnamecomma = HumanName("{last}, {title} {first} {middle} {suffix}".format(**hn._dict))
            suffixcomma = HumanName("{title} {first} {middle} {last}, {suffix}".format(**hn._dict))
            for attr in hn._members:
                self.m(getattr(hn, attr), getattr(nocomma, attr), hn)
                self.m(getattr(hn, attr), getattr(lastnamecomma, attr), hn)
                if hn.suffix:
                    self.m(getattr(hn, attr), getattr(suffixcomma, attr), hn)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        log.setLevel(logging.ERROR)
        log.addHandler(logging.StreamHandler())
        name = sys.argv[1]
        hn = HumanName(name)
        print((repr(hn)))
    else:
        if log.level > 0:
            for name in TEST_NAMES:
                hn = HumanName(name)
                print((u(name)))
                print((u(hn)))
                print((repr(hn)))
                print("\n-------------------------------------------\n")
        unittest.main()
