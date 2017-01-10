# coding=utf-8
import re
from bs4 import BeautifulSoup
from datetime import datetime
from requests import Session

from epherousa.modules.google import Google
from .common import Searcher, Exploit


class SecurityFocus(Searcher):
    _URL = 'http://www.securityfocus.com{}'
    _SEARCH_URL = _URL.format('/bid')
    _DESCRIPTION = 'Searches securityfocus.com for exploits'

    @staticmethod
    def _format_cve(cve):
        if len(cve) <= 13:
            return cve

        tmp = cve[0:13]
        for i in range(13, len(cve), 13):
            tmp += ',{}'.format(cve[i:i + 13])
        return tmp

    def find_exploits_by_cve(self):
        self.log.debug('Posting search form: {} with {}'.format(self._SEARCH_URL, self.cve))
        response = self.session.post(self._SEARCH_URL, data={'CVE': self.cve, 'op': 'display_list', 'c': 12})

        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        # retrieve table with style, it has no class or ID to identify
        table = soup.find_all('div', style='padding: 4px;')
        if len(table) == 0:
            self.log.error(
                'Could not find a list, web layout may have changed. Please create an issue on the project.')
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
        except IndexError as e:
            self.log.notice('SecurityFocus returned no results.')
            
    def find_exploits_by_string(self):
        google = Google()
        google_results = google.site(self._URL.format(''), self.search_string)

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
                if any(clean_url == exploit.url for exploit in self.exploits):
                    continue
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
                    exploit.cve = self._format_cve(cve)
                if date:
                    exploit.date = date
                exploit.desc = title
                exploit.url = clean_url
                self.exploits.append(exploit)
