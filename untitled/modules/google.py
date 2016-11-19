# coding=utf-8
from __future__ import unicode_literals

import re
from datetime import datetime

from bs4 import BeautifulSoup
from requests import Session

from untitled.logger import setup_logger
from untitled.models.googleresult import GoogleResult


class Google(object):
    def __init__(self, called_by=None):
        self.session = Session()
        self.log = setup_logger('{} Google'.format(called_by) if called_by else 'Google')

        self.base_url = 'https://www.google.co.uk{}'
        self.search_url = self.base_url.format('/search?q={}')
        self.site_pat = 'site:{} {}'

    def site(self, site_url, keyword):
        clean_site_url = re.sub('http(s)://', '', site_url)
        query = self.site_pat.format(clean_site_url, keyword)
        search_url = self.search_url.format(query)

        response = self.session.get(search_url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        results = soup.find_all('div', class_='g')
        google_results = []
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
