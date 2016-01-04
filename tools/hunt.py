#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import sys

from multicpu import multi_cpu


def read_file(input_file):
    with open(input_file) as f:
        domain_list = f.readlines()
    result = []
    for domain in domain_list:
        domain = domain.strip('\n').strip('\/')
        if (not domain.startswith('http://') and
                not domain.startswith('https://')):
            domain = 'http://' + domain
        result.append(domain)
    return result


def hunt(domain):
    url = domain + '/crossdomain.xml'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',  # nopep8
    }
    result = {'domain': domain}
    try:
        res = requests.get(url, headers=headers, allow_redirects=False)
        if res.status_code / 100 == 2:
            result['crossdomain'] = res.text
        if 'domain="*"' in result['crossdomain']:
            result['crossdomain_allow_any'] = True
    except:
        pass

    url = domain + '/.git/config'
    try:
        res = requests.get(url, headers=headers, allow_redirects=False)
        result['git_hack'] = (res.status_code / 100 == 2)
    except:
        pass

    return result


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='The input file consists of domains.')
    parser.add_argument('-c', '--cpu_num', type=int)
    parser.add_argument('-t', '--thread_num', type=int)
    args = vars(parser.parse_args(argv))
    input_file = args['input']
    domain_list = read_file(input_file)
    cpu_num = 2 if args['cpu_num'] is None else args['cpu_num']
    thread_num = 4 if args['thread_num'] is None else args['thread_num']
    result = multi_cpu(hunt, domain_list, cpu_num, thread_num)
    # TODO: output the result


if __name__ == '__main__':
    main(sys.argv[1:])
