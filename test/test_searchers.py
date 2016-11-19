#!/usr/bin/env python
# coding=utf-8

import unittest

from untitled.searchers import ExploitDB, PacketStorm, SecurityFocus, ZeroDayToday


class TestSearcherCVE(unittest.TestCase):
    def setUp(self):
        # Dirty COW CVE
        self.cve = 'CVE-2016-5195'
        self.limit = 5

    def test_exploitdb(self):
        exploitdb = ExploitDB(_cve=self.cve, _verbose=True, _limit=self.limit)
        exploitdb.findExploits()
        self.assertGreater(len(exploitdb.exploits), 0, 'Exploit-db could not find any Dirty COW exploit')

    def test_packetstorm(self):
        packetstorm = PacketStorm(_cve=self.cve, _verbose=True, _limit=self.limit)
        packetstorm.findExploits()
        self.assertGreater(len(packetstorm.exploits), 0, 'PacketStorm could not find any Dirty COW exploit')

    def test_zerodaytoday(self):
        zerodaytoday = ZeroDayToday(_cve=self.cve, _verbose=True, _limit=self.limit)
        zerodaytoday.findExploits()
        self.assertGreater(len(zerodaytoday.exploits), 0, '0day.today could not find any Dirty COW exploit')

    def test_securityfocus(self):
        securityfocus = SecurityFocus(_cve=self.cve, _verbose=True, _limit=self.limit)
        securityfocus.findExploits()
        self.assertGreater(len(securityfocus.exploits), 0, 'SecurityFocus could not find any Dirty COW exploit')


class TestSearcherPhrase(unittest.TestCase):
    def setUp(self):
        self.phrase = 'Dirty COW'
        self.limit = 5

    def test_exploitdb(self):
        exploitdb = ExploitDB(_search_string=self.phrase, _verbose=True, _limit=self.limit)
        exploitdb.findExploits()
        self.assertGreater(len(exploitdb.exploits), 0, 'Exploit-db could not find any Dirty COW exploit')

    def test_packetstorm(self):
        packetstorm = PacketStorm(_search_string=self.phrase, _verbose=True, _limit=self.limit)
        packetstorm.findExploits()
        self.assertGreater(len(packetstorm.exploits), 0, 'PacketStorm could not find any Dirty COW exploit')

    def test_zerodaytoday(self):
        zerodaytoday = ZeroDayToday(_search_string=self.phrase, _verbose=True, _limit=self.limit)
        zerodaytoday.findExploits()
        self.assertGreater(len(zerodaytoday.exploits), 0, '0day.today could not find any Dirty COW exploit')

    def test_securityfocus(self):
        securityfocus = SecurityFocus(_search_string=self.phrase, _verbose=True, _limit=self.limit)
        securityfocus.findExploits()
        self.assertGreater(len(securityfocus.exploits), 0, 'SecurityFocus could not find any Dirty COW exploit')
