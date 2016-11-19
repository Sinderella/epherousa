#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import argparse
import re
import threading

from logbook import NOTICE, DEBUG

from .logger import setup_logger
from .models.exploit import Exploit
from .searchers import *


def parse_args():
    # Deal with argument parsing
    # maybe add these to an init class one day
    arg_parser = argparse.ArgumentParser(
        description="Search mutltiple sources for exploits for CVEs or software versions")
    arg_parser.add_argument("cve", help="The cve to find exploits for.")
    arg_parser.add_argument("-d", "--disable",
                            help="Disable only these scanners. Input is interpreted as a series of comma-seperated "
                                 "case-insensitive regexes.")
    arg_parser.add_argument("-e", "--enable",
                            help="Enable only these scanners. Input is interpreted as a series of comma-seperated "
                                 "case-insensitive regexes.")
    arg_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
    arg_parser.add_argument("-p", "--phrase", action="store_true",
                            help="Force interpreting the search argument as a search string rather than a CVE")
    arg_parser.add_argument("-l", "--limit", type=int, default=5,
                            help="Limit the results of the exploits returned for each Scanner. Default value is set to "
                                 "0 for no limit.")

    return arg_parser.parse_args()


def filter_class_list(class_list, regex_list):
    """Takes a list of classes and a list of regexes, and returns a list of all the classes that have a matching name"""

    class_names = [c.__name__ for c in class_list]
    filtered_names = []
    for name in class_names:
        matches = [re.search(r, name, re.IGNORECASE) for r in regex_list]
        matches = [x for x in matches if x is not None]  # re returns a none object for no matches, so remove these
        if len(matches) > 0:  # i.e. no matching regex
            filtered_names.append(name)

    return [c for c in class_list if c.__name__ in filtered_names]


def main():
    args = parse_args()
    log = setup_logger('searchsploit')
    log.level = DEBUG if args.verbose else NOTICE
    log.debug("Arguments: {}".format(args))

    # Construct the list of searchers to use
    searcher_classes = [ExploitDB, PacketStorm, SecurityFocus, ZeroDayToday]  # Keep alphabetical to make life easier

    if args.enable:
        enable_regexes = args.enable.split(',')
        searcher_classes = filter_class_list(searcher_classes, enable_regexes)

    if args.disable:
        disable_regexes = args.disable.split(',')
        disabled_classes = filter_class_list(searcher_classes, disable_regexes)
        searcher_classes = [c for c in searcher_classes if c not in disabled_classes]

    # Actually do the searching
    log.info("Using searchers: " + str([s.__name__ for s in searcher_classes]))

    # We should also consider searching in multiple ways in the future! But it will be easy to add up later on
    if args.phrase or not re.match("CVE", args.cve, re.IGNORECASE):
        phrase = args.cve
        cve = ""
    else:
        cve = args.cve
        phrase = ""

    # Actually create the searchers
    limit = args.limit if args.limit else 0
    log.debug("Setting limit to {}".format(limit))
    searcher_list = [searcher_class(_cve=cve, _search_string=phrase, _verbose=args.verbose, _limit=limit) for
                     searcher_class
                     in searcher_classes]
    log.info("Setting {} searchers {}".format(len(searcher_list), searcher_list))

    threads = []
    for s in searcher_list:
        new_thread = threading.Thread(target=s.findExploits)
        new_thread.start()
        threads.append(new_thread)
        log.notice("Spawned a thread for searching at {}".format(s))

    # wait for each thread until all done
    [thread.join() for thread in threads]

    Exploit.calculateWidths(searcher_list)
    Exploit.printHeader()
    for s in searcher_list:
        s.printExploits()

    Exploit.printFooter()
