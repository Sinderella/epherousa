# coding=utf-8
from __future__ import unicode_literals

from requests import Session
from requests.adapters import HTTPAdapter

from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class Requester(Session):
    """Every request should be only made by this class"""
    _USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'}
    _MAX_RETRIES = 3

    def __init__(self, args=None):
        """Construct the `Requester` object based on given arguments

        :param args: application arguments for settings
        """
        super(Requester, self).__init__()

        self.args = args
        try:
            self.proxies = {
                'http': self.args.proxy,
                'https': self.args.proxy
            }
            self.verify_ssl = not self.args.ignore_ssl
        except AttributeError:
            self.proxies = None
            self.verify_ssl = True

        self.headers.update(Requester._USER_AGENT)

        self.mount('http://', HTTPAdapter(max_retries=Requester._MAX_RETRIES))
        self.mount('https://', HTTPAdapter(max_retries=Requester._MAX_RETRIES))

        disable_warnings(InsecureRequestWarning)

    def get(self, url, **kwargs):
        """Issue GET HTTP request to the URL

        :param url: URL to request
        :param kwargs: Other parameters to be sent to `requests.Session().get()`
        :return:
        """
        return super(Requester, self).get(url, proxies=self.proxies, verify=self.verify_ssl, **kwargs)

    def head(self, url, **kwargs):
        """Issue HEAD HTTP request to the URL

        :param url: URL to request
        :param kwargs: Other parameters to be sent to `requests.Session().get()`
        :return:
        """
        return super(Requester, self).head(url, proxies=self.proxies, verify=self.verify_ssl, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """Issue POST HTTP request to the URL

        :param url: URL to request
        :param kwargs: Other parameters to be sent to `requests.Session().get()`
        :return:
        """
        return super(Requester, self).post(url, data, json, proxies=self.proxies, verify=self.verify_ssl, **kwargs)
