#!/usr/bin/python2.7

from collections import defaultdict

import addrparse
import tests.datafile_tests as filetests

def test_parsed(parsed, dry_run=True):
    full_results = defaultdict(dict)

    [ parsed.setdefault(k,v) for k,v in parsed.items() ]

    full_results['nodupes'] = test_dupes(parsed)
    full_results['minreq'] = test_minreq(parsed)

    success, passes, fails = check_results(full_results)

    return fails

def check_results(results):
    fails = [ (k,v[1]) for k,v in results.items() if not v[0] ]
    passes = [ (k,v[1]) for k,v in results.items() if v[0] ]

    success = True
    if fails:
        success = False

    return success, passes, fails

def test_dupes(parsed):
    success = False
    dupes = dict([ (key,vals) for key,vals in parsed.items() if type(vals) == list ])

    if not dupes:
        success = True

    return success, dupes

def test_minreq(parsed):
    success = False
    req_keys = [ 'AddressNumber', 'StreetNamePreDirectional',
                 'StreetName', 'StreetNamePostType' ]

    found = [key for key in parsed.keys() if key in req_keys]
    missing = [key for key in req_keys if key not in req_keys]

    if not missing:
        success = True

    return success, missing
