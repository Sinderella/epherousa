# coding=utf-8
import re
from datetime import datetime

from bs4 import BeautifulSoup
from requests import Session

from untitled import Exploit
from untitled.modules.google import Google
from .Searcher import Searcher


class SecurityFocus(Searcher):
    def setup(self):
        super(SecurityFocus, self).setup()
        self.url = 'http://www.securityfocus.com{}'
        self.search_url = self.url.format('/bid')

        self.description = 'Searches securityfocus.com for exploits'

    def findExploitsByCVE(self):
        session = Session()
        self.log.debug('Posting search form: {} with {}'.format(self.search_url, self.cve))
        response = session.post(self.search_url, data={'CVE': self.cve, 'op': 'display_list', 'c': 12},
                                headers={'User-Agent': 'Mozilla/5.0'})

        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        # retrieve table with style, it has no class or ID to identify
        table = soup.find_all('div', style='padding: 4px;')
        if len(table) == 0:
            self.log.error('Could not find a list, web layout may have changed. Please create an issue on the project.')
            raise RuntimeError(
                'Could not find a list, web layout may have changed. Please create an issue on the project.')

        # TODO: currently does not respect limit, but retrieve only first page
        try:
            # parse table, one exploit row has 11 HTML tags
            for idx in range(0, len(table[0].contents), 11):
                exploit = Exploit()
                exploit.cve = self.cve
                exploit.desc = table[0].contents[idx + 1].text
                exploit.date = datetime.strptime(table[0].contents[idx + 4].text, "%Y-%m-%d")
                exploit.url = table[0].contents[idx + 7].text
                self.exploits.append(exploit)
        except AttributeError as e:
            self.log.error('Could not find an attribute, web layout may have changed. Please create an issue on '
                           'the project. {}'.format(e))
            raise RuntimeError(
                'Could not find a list, web layout may have changed. Please create an issue on the project. '
                '{}'.format(e))

    def findExploitsByString(self):
        google = Google()
        google_results = google.site(self.url.format(''), self.search_string)

        session = Session()
        # TODO: currently does not respect limit, but retrieve only first page
        # only get URL with '/bid/'
        for result in google_results:
            if '/bid/' in result.url:
                # return info page to users
                if result.url[-1].isdecimal():
                    clean_url = 'http://' + result.url
                else:
                    clean_url = 'http://' + result.url[0:result.url.rfind('/')]
                # retrieving more info (CVE/date)
                response = session.get(clean_url)
                content = response.content
                soup = BeautifulSoup(content, 'html.parser')
                title = soup.find('span', class_='title').text
                cve = None
                date = None
                for content in soup.find_all('table')[2].contents:
                    try:
                        text = content.text
                        if 'CVE' in text:
                            text = re.sub(r'[\t\n]', '', text)
                            cve = text.split(':')[1]
                        if 'Published' in text:
                            text = re.sub(r'[\t\n]', '', text)
                            date = text.split(':')[1]
                            date = ' '.join(date.split(' ')[0:3])
                            date = datetime.strptime(date, '%b %d %Y')
                    except AttributeError:
                        pass
                exploit = Exploit()
                if cve:
                    exploit.cve = cve
                if date:
                    exploit.date = date
                exploit.desc = title
                exploit.url = clean_url
                self.exploits.append(exploit)
