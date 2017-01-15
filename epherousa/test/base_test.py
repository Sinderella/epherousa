#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import

import unittest


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
