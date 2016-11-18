# coding=utf-8
from __future__ import unicode_literals

from untitled.logger import setup_logger


class Searcher(object):
    """A template class for the exploit searchers"""

    def __init__(self, _cve="", _search_string="", _verbose=False, _limit=0):
        self.url = ""
        self.exploits = []
        self.description = ""

        self.cve = _cve
        self.search_string = _search_string
        self.verbose = _verbose
        self.limit = _limit
        self.log = setup_logger(self.__str__())

        self.setup()

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return '\'{}\''.format(self.__class__.__name__)

    def setup(self):
        """Called at the end of init to make initial setup easier for searchers"""
        self.log.debug('Setting up searcher: {}'.format(self.__str__()))

    def findExploits(self):
        """Update self.exploits after searching"""
        if self.cve != "":
            self.findExploitsByCVE()
        else:
            self.findExploitsByString()
        self.log.debug('Found {} exploits'.format(len(self.exploits)))

    def findExploitsByCVE(self):
        """Searches the database using self.cve"""
        pass

    def findExploitsByString(self):
        """Searches the database using self.search string"""

    def printExploits(self):
        """Print the contents of self.exploits, only up to the limit of the searcher"""
        if self.limit == 0:
            for e in self.exploits:
                e.print_exploit()
        else:
            for e in self.exploits[:self.limit]:
                e.print_exploit()
