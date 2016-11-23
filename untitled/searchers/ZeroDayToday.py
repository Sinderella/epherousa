# coding=utf-8
from __future__ import unicode_literals

import requests
from datetime import datetime
from lxml import html

from .common import Searcher, Exploit


class ZeroDayToday(Searcher):
    def setup(self):
        super(ZeroDayToday, self).setup()
        self.name = "0day.today"
        self.url = "http://0day.today/"
        self.description = "Searches 0day.today"

    def findExploitsByCVE(self):
        # It looks like a lot of stuff on 0day.today might not be tagged properly with CVEs
        # For now using this method, though may just use normal text search in the future

        search_url = "http://0day.today/search?search_request=&search_type=1&search_in_text=on&category=-1" \
                     "&platform=-1&price_from=0&price_to=-1&author_login=&cve=" + self.cve
        self.findExploitsFromURL(search_url)

    def findExploitsByString(self):
        search_url = "http://0day.today/search?search_request=" + self.search_string
        self.findExploitsFromURL(search_url)

    def findExploitsFromURL(self, search_url):
        self.log.info('Requesting {}'.format(search_url))
        search_page = requests.post(search_url, data={"agree": "Yes%2C+I+agree"}, allow_redirects=True,
                                    headers={"Referer": search_url})
        search_tree = html.fromstring(search_page.content)

        exploit_rows = search_tree.xpath("//div[@class='ExploitTableContent']")
        for row in exploit_rows:
            if len(self.exploits) >= self.limit:
                self.log.notice('Limit reached (limit: {})'.format(self.limit))
                break

            # Get date
            date_string = row.xpath("./div/a[starts-with(@href, '/date')]/text()")
            if len(date_string) > 0:
                date = datetime.strptime(date_string[0], "%d-%m-%Y")
            else:
                self.log.warn("0day.today: Failed to find date.")
                continue

            # Get description and the url
            desc_box = row.xpath("./div//a[starts-with(@href, '/exploit/description')]")
            if len(desc_box) > 0:
                desc_box = desc_box[0]
                desc = desc_box.xpath("./text()")
                if len(desc) > 0:
                    desc = desc[0]
                else:
                    self.log.warn("0day.today: Failed to find description.")
                    continue

                link = desc_box.xpath("./@href")
                if len(link) > 0:
                    link = self.url.rstrip("/") + link[0]
                else:
                    self.log.warn("0day.today: Failed to find URL")
                    continue
            else:
                self.log.warn("0day.today: Failed to find description box")
                continue

            # Get the cost
            cost = row.xpath("./div[10]/text()")
            if len(cost) > 0:
                cost = cost[0]
                if cost.startswith("free"):
                    cost = "0"
                else:
                    cost = row.xpath(".//div[@class='GoldText']/text()")
                    if len(cost) == 0:
                        self.log.warn("0day.today: Failed to find cost.")
                        continue

                    cost = cost[0].replace(" ", "")
            else:
                self.log.warn("0day.today: Failed to find cost.")
                continue

            # And add
            e = Exploit(self.cve)
            e.desc = desc
            e.date = date
            e.url = link
            e.cost = cost
            self.exploits.append(e)
