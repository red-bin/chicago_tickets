#!/usr/bin/python2.7

import sys, os, re
from tests import addrtests
import cfg

from pprint import pprint
from usaddress import parse

#def second_parse(usaddr_parsed, addr_str, chicago_addrs):

def parse_address(addr_string):
    ret_fails = []
    parsed_list = [ (k,v) for v,k in parse(addr_string) ]

    street_name = combine_streetnames(parsed_list)

    parsed = dict(parsed_list)
    parsed['StreetName'] = street_name
    parsed = clean_parsed(parsed)

    test_failures = addrtests.test_parsed(parsed, addr_string)
    fails = True if [ val for val in test_failures.values() if val ] else False

    if fails:
        parsed = correct_failures(parsed, test_failures)
        test_failures = addrtests.test_parsed(parsed, addr_string)
        fails = True if [ val for val in test_failures.values() if val ] else False

    if fails:
        if len(test_failures['missing']) == 1 and test_failures['missing'][0] == 'StreetNamePostType':
            pass
        else:
            ret_fails = test_failures

    #TODO - split tests into something that understands addr grammar

    return parsed, ret_fails

def clean_parsed(parsed):
    if 'PlaceName' in parsed.keys():
        if parsed['PlaceName'] == "CHICAGO":
            parsed.pop('PlaceName')

    return parsed

def combine_streetnames(parsed_list):
    street_names = [ val for key,val in parsed_list if key == 'StreetName' ] 
    if len(street_names) > 1:
        street_names = ' '.join(street_names)

    return street_names


def correct_failures(parsed, test_failures):
    missing = test_failures['missing']
    nodupes = test_failures['nodupes']
    forbidden = test_failures['forbidden']

    if forbidden:
        if 'PlaceName' in forbidden:
            if len(missing) == 1 and len(forbidden) == 1:
                parsed[missing[0]] = parsed.pop(forbidden[0])
                missing = []

    if nodupes:
        parsed = correct_nodupes(parsed, nodupes)

    if missing:
        parsed = correct_missing(parsed, missing)

    return parsed

def correct_missing(parsed, failvals):
    parsed = dict(parsed)
    keys =  parsed.keys()

    try:
        street_name = parsed['StreetName']
    except:
        street_name = None

    try:
        street_type = parsed['StreetNamePostType']
    except:
        street_type = None

    try:
        street_num = parsed['AddressNumber']
    except:
        street_num = None

    try:
        street_dir = parsed['StreetNamePreDirectional']
    except:
        street_dir = None

    if 'StreetName' in failvals:
        return parsed

    if 'StreetNamePostType' in failvals:
        if street_type:
            parsed.pop('StreetNamePreType')
            parsed['StreetNamePostType'] = street_type

    elif 'StreetNamePostType' in failvals:
        if len(streetname) == 1 and int(street_num) >= 9500:
            if 'StreetNamePreType' in keys:
                if street_type in ['AVENUE', 'AVE']:
                    parsed.pop('StreetNamePreType')
                    parsed['StreetName'] = street_type

    elif 'StreetNamePreDirectional' in failvals:
        street_name_len = len(street_name)
        if street_name_len == 1 and int(street_num) >= 9500:
            if 'StreetNamePostDirectional' in keys:
                if 'StreetNamePostType' in keys:
                    if street_type in ['AVENUE', 'AVE']:
                        parsed.pop('StreetNamePostDirectional')
                        parsed['StreetName'] = street_dir
                        parsed['StreetNamePreDirectional'] = 'S'

        if street_name_len == 1:
            if 'OccupancyIdentifier' in keys:
                occupancy_id = parsed.pop('OccupancyIdentifier')
                old_type = parsed.pop('StreetNamePostType')

                new_streetname = "%s %s" % (occupancy_id, old_type)
                new_dir = street_name

                parsed['StreetNamePreDirectional'] = new_dir
                parsed['StreetName'] = new_streetname

            else:
                if 'StreetNamePostType' in keys:
                    new_streetname = street_type
                    new_dir = street_name

                    parsed['StreetName'] = new_streetname
                    parsed['StreetNamePreDirectional'] = new_dir

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
