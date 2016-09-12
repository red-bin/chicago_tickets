#!/usr/bin/python2.7

import sys, os, re
import cfg

from usaddress import parse

def parse_address(addr_string):
    parsed = dict([ (k,v) for v,k in parse(addr_string) ])

    test_failures = addrtests.test_parsed(parsed, addr_string)
    parsed = correct_failures(parsed, addr_string, test_failures)

    if test_failures:
        print '\n'.join(map(str,(addr_string, test_failures, parsed, addr_string)))

    return parsed

def correct_failures(parsed, addr_string, test_failures):
    for failkey, failvals in test_failures:
        if failkey == 'nodupes':
            parsed = correct_nodupes(parsed, failvals)

        if failkey == 'minreq':
            parsed = correct_minreq(parsed, failvals)

    return parsed

def correct_minreq(parsed, failvals):
    parsed = dict(parsed)

    for failkey in failvals:
        if failkey == 'StreetNamePostType':
            if 'StreetNamePreType' in parsed.keys():
                post_type = parsed.pop('StreetNamePreType')
                parsed['StreetNamePostType'] = post_type

    return parsed

def correct_nodupes(parsed, dupefails):
    good_dupes = ['StreetName']
    new_parsed = parsed

    for key, vals in dupefails.items():
        if key in good_dupes and type(vals) == list:
            new_val = ' '.join(vals)
            new_parsed[key] = new_val

    return new_parsed

def correct_chiaddr(line):
    line = ','.join(line)
    newline = re.sub(r'([^,])-87\.',r'\1,-87.',line)
    newline = newline.split(',')

    return newline

def parse_ticket(ticket):
    return True

def parse_tickets(unparsed):
    return [ parse_ticket(ticket) for ticket in unparsed ]
