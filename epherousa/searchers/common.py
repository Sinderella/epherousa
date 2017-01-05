# coding=utf-8
from __future__ import unicode_literals, print_function

import re
from datetime import datetime
from requests import ConnectionError
from requests import Session
from requests import Timeout
from epherousa.logger import setup_logger
from ..libraries.pycvesearch.core import CVESearch

class Searcher(object):
    """A template class for the exploit searchers"""
    _USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'}
    _CVE_PATTERN = re.compile('CVE-\d{4}-\d{4,7}')

    def __init__(self, _cve="", _search_string="", _verbose=False, _limit=0):
        self.exploits = []

        self.session = self._setup_session()
        self.cve = _cve
        self.search_string = _search_string
        self.verbose = _verbose
        self.limit = _limit
        self.log = setup_logger(self.__str__())
        if self.verbose:
            self.log.level = self.verbose

        self.setup()

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return '\'{}\''.format(self.__class__.__name__)

    def setup(self):
        """Called at the end of init to make initial setup easier for searchers"""
        self.log.debug('Setting up searcher: {}'.format(self.__str__()))

    def _setup_session(self):
        session = Session()
        session.headers.update(self._USER_AGENT)
        return session

    def test_cvesearch(self):
        cve = CVESearch()
        print(cve.dbinfo())
        #data = cve.id('CVE-2008-4250')
        #data = {k.decode('utf8'): v.decode('utf8') for k, v in data.items()}
        #print(data)

    def find_exploits(self):
        """Update self.exploits after searching"""
        try:
            if self.cve != "":
                self.find_exploits_by_cve()
                self.test_cvesearch()
            else:
                self.test_cvesearch()
                self.find_exploits_by_string()
            self.log.debug('Found {} exploits'.format(len(self.exploits)))
        except Timeout as e:
            self.log.error('Timed out, {} is down, try again later...: {}'.format(self, e))
        except ConnectionError as e:
            self.log.error('{} is down, check if the site is not taken down: {}'.format(self, e))
        except RuntimeError as e:
            self.log.error('Something has gone wrong: {}'.format(e))

    def find_exploits_by_cve(self):
        """Searches the database using self.cve"""

    def find_exploits_by_string(self):
        """Searches the database using self.search string"""

    def print_exploits(self):
        """Print the contents of self.exploits, only up to the limit of the searcher"""
        if self.limit == 0:
            for e in self.exploits:
                e.print_exploit()
        else:
            for e in self.exploits[:self.limit]:
                e.print_exploit()


class Exploit:
    """A class to hold all of the information about a particular exploit"""

    # Initially this defines the min width for each column (see calculate_widths)
    column_widths = {"cve": 14, "desc": 12, "cost": 5, "date": 11, "url": 4}

    def __init__(self, _cve="", _date=None, _desc="", _cost=0, _url=""):
        self.cve = _cve
        self.desc = _desc
        self.cost = _cost
        self.date = _date
        self.url = _url

    @staticmethod
    def print_formatted(var, name, end_line=False):
        str_format = "| {:" + str(Exploit.column_widths[name]) + "}"
        out = str_format.format(str(var))
        out = out[:Exploit.column_widths[name] + 2]  # Cut the string if necessary
        if end_line:
            out += "|"
            end = "\n"
        else:
            end = ""

        print(out, end=end)

    def print_exploit(self):
        """Prints the exploit in a standardised way"""
        date_string = datetime.strftime(self.date, "%Y-%m-%d")
        self.print_formatted(self.cve, "cve")
        self.print_formatted(self.desc, "desc")
        self.print_formatted(date_string, "date")
        # just commented out so it doesn't print the cost column (issue #19)
        # self.print_formatted(self.cost, "cost")
        self.print_formatted(self.url, "url", end_line=True)

    @staticmethod
    def get_total_width():
        total_width = 1  # Account for the final bar that is printed
        for key in Exploit.column_widths:
            # added this condition so it doesn't print the cost column (issue #19)
            if key == 'cost':
                continue
            total_width += Exploit.column_widths[key] + 2  # +2 to account for the "| "
        return total_width

    @staticmethod
    def calculate_widths(searchers):
        """Takes a list of searchers and makes each column wide enough for the longest item
        that will be displayed in it"""
        # Note that the date is always the same length since it is printed in a given format
        exploits = []
        for s in searchers:
            exploits.extend(s.exploits)

        if len(exploits) == 0:
            return  # Otherwise we get a crash for trying evaluate max of an empty sequence

        widths = {}
        widths["cve"] = max([len(e.cve) for e in exploits])
        widths["desc"] = max([len(e.desc) for e in exploits])
        # just commented out so it doesn't print the cost column (issue #19)
        # widths["cost"] = max([len(str(e.cost)) for e in exploits])
        # +1 so the pipe ('|') doesn't be a part of the URL as it's next to the URL
        widths["url"] = max([len(e.url) for e in exploits]) + 1

        for key in widths:
            Exploit.column_widths[key] = max(Exploit.column_widths[key], widths[key])

    @staticmethod
    def print_header():
        """Print the table header for the exploit table"""
        total_width = Exploit.get_total_width()
        print("_" * total_width)

        Exploit.print_formatted("CVE", "cve")
        Exploit.print_formatted("Description", "desc")
        Exploit.print_formatted("Date", "date")
        # just commented out so it doesn't print the cost column (issue #19)
        # Exploit.print_formatted("Cost", "cost")
        Exploit.print_formatted("URL", "url", end_line=True)

        print("_" * total_width)

    @staticmethod
    def print_footer():
        total_width = Exploit.get_total_width()
        print("_" * total_width)
