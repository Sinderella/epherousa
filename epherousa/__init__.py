#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import argparse
import re
import signal
import sys
import threading
from builtins import input

from logbook import NOTICE, DEBUG

from .logger import setup_logger
from .searchers import ExploitDB, PacketStorm, SecurityFocus, ZeroDayToday
from .searchers.common import Exploit
from .version import __version__


def parse_args():
    # Deal with argument parsing
    # maybe add these to an init class one day
    arg_parser = argparse.ArgumentParser(
        description="Search multiple sources for exploits for CVEs or software versions")
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
    arg_parser.add_argument("-l", "--limit", type=int, default=10,
                            help="Limit the results of the exploits returned for each Scanner. Default value is set to"
                                 " 0 for no limit.")
    arg_parser.add_argument("-q", "--quiet", action="store_true",
                            help="Do not display ephe's banner.")
    arg_parser.add_argument("-px", "--proxy", help="Proxy for ephe, used in every requests.")
    arg_parser.add_argument("-k", "--insecure", action="store_true", help="Ignore SSL certificates in requests.")

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


def print_banner():
        """Prints ephe's banner on startup"""
        print("""
                         .-""-.
                        (___/\ \\
                       ( |' ' ) )   """
              + "\tEphe v" + __version__ +
              """
                     __) _\=_/  (
                ____(__._ `  \   )
              .(/8-.._.88,   ; (
             /   /8.    `88., |  )
  _.`'---.._/   /.8_ ____.'_| |_/
'-'``'-._     /  | `-........'
        `;-"`;  |"""
        + 6*"\t" + "Dionach Ltd" + """
          `'.__/""")


def process_signal_exit(signum, stack):
    choice = input('\nexit? [y/N]')
    try:
        if choice.lower().startswith('y'):
            sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)


def main():
    signal.signal(signal.SIGINT, process_signal_exit)
    args = parse_args()
    log = setup_logger('ephe')
    log.level = DEBUG if args.verbose else NOTICE

    # print banner
    if not args.quiet:
        print_banner()
    else:
        log.disable()

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
        cve = None
    else:
        cve = args.cve
        phrase = None

    # Actually create the searchers
    limit = args.limit if args.limit else 0
    log.debug("Setting limit to {}".format(limit))
    searcher_list = [searcher_class(_cve=cve, _search_string=phrase, _args=args, _limit=limit) for
                     searcher_class
                     in searcher_classes]
    log.info("Setting {} searchers {}".format(len(searcher_list), searcher_list))

    threads = []
    for s in searcher_list:
        new_thread = threading.Thread(target=s.find_exploits)
        # threads will exit if main thread exits
        new_thread.daemon = True
        new_thread.start()
        threads.append(new_thread)
        log.notice("Spawned a thread for searching at {}".format(s))

    # wait for each thread until all done
    [thread.join() for thread in threads]

    Exploit.calculate_widths(searcher_list)
    Exploit.print_header()
    for s in searcher_list:
        s.print_exploits(cve) if cve else s.print_exploits(phrase.split(' '))

    Exploit.print_footer()
