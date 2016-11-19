# coding=utf-8
from datetime import datetime

from bs4 import BeautifulSoup
from requests import Session

from untitled import Exploit
from .Searcher import Searcher


class SecurityFocus(Searcher):
    def setup(self):
        self.url = 'http://www.securityfocus.com{}'
        self.search_url = self.url.format('/bid')

        self.description = 'Searches securityfocus.com for exploits'

    def findExploitsByCVE(self):
        session = Session()
        response = session.post(self.search_url, data={'CVE': self.cve, 'op': 'display_list', 'c': 12},
                                headers={'User-Agent': 'Mozilla/5.0'})

        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        # retrieve table with style, it has no class or ID to identify
        table = soup.find_all('div', style='padding: 4px;')

        # parse table, one exploit row has 11 HTML tags
        for idx in range(0, len(table[0].contents), 11):
            exploit = Exploit()
            exploit.cve = self.cve
            exploit.desc = table[0].contents[idx+1].text
            exploit.date = datetime.strptime(table[0].contents[idx+4].text, "%Y-%m-%d")
            exploit.url = table[0].contents[idx+7].text
            self.exploits.append(exploit)

    def findExploitsByString(self):
        pass
