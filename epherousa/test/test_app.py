#!/usr/bin/env python
# coding=utf-8
import os
import unittest


class TestApp(unittest.TestCase):
    def setUp(self):
        self.command = 'ephe {1} \'{0}\''

        # Dirty COW CVE
        self.cve = 'CVE-2016-5195'
        self.phrase = 'Dirty COW'

    def test_cve(self):
        return_code = os.system(self.command.format(self.cve, ''))
        self.assertEqual(return_code, 0)

    def test_cve_verbose(self):
        return_code = os.system(self.command.format(self.cve, '-v'))
        self.assertEqual(return_code, 0)

    def test_cve_quiet(self):
        return_code = os.system(self.command.format(self.cve, '-q'))
        self.assertEqual(return_code, 0)

    def test_phrase(self):
        return_code = os.system(self.command.format(self.phrase, ''))
        self.assertEqual(return_code, 0)

    def test_phrase_verbose(self):
        return_code = os.system(self.command.format(self.phrase, '-v'))
        self.assertEqual(return_code, 0)

    def test_phrase_quiet(self):
        return_code = os.system(self.command.format(self.phrase, '-q'))
        self.assertEqual(return_code, 0)
