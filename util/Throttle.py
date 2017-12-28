# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   Project Name :    Chatting
   File Name :       Throttle
   Version :         1.0
   Author :          Angel
   Date :            2017/10/7
-------------------------------------------------
   Description :      下载限速
-------------------------------------------------
"""
__author__ = 'Angel'
import time
import datetime
from requests.utils import urlparse


class Throttle:
    """
    在下同一域名时增加下载延迟
    """

    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urlparse(url)
        last_acessed = self.domains.get(domain)

        if self.delay > 0 and last_acessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_acessed).seconds
            if sleep_secs > 0:
                # 该domain刚访问过，因此需要休眠
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.datetime.now()
