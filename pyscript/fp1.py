#!/usr/bin/env python
# encoding: utf-8

import argparse
import pcre
import copy
from pprint import pprint
from glob import glob
from os import path


REGEX = r"HTTP\x2f1\.1\x20200\x20OK\r\nServer\x3a\x20WebServer\(IPCamera\x5fLogo\)\r\n"
RESULT = {
    'uuid': '8040799c7798458486c4b61d36a6ef80',
    'author': {
        'name': 'yangy',
        'mail': 'yangy4@knownsec.com',
        'zoomeye_id': 'vayneyang',
        'date': '2015-10-26',
    },
    'rule': {
        'pattern': {
            'regex': REGEX,
            'flags': ['s'],   # 'i' => case-insensitive , 's' => DOTALL
        },
        'service': 'http',
        'portinfo': {
            'product': 'WebServer(IPCamera_Logo) httpd',
            'version': '',
            'info': '',
            'hostname': '',
            'ostype': '',
            'devicetype': 'webcam',
            'cpe': [],
        },
        'probe': 'GetRequest',
        'protocol': 'TCP',
        'next': '',
    },
    'knowledge': {
        'type': 'hardware',   # 取值 hardware/software/unknown
        'company': '',   # hardware
        'brand': '',   # hardware
        'model': '',   # hardware
        'devicetype': ['网络摄像机'],   # hardware
        'name': '',   # software
        'extra_devicetype': [],   # software
    },
    'tags': [],
    'references': [''],
}


def extract(fingerprint):
    pattern_compiled = pcre.compile(REGEX, flags=parse_compile_flags(RESULT['rule']['pattern']['flags']))
    matched = pcre.match(pattern_compiled, fingerprint)
    if not matched:
        return None
    result = copy.deepcopy(RESULT)
    result['rule']['portinfo'] = substitute_portinfo_template(result['rule']['portinfo'], matched.groups())
    return result


def parse_compile_flags(flags):
    if flags == ['i']:
        return pcre.IGNORECASE
    elif flags == ['s']:
        return pcre.DOTALL
    elif flags == ['i', 's'] or flags == ['s', 'i']:
        return pcre.IGNORECASE | pcre.DOTALL


def substitute_portinfo_template(portinfo_dict, matched_results):
    def substitute_template(value, matched_result):
        pattern_compiled = pcre.compile('\$([\d]{1,2})')
        for index in pattern_compiled.findall(value):
            group_value = matched_result[int(index)-1] if index else ''
            value = value.replace('$'+index, '' if not group_value else group_value)
        return value
    return dict((k, substitute_template(str(v), matched_results)) for k, v in portinfo_dict.iteritems())


def get_groups_details_of_results(raw_results, matched_results):
    pattern_compiled = pcre.compile('\$([\d]{1,2})')
    group_list = []
    for  key, value in raw_results['rule']['portinfo'].iteritems():
        if pattern_compiled.search(str(value)):
            group_list.append([key, value, matched_results['rule']['portinfo'][key]])
    return group_list


def main():
    parser = argparse.ArgumentParser(description='{}'.format(__file__))

    parser.add_argument(
        '-f', '--fingerprint',
        dest='fingerprint',
        default='',
        help='specified sample file'
        )
    args = parser.parse_args()

    if args.fingerprint:
        with open(args.fingerprint) as f:
            pprint(extract(f.read()))
    else:
        results = []
        for fp_path in glob(path.join(path.dirname(path.realpath(__file__)), '*.fp')):
            with open(fp_path) as f:
                print '\n{}'.format(fp_path)
                result = extract(f.read())
                pprint(result)
                results.append([fp_path, 'OK' if result else 'No Result', get_groups_details_of_results(RESULT, result)])

        print '\nMatch Result:'
        for result in results:
            print result


if __name__ == '__main__':
    main()

