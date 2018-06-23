#!/usr/bin/env python2
# coding=utf-8

import argparse
import os
import sys

parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)

from vendor.inwx import domrobot, getOTP
from vendor.tldextract import TLDExtract


class AcmeInwxException(Exception):
    pass


ACME_PREFIX = '_acme-challenge.'


class AcmeDomain(object):
    def __init__(self, text):
        if text.startswith(ACME_PREFIX):
            text = text[len(ACME_PREFIX):]

        no_cache_extract = TLDExtract(cache_file=False)
        result = no_cache_extract(text)

        self.fqdn = result.fqdn
        self.domain = result.registered_domain
        self.subdomain = result.subdomain


class Inwx(object):
    def __init__(self, domain, subdomain=None):
        self.url = "https://api.domrobot.com/xmlrpc/"
        self.inwx = domrobot(self.url)
        self.domain = domain
        self.subdomain = subdomain

        self.acme_record_name = '_acme-challenge{subdomain}'.format(
            subdomain='.' + subdomain if subdomain is not None else '')
        self.acme_record_type = 'TXT'

    def login(self, user, password, tfa):
        res = self.inwx.account.login({'user': user, 'pass': password})

        # Perform OTP login if enabled
        if 'tfa' in res['resData'] and res['resData']['tfa'] == 'GOOGLE-AUTH':
            self.inwx.account.unlock({'tan': getOTP(tfa)})

    def has_acme_challange(self):
        res = self.inwx.nameserver.info({
            'domain': self.domain,
            'name': self.acme_record_name,
            'type': self.acme_record_type,
        })

        return 'record' in res['resData']

    def get_record_id(self):
        res = self.inwx.nameserver.info({
            'domain': self.domain,
            'type': self.acme_record_type,
            'name': self.acme_record_name
        })

        resData = res['resData']
        if 'count' in resData and resData['count'] == 1:
            return resData['record'][0]['id']

        return None

    def add_acme_challenge(self, challenge):
        acme_record_id = self.get_record_id()

        if acme_record_id is not None:
            print("Record already exists.")
            return

        self.inwx.nameserver.createRecord({
            'domain': self.domain,
            'type': self.acme_record_type,
            'name': self.acme_record_name,
            'content': challenge,
            'ttl': 300
        })

    def remove_acme_challenge(self):
        acme_record_id = self.get_record_id()
        if id is not None:
            self.inwx.nameserver.deleteRecord({
                'id': acme_record_id,
            })
        else:
            pass  # Had no acme challenge record in the first place


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DNS-01 ACME implementation for INWX using acme.sh')
    add_or_remove_group = parser.add_mutually_exclusive_group(required=True)
    add_or_remove_group.add_argument('--add', action='store_true', help='Adds the ACME txt record.')
    add_or_remove_group.add_argument('--remove', action='store_true', help='Removes the ACME txt record.')
    parser.add_argument('--acme-record-name', help='The ACME txt record name.')
    parser.add_argument('--challenge', default=None, help='The ACME challange code. Required if --add is specified.')
    args = parser.parse_args()

    if args.add and args.challenge is None:
        parser.error('--add requires --challenge')
        exit(1)

    dom = AcmeDomain(args.acme_record_name)

    try:
        try:
            print('Trying configuration for %s' % dom.domain)
            exec 'from config.%s import INWX_USER, INWX_PASS, INWX_OTP_SECRET' % dom.domain.replace('.', '_')
            print('Found configuration for %s' % dom.domain)
        except ImportError:
            print('Trying default configuration')
            from config._ import INWX_USER, INWX_PASS, INWX_OTP_SECRET
            print('Found default configuration')
    except ImportError:
        print("Make sure to create a configuration file first (check README.md).")
        exit(1)

    inwx_client = Inwx(dom.domain, dom.subdomain)
    inwx_client.login(INWX_USER, INWX_PASS, INWX_OTP_SECRET)

    if args.add:
        inwx_client.add_acme_challenge(args.challenge)
    else:
        inwx_client.remove_acme_challenge()
