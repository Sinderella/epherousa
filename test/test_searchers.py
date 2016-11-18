#!/usr/bin/env python
# coding=utf-8

import sys
import unittest

from untitled.searchers import ExploitDB, PacketStorm, ZeroDayToday


class TestSearcherCVE(unittest.TestCase):
    def setUp(self):
        try:
            reload(sys)
            sys.setdefaultencoding('utf-8')
        except NameError as e:
            pass
        # Dirty COW CVE
        self.cve = 'CVE-2016-5195'
        self.limit = 5

    def test_exploitdb(self):
        exploitdb = ExploitDB(_cve=self.cve, _verbose=True, _limit=self.limit)
        exploitdb.findExploits()
        self.assertGreater(len(exploitdb.exploits), 0, 'Exploit-db could not find any Dirty COW exploit')

    def test_packetstorm(self):
        exploitdb = PacketStorm(_cve=self.cve, _verbose=True, _limit=self.limit)
        exploitdb.findExploits()
        self.assertGreater(len(exploitdb.exploits), 0, 'PacketStorm could not find any Dirty COW exploit')

    def test_zerodaytoday(self):
        exploitdb = ZeroDayToday(_cve=self.cve, _verbose=True, _limit=self.limit)
        exploitdb.findExploits()
        self.assertGreater(len(exploitdb.exploits), 0, '0day.today could not find any Dirty COW exploit')
