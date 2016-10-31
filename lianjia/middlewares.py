# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 23:48:03 2016

@author: Dee
"""


import random
import json
from lianjia.settings import PROXIES

class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        #print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class ProxyMiddleware(object):
    def __init__(self):
        with open(PROXIES, 'r') as f:
            self.dict_list = json.load(f)
    def process_request(self, request, spider):
        proxy = random.choice(self.dict_list)
        try:
            request.meta['proxy'] = proxy['http']
        except:
            request.meta['proxy'] = "http://127.0.0.1:1080"
