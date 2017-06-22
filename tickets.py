#!/usr/bin/python3

"""
Tickets

Usage:
  tickets.py [--chiaddrs=<n> | --tickets=<n>]
  tickets.py --populate

Options:
    -t --tickets=<n>   Tickets count [default: 1].
    -r --random        Select at random
    -T --tests         Run tests
    -p --populate      Populate Chicago Addresses Table
"""

from datetime import datetime
from docopt import docopt

import addrparse
import fetchers
import pushers
import psycopg2

def postgres_conn():
    connstr = "dbname=tickets host=%s user=tickets password=tickets" % "localhost"
    conn = psycopg2.connect(connstr)

    return conn

db = postgres_conn()
c = db.cursor()

if __name__ == '__main__':
    d_args = docopt(__doc__)
    ticket_count = int(d_args['--tickets'])

    chicago_addrs = []

    if d_args['--populate']:
        pushers.populate_violations(db, '/opt/data/tickets/violation_descriptions.csv')
        #unparsed_chiaddrs = fetchers.chiaddrs()
        #pushers.populate_chicago_table(db, unparsed_chiaddrs)
        #print "Done inserting."
        exit(0)

    unparsed_tktlines = fetchers.raw_tickets(ticket_count)
    sql_strs = []

    count = 0
    for line in unparsed_tktlines:
        addr_str = line['Violation Location']
        chi_addr_str = "%s CHICAGO, Illinois" % addr_str
        chi_parsed, chi_fails = addrparse.parse_address(chi_addr_str)

        parsed = chi_parsed 
        fails = chi_fails

        time_format = '%m/%d/%Y %I:%M %p'
        time_str = datetime.strptime(line['Issue Date'], time_format)

        try:
            pushers.insert_ticket_row(c,
                                      ticket_number=int(line['Ticket Number']),
                                      violation_code=line['Violation Code'], 
                                      address_num=int(parsed['AddressNumber']), 
                                      addr_id=None,
                                      street_dir=parsed['StreetNamePreDirectional'], 
                                      street_name=parsed['StreetName'], 
                                      street_type=parsed['StreetNamePostType'],
                                      time=time_str,
                                      weekday=time_str.isoweekday(),
                                      ticket_queue=line['Ticket Queue'],
                                      unit=line['Unit'],
                                      badge=line['Badge'],
                                      license_type=line['License Plate Type'],
                                      license_state=line['License Plate State'],
                                      license_number=line['License Plate Number'],
                                      car_make=line['Ticket Make'],
                                      hearing_dispo=line['Hearing Dispo'],
                                      raw_location=addr_str)
        except:
            print(line)

        count += 1
        if (count % 100000) == 0:
            print(count) 
            db.commit()
