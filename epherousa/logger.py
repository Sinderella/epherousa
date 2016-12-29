# coding=utf-8
"""
fundamental logging methods

critical – for errors that lead to termination
error - for errors that occur, but are handled
warning – for exceptional circumstances that might not be errors
notice – for non-error messages you usually want to see
info – for messages you usually don’t want to see
debug – for debug messages

source: https://logbook.readthedocs.io/en/stable/quickstart.html
"""
import colorama
import sys
from colorama import Fore, Style

from logbook import Logger, StreamHandler, CRITICAL, ERROR, WARNING, INFO
from logbook import NOTICE
from logbook.more import ColorizingStreamHandlerMixin


class ColourisingMixin(ColorizingStreamHandlerMixin):
    def get_color(self, record):
        """Returns the color for this record."""
        if record.level == CRITICAL:
            return Fore.RED + Style.DIM
        elif record.level == ERROR:
            return Fore.RED + Style.BRIGHT
        elif record.level == WARNING:
            return Fore.YELLOW + Style.BRIGHT
        elif record.level == NOTICE:
            return Fore.CYAN + Style.BRIGHT
        elif record.level == INFO:
            return Fore.WHITE + Style.BRIGHT
        return Fore.WHITE

    def format(self, record):
        rv = super(ColorizingStreamHandlerMixin, self).format(record)
        if self.should_colorize(record):
            colour = self.get_color(record)
            if colour:
                rv = colour + rv + Style.RESET_ALL
        return rv


class ColourHandler(ColourisingMixin, StreamHandler):
    def __init__(self, *args, **kwargs):
        super(ColourHandler, self).__init__(*args, **kwargs)
        colorama.init(autoreset=True)


def setup_logger(logger_name):
    handler = ColourHandler(sys.stdout)
    handler.format_string = '[{record.time:%H:%M:%S}] {record.level_name}: {record.channel}: {record.message}'
    handler.push_thread()
    log = Logger(logger_name)
    return log
