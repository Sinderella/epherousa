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
import sys

from logbook import Logger, StreamHandler, CRITICAL, ERROR, WARNING, INFO
from logbook.more import ColorizingStreamHandlerMixin


class ColourizingMixin(ColorizingStreamHandlerMixin):
    def get_color(self, record):
        """Returns the color for this record."""
        if record.level == CRITICAL:
            return 'darkred'
        elif record.level == ERROR:
            return 'red'
        elif record.level == WARNING:
            return 'yellow'
        elif record.level >= INFO:
            return 'lightgray'
        return 'lightgray'


class ColourHandler(ColourizingMixin, StreamHandler):
    def __init__(self, *args, **kwargs):
        super(ColourHandler, self).__init__(*args, **kwargs)

        try:
            import colorama
        except ImportError:
            pass
        else:
            colorama.init()


def setup_logger(logger_name):
    handler = ColourHandler(sys.stdout)
    handler.format_string = '[{record.time:%H:%M:%S}] {record.level_name}: {record.channel}: {record.message}'
    handler.push_thread()
    log = Logger(logger_name)
    return log
