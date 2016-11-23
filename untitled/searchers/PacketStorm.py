# coding=utf-8
from __future__ import unicode_literals

import re
import requests
from datetime import datetime
from lxml import html

from .common import Searcher, Exploit


class PacketStorm(Searcher):
    _URL = 'https://packetstormsecurity.com{}'
    _DESCRIPTION = "Searches packetstormsecurity.com for exploits"

    def find_exploits_by_cve(self):
        # Packet storm has no way to specifically search for CVEs, so just search by string for all of them
        self.search_string = self.cve
        self.find_exploits_by_string()

    def find_exploits_by_string(self):
        results_tree = self.get_page_tree(1)

        # Check if any results were returned
        if len(results_tree.xpath("//h1[text()='No Results Found']")) != 0:
            self.log.notice("PacketStorm: No results found")
            return

        # Get the number of pages
        page_text = results_tree.xpath("//div[@id='nv']/strong[contains(text(), 'Page ')]/text()")
        if len(page_text) > 0:
            page_text = page_text[0]
        else:
            self.log.warn("PacketStorm: Error finding number of pages.")

        num_pages = re.findall("Page \d+ of (\d+)", page_text)
        if len(num_pages) > 0:
            num_pages = int(num_pages[0])
            self.log.debug('Total pages: {}'.format(num_pages))
        else:
            self.log.notice("PacketStorm: Error finding number of pages.")

        results_files = results_tree.xpath("//dl[contains(@class, 'file')]")
        for i in range(2, num_pages + 1):
            if len(results_files) < self.limit:
                results_tree = self.get_page_tree(i)
                results_files.extend(results_tree.xpath("//dl[contains(@class, 'file')]"))
            else:
                self.log.notice('Limit reached (limit: {})'.format(self.limit))
                break

        for rfile in results_files:
            tags = rfile.xpath("./dd[contains(@class, 'tags')]//a/text()")
            if "exploit" not in tags:
                continue

            # Get date
            date_string = rfile.xpath("./dd[@class='datetime']/a/text()")  # e.g. Aug 24, 2016
            if len(date_string) > 0:
                date_string = date_string[0]
            else:
                self.log.warn("PacketStorm: Failed to find date")
            date = datetime.strptime(date_string, "%b %d, %Y")

            # Get description
            desc = rfile.xpath("./dt/a[contains(@href, '/files')]/text()")
            if len(desc) > 0:
                desc = desc[0]
            else:
                self.log.warn("PacketStorm: Failed to find description.")

            # Get url
            link = rfile.xpath("./dt/a[contains(@href, '/files')]/@href")
            if len(link) > 0:
                link = link[0]
            else:
                self.log.warn("PacketStorm: Failed to find url")
            link = self._URL.format('') + link[0:link.rfind('/')]

            exploit = Exploit(self.cve)
            exploit.desc = desc
            exploit.date = date
            exploit.url = link
            self.exploits.append(exploit)

    def get_page_tree(self, page_number):
        search_url = self._URL.format('/search/files/page' + str(page_number) +
                                      '/search/?s=files&q=' + self.search_string)
        results_page = requests.get(search_url)
        self.log.info('Requesting {}'.format(search_url))
        return html.fromstring(results_page.content)
