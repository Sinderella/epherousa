# coding=utf-8

from bs4 import BeautifulSoup
from requests import Session

from .Searcher import Searcher


class SecurityFocus(Searcher):
    def setup(self):
        self.url = 'http://www.securityfocus.com{}'
        self.search_url = self.url.format('/bid')

        self.description = 'Searches packetstormsecurity.com for exploits'

    def findExploitsByCVE(self):
        session = Session()
        response = session.post(self.search_url, data={'CVE': self.cve, 'op': 'display_list', 'c': 12},
                                headers={'User-Agent': 'Mozilla/5.0'})

        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find_all('div', style='padding: 4px;')
        i = 0
        for child in table[0].descendants:
            print('{}: {}'.format(i, child))
            i += 1

    def findExploitsByString(self):
        pass
