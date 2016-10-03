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
    -p --populate      Populate Chicago Addresses Table
"""

from docopt import docopt
from mysql import connector

import cfg
import fetchers
#import pushers
import addrparse
import sys
from pprint import pprint
from tests import addrtests
from datetime import datetime

db = connector.connect(host='hostname' user='username', passwd='password', database='tickets')
c = db.cursor()
stmt = "INSERT INTO tickets (ticket_number,violation_code,address_num, street_dir, street_name, street_type, time,weekday,ticket_queue,unit,badge,license_type,license_state,license_number,car_make,hearing_dispo,raw_location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

#if __name__ == '__main__':
if 1 == 1:
    d_args = docopt(__doc__)
    chi_addrcount =  int(d_args['--chiaddrs'])
    ticket_count = int(d_args['--tickets'])

    chicago_addrs = []

    #if d_args['--populate']:
    #    unparsed_chiaddrs = fetchers.chiaddrs(chi_addrcount)
    #    populate_chicago_table(unparsed_chiaddrs)

    unparsed_tktlines = fetchers.raw_tickets(ticket_count)

    for_sql = []

    count = 0
    for line in unparsed_tktlines:
        addr_str = line['Violation Location']
        chi_addr_str = "%s CHICAGO" % addr_str
        chi_parsed, chi_fails = addrparse.parse_address(chi_addr_str)

        parsed = chi_parsed 
        fails = chi_fails

        if chi_fails:
            nochi_parsed, nochi_fails = addrparse.parse_address(addr_str)

            if nochi_fails:
                nochi_fail_count = 0
                for vals in nochi_fails.values():
                    nochi_fail_count += len(vals)

                chi_fail_count = 0
                for vals in chi_fails.values():
                    chi_fail_count += len(vals)

                if chi_fail_count > nochi_fail_count:
                    parsed = nochi_parsed
                    fails = nochi_fails

        #if fails:
        #    print([addr_str, parsed, fails])

        if 1 ==1:
            address_num, street_dir, street_name, street_type = (None,None,None,None)
            try:
                address_num = int(parsed['AddressNumber'])
            except:
                address_num = None
            try:
                street_dir = parsed['StreetNamePreDirectional']
            except:
                street_dir = None
            try:
                street_name = parsed['StreetName']
            except:
                street_name = None
            try:
                street_type = parsed['StreetNamePostType']
            except:
                street_type = None

            ticket_number = int(line['Ticket Number'])
            violation_code = line['Violation Code']
            time = datetime.strptime(line['Issue Date'], '%m/%d/%Y %I:%M %p')
            day = time.isoweekday()
            timestr = time.strftime('%Y-%m-%d %H:%M:%S')
            ticket_queue = line['Ticket Queue']
            unit = line['Unit']
            badge = line['Badge']
            if len(badge) > 10:
                continue
            license_type = line['License Plate Type']
            license_state = line['License Plate State']
            license_number = line['License Plate Number']
            car_make = line['Ticket Make']
            hearing_dispo = line['Hearing Dispo']
            raw_location = addr_str

            sql_line = ( ticket_number, violation_code, address_num, street_dir, street_name, street_type, timestr,day, ticket_queue, unit, badge, license_type, license_state, license_number, car_make, hearing_dispo, raw_location)
            for_sql.append(sql_line)
            if len(for_sql) % 10000 == 0:
                count+=10000
                print "Count: %s. Inserting.." % count
                c.executemany(stmt, for_sql)
                db.commit()
                print  "done"
                for_sql = []

    c.executemany(stmt, for_sql)
    db.commit()
