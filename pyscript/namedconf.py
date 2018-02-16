#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
import sys
import os


defaultdns = "45.76.190.236"
defaultimage = "45.76.190.236"

content = '''$TTL 7200

{domain}. IN SOA {domain}. {domain}.gmail.com (222 1H 15M 1W 1D)

{domain}. IN NS dns1.{domain}.

dns1.{domain}. IN A {dns}

'''


def generate(domain):
    template = '{domain}. IN A {website}\n\n'.format(domain=domain, website=defaultimage)
    return template


def main():
    file = sys.argv[1]
    if not os.path.exists(file):
        print "File not exists"
        sys.exit()

    domains = []
    with open(file) as f:
        for domain in f.readlines():
            domains.append(domain.replace('\n', ''))

    for domain in domains:
        routedomain = domain.split(',')[0]
        dcontent = content.format(domain=routedomain, dns=defaultdns)
        if domain.find(',') > 0:

            for d in domain.split(','):
                dcontent += generate(d)

        savefile = routedomain + '.zone'
        with open(savefile, 'wb') as f:
            f.write(dcontent)

        print "{domain} is ok".format(domain=routedomain)


if __name__ == '__main__':
    main()