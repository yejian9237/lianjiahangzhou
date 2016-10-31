# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 21:15:26 2016

@author: Dee
"""

import random
import json
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import queue
from threading import Thread
from time import sleep


check_url = 'http://hz.lianjia.com/'
check_str = '1010 9666'

ok_proxy = []

SHARE_Q = queue.Queue()

thread_num = 5

def worker() :
    global SHARE_Q
    while not SHARE_Q.empty():
        item = SHARE_Q.get() #获得任务
        check_one_proxy(item)
        sleep(0.2)


class MyThread(Thread) :
    def __init__(self, func) :
        super(MyThread, self).__init__()
        self.func = func

    def run(self) :
        self.func()

def check_one_proxy(proxy):
    proxy['type'] = str.lower(proxy['type'])
    proxies = {proxy['type']:proxy['type'] + '://' + proxy['ip'] + ':' + proxy['port']}
    print(proxies)
    if proxy['type'] == 'http':
        try:
            r = requests.get(check_url, headers=headers, proxies=proxies, timeout=5)
            r.encoding = 'utf-8'
            if check_str in r.text:
                ok_proxy.append(proxies)
                print(proxy['ip'],'OK')
        except:
            pass
            print(proxy['ip'],'FAILED')

def check_proxy():
    proxy_l = proxy_list()
    for p in proxy_l:
        SHARE_Q.put(p)
    threads=[]    
    for index in range(thread_num):
        t = MyThread(worker)
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    
    with open('ok_proxy.json', 'w') as f:
        json.dump(ok_proxy, f)





def proxy_list(file='proxy.json'):
    with open(file, 'r') as f:
        dict_list = json.load(f)

    return dict_list


def random_choice_proxy(p_list):
    index = random.randint(0, len(p_list)-1)
    return p_list[index]


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0'
}

proxies = {'http': 'http://127.0.0.1:1080'}


def get_soup(url):
    r = requests.get(url, headers=headers, proxies=proxies)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def get_all_url():
    url = 'http://proxylist.hidemyass.com/{}'
    soup = get_soup(url.format(1))
    lis = soup.find('ul', {'class': "pagination ng-scope"}).find_all('li')
    lis = [i.get_text() for i in lis]
    m = int(max(lis))
    url_list = []
    for i in range(1, m+1):
        u = url.format(i)
        url_list.append(u)
    return url_list


def get_all_table(url_list):
    proxy_list = []
    for url in url_list:
        print(url)
        soup = get_soup(url)
        table = soup.find('table')
        trs = table.find_all('tr')
        for tr in trs[1:]:
            a_proxy = clean_a_proxy(tr)
            proxy_list.append(a_proxy)
    with open('proxy.json', 'w') as f:
        json.dump(proxy_list, f)


def clean_a_proxy(tr):
    proxy_dict = {}
    proxy_dict.setdefault('ip', None)
    proxy_dict.setdefault('port', None)
    proxy_dict.setdefault('type', None)
    proxy_dict.setdefault('area', None)
    proxy_dict.setdefault('anon', None)
    tds = tr.find_all('td')
    # ip
    ip_s = tds[1]
    style = ip_s.find('style')
    s = style.get_text()
    b = str(ip_s)
    key = re.findall('(?<=.)\S+(?={)', s)
    values = re.findall(r'(?<={)\S+(?=})', s)
    s_dict = dict(zip(key, values))
    for k, v in s_dict.items():
        b = b.replace(k, v)
    c = re.findall('(?<!display:none")>"*\d+|(?<=\.)\d+', b)
    if len(c) != 4:
        print(b)
    c = [i.replace('>', '') for i in c]
    print(tr['rel'])
    print(c)
    proxy_dict['ip'] = '.'.join(c)
    # port
    proxy_dict['port'] = tds[2].get_text(strip=True)
    # area
    proxy_dict['area'] = tds[3].span.get_text(strip=True)
    # type
    proxy_dict['type'] = tds[6].get_text(strip=True)
    # anon
    proxy_dict['anon'] = tds[7].get_text(strip=True)
    return proxy_dict
