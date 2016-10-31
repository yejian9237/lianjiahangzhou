# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 21:19:59 2016

@author: Dee
"""

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['lianjia']

