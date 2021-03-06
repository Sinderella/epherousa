# coding=utf-8
from __future__ import unicode_literals, print_function

import re
from datetime import datetime

from colorama import Fore, Style
from logbook import DEBUG, NOTICE
from requests import ConnectionError
from requests import Timeout
from requests.exceptions import SSLError

from epherousa.logger import setup_logger
from epherousa.modules.requester import Requester


class Searcher(object):
    """A template class for the exploit searchers"""
    _CVE_PATTERN = re.compile('CVE-\d{4}-\d{4,7}')

    def __init__(self, _cve="", _search_string="", _args=None, _limit=0):
        self.exploits = []

        self.cve = _cve
        self.search_string = _search_string
        self.args = _args
        self.limit = _limit

        self.session = Requester(self.args)

        self.log = self._setup_logger()
        self.setup()

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return '\'{}\''.format(self.__class__.__name__)

    def setup(self):
        """Called at the end of init to make initial setup easier for searchers"""
        self.log.debug('Setting up searcher: {}'.format(self.__str__()))

    def _setup_logger(self):
        log = setup_logger(self.__str__())
        # do not log if quiet exists
        if self.args and self.args.quiet:
            log.disable()
        # log as necessary if args exists
        elif self.args and not self.args.verbose:
            log.level = NOTICE
        # log everything if args does not exist, only happens in tests
        elif not self.args:
            log.level = DEBUG
        return log

    def find_exploits(self):
        """Update self.exploits after searching"""
        try:
            if self.cve:
                self.find_exploits_by_cve()
            else:
                self.find_exploits_by_string()
            self.log.debug('Found {} exploits'.format(len(self.exploits)))
        except SSLError as e:
            self.log.error('Use \'-k\' to ignore digital certificates verifications: {}'.format(e))
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

    def print_exploits(self, keywords):
        """Print the contents of self.exploits, only up to the limit of the searcher"""
        if self.limit == 0:
            for e in self.exploits:
                e.print_exploit(keywords)
        else:
            for e in self.exploits[:self.limit]:
                e.print_exploit(keywords)


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
    def print_formatted(var, name, keywords=None, end_line=False):
        str_format = "| {:" + str(Exploit.column_widths[name]) + "}"
        out = str_format.format(str(var))
        if keywords:
            out = Exploit.highlight_kw(out, keywords)
        out = out[:Exploit.column_widths[name] + 2]  # Cut the string if necessary
        if end_line:
            out += "|"
            end = "\n"
        else:
            end = ""

        print(out, end=end)

    @staticmethod
    def highlight_kw(line, keywords):
        """Wrap the given keywords with ASCII colour code in the given line

        :param line: String of message
        :param keywords: Keywords to be highlighted
        :return: Highlighted `line`
        """
        out = line
        replace_format = Fore.RED + Style.BRIGHT + '{}' + Style.RESET_ALL + Fore.RESET
        for keyword in keywords:
            regex_pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            # comment out the highlight as it messes up the table
            # out = regex_pattern.sub(replace_format.format(keyword), out)
        return out

    def print_exploit(self, keywords):
        """Prints the exploit in a standardised way"""
        date_string = datetime.strftime(self.date, "%Y-%m-%d")
        self.print_formatted(self.cve if self.cve else "N/A", "cve", keywords)
        self.print_formatted(self.desc, "desc", keywords)
        self.print_formatted(date_string, "date", keywords)
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
        try:
            widths["cve"] = max([len(e.cve) for e in exploits if e.cve])
        except ValueError:
            widths["cve"] = 0

        widths["desc"] = max([len(e.desc) for e in exploits if e.desc])

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
