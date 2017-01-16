#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import

import sys
import unittest


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)

        # Fix encoding problem in python 2.7
        try:
            reload(sys)
            sys.setdefaultencoding('utf-8')
        except NameError as e:
            pass
