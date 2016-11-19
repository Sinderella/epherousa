# coding=utf-8
from __future__ import unicode_literals

from datetime import datetime


class GoogleResult(object):
    def __init__(self):
        self._title = None
        self._url = None
        self._desc = None
        self._date = None

    def __repr__(self):
        return self.title

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc = desc

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if not isinstance(date, datetime):
            raise AttributeError('date only accepts datetime object')
        self._date = date
