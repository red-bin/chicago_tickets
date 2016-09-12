#!/usr/bin/python2.7

"""
Tickets

Usage:
  tickets.py [--chiaddrs=<n> | --tickets=<n>]

Options:
    -t --tickets=<n>   Tickets count [default: 1].
    -a --chiaddrs=<n>  Addrs count [default: 2000].
    -r --random        Select at random
    -T --tests         Run tests
"""

from docopt import docopt

import cfg
import fetchers
import addrparse
from tests import addrtests, datafile_tests

if __name__ == '__main__':
    d_args = docopt(__doc__)
    chi_addrcount =  int(d_args['--chiaddrs'])
    ticket_count = int(d_args['--tickets'])

    unparsed_addrs = fetchers.chiaddrs(chi_addrcount)
    unparsed_tktlines = fetchers.raw_tickets(ticket_count)

    for is_pass,line in unparsed_tktlines:
        if not is_pass:
            print line
        

    #print addrparse.parse_tickets(unparsed_tktlines)
