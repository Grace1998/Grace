#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup


def get_info(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup
    except:
        print('Error')


def count_ca(info):
    ca_count = 0
    ca_repu = []
    pattern = '寄达地点：加拿大'
    guests = info('li')
    for guest in guests[1:]:
        message = guest('span', attrs={'class': 'country'})[0].string
        match = re.match(pattern, message)
        if match:
            ca_count += 1
            ca_repu.append(guest('span', attrs={'class': 'text'})[0].string)
    print(ca_count)
    return ca_repu


def get_distribution(info):
    dis_dict = {}
    guests = info('li')
    pattern = '寄达地点：([\u4e00-\u9fa5]+)'
    for guest in guests[1:]:
        message = guest('span', attrs={'class': 'country'})[0].string
        match = re.search(pattern, message)
        country = match.group(1)
        if country not in dis_dict.keys():
            dis_dict[country] = 1
        else:
            dis_dict[country] += 1
    return dis_dict


def main():
    url = r'http://www.panli.com/taobaodaigou/?utm_source=baidu&utm_medium=cpc&utm_campaign=BD_QT_pinpaici_/' \
          r'E&source=BD_QT_pinpaici_E_panli'
    info = get_info(url)
    print(count_ca(info))
    print(get_distribution(info))


if __name__ == '__main__':
    main()
