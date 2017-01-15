#!/usr/bin/env python
# coding=utf-8

from epherousa.modules.google import Google
from epherousa.test.base_test import BaseTest


class TestGoogle(BaseTest):
    def setUp(self):
        self.google = Google()
        self.test_site = 'exploit-db.com'
        self.test_kw = 'dirty cow'

    def test_site(self):
        results = self.google.site(self.test_site, self.test_kw)
        self.assertGreater(len(results), 0, 'Google cannot find {} exploit on {}'.format(self.test_kw, self.test_site))
        for result in results:
            self.assertTrue(self.test_site in result.url, 'Google result grabbed incorrect URL')
