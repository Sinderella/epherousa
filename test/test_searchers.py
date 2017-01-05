#!/usr/bin/env python
# coding=utf-8

import unittest

from epherousa.searchers.ExploitDB import ExploitDB
from epherousa.searchers.PacketStorm import PacketStorm
from epherousa.searchers.SecurityFocus import SecurityFocus


class TestSearcherCVE(unittest.TestCase):
    def setUp(self):
        # Dirty COW CVE
        self.cve = 'CVE-2016-5195'
        # just for exploitdb
        self.exploitdb_cve = 'CVE-2016-5840'
        self.limit = 5

    def test_exploitdb(self):
        exploitdb = ExploitDB(_cve=self.exploitdb_cve, _limit=self.limit)
        exploitdb.find_exploits()
        self.assertGreater(len(exploitdb.exploits), 0,
                           'Exploit-db could not find any {} exploit'.format(self.exploitdb_cve))

    def test_packetstorm(self):
        packetstorm = PacketStorm(_cve=self.cve, _limit=self.limit)
        packetstorm.find_exploits()
        self.assertGreater(len(packetstorm.exploits), 0, 'PacketStorm could not find any Dirty COW exploit')

    # def test_zerodaytoday(self):
    #     zerodaytoday = ZeroDayToday(_cve=self.cve, _limit=self.limit)
    #     zerodaytoday.find_exploits()
    #     self.assertGreater(len(zerodaytoday.exploits), 0, '0day.today could not find any Dirty COW exploit')

    def test_securityfocus(self):
        securityfocus = SecurityFocus(_cve=self.cve, _limit=self.limit)
        securityfocus.find_exploits()
        self.assertGreater(len(securityfocus.exploits), 0, 'SecurityFocus could not find any Dirty COW exploit')


class TestSearcherPhrase(unittest.TestCase):
    def setUp(self):
        self.phrase = 'Dirty COW'
        self.limit = 5

    def test_exploitdb(self):
        exploitdb = ExploitDB(_search_string=self.phrase, _limit=self.limit)
        exploitdb.find_exploits()
        self.assertGreater(len(exploitdb.exploits), 0, 'Exploit-db could not find any Dirty COW exploit')

    def test_packetstorm(self):
        packetstorm = PacketStorm(_search_string=self.phrase, _limit=self.limit)
        packetstorm.find_exploits()
        self.assertGreater(len(packetstorm.exploits), 0, 'PacketStorm could not find any Dirty COW exploit')

    # def test_zerodaytoday(self):
    #     zerodaytoday = ZeroDayToday(_search_string=self.phrase, _limit=self.limit)
    #     zerodaytoday.find_exploits()
    #     self.assertGreater(len(zerodaytoday.exploits), 0, '0day.today could not find any Dirty COW exploit')

    def test_securityfocus(self):
        securityfocus = SecurityFocus(_search_string=self.phrase, _limit=self.limit)
        securityfocus.find_exploits()
        self.assertGreater(len(securityfocus.exploits), 0, 'SecurityFocus could not find any Dirty COW exploit')
