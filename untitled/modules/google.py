# coding=utf-8
from __future__ import unicode_literals

import re
from bs4 import BeautifulSoup
from datetime import datetime
from requests import Session
from requests import Timeout

from untitled.logger import setup_logger
from untitled.models.googleresult import GoogleResult


class Google(object):
    _BASE_URL = 'https://www.google.co.uk{}'
    _SEARCH_URL = _BASE_URL.format('/search?q={}')
    _SITE_PAT = 'site:{} {}'

    def __init__(self, called_by=None):
        self.session = Session()
        self.log = setup_logger('{} Google'.format(called_by) if called_by else 'Google')

    def site(self, site_url, keyword):
        clean_site_url = re.sub('http(s)://', '', site_url)
        query = self._SITE_PAT.format(clean_site_url, keyword)
        search_url = self._SEARCH_URL.format(query)

        try:
            response = self.session.get(search_url)
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')

            results = soup.find_all('div', class_='g')
            # TODO: add exception handler
            google_results = []
            # TODO: currently retrieve only first page
            for result in results:
                title = result.a.text
                url = result.cite.text

                desc = result.find('span', class_='st').text
                # try to parse date, if any
                date = None
                try:
                    date = datetime.strptime(' '.join(desc.split(' ')[0:3]), '%d %b %Y')
                    desc = ' '.join(desc.split(' ')[3:])
                except ValueError:
                    pass

                google_result = GoogleResult()
                google_result.title = title
                google_result.url = url
                google_result.desc = desc
                if date:
                    google_result.date = date
                google_results.append(google_result)

            return google_results
        except Timeout as e:
            raise RuntimeError('Google is down? Seriously?: {}'.format(e))
