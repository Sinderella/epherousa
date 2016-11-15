"""
fundamental logging methods

critical – for errors that lead to termination
error – for errors that occur, but are handled
warning – for exceptional circumstances that might not be errors
notice – for non-error messages you usually want to see
info – for messages you usually don’t want to see
debug – for debug messages

source: https://logbook.readthedocs.io/en/stable/quickstart.html
"""
import sys

from logbook import Logger, StreamHandler


def setup_logger(logger_name):
    handler = StreamHandler(sys.stdout)
    handler.format_string = '[{record.time:%H:%M:%S}] {record.level_name}: {record.channel}: {record.message}'
    handler.push_thread()
    log = Logger(logger_name)
    return log
