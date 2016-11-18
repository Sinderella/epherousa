from __future__ import unicode_literals, print_function

from datetime import datetime


class Exploit:
    """A class to hold all of the information about a particular exploit"""

    # Initially this defines the min width for each column (see calculateWidths)
    column_widths = {"cve": 14, "desc": 12, "cost": 5, "date": 11, "url": 4}

    def __init__(self, _cve="", _date=None, _desc="", _cost=0, _url=""):
        self.cve = _cve
        self.desc = _desc
        self.cost = _cost
        self.date = _date
        self.url = _url

    @staticmethod
    def printFormatted(var, name, end_line=False):
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
        self.printFormatted(self.cve, "cve")
        self.printFormatted(self.desc, "desc")
        self.printFormatted(date_string, "date")
        self.printFormatted(self.cost, "cost")
        self.printFormatted(self.url, "url", end_line=True)

    @staticmethod
    def getTotalWidth():
        total_width = 1  # Account for the final bar that is printed
        for key in Exploit.column_widths:
            total_width += Exploit.column_widths[key] + 2  # +2 to account for the "| "
        return total_width

    @staticmethod
    def calculateWidths(searchers):
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
        widths["cost"] = max([len(str(e.cost)) for e in exploits])
        widths["url"] = max([len(e.url) for e in exploits])

        for key in widths:
            Exploit.column_widths[key] = max(Exploit.column_widths[key], widths[key])

    @staticmethod
    def printHeader():
        """Print the table header for the exploit table"""
        total_width = Exploit.getTotalWidth()
        print("_" * total_width)

        Exploit.printFormatted("CVE", "cve")
        Exploit.printFormatted("Description", "desc")
        Exploit.printFormatted("Date", "date")
        Exploit.printFormatted("Cost", "cost")
        Exploit.printFormatted("URL", "url", end_line=True)

        print("_" * total_width)

    @staticmethod
    def printFooter():
        total_width = Exploit.getTotalWidth()
        print("_" * total_width)
