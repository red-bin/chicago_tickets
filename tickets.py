#!/usr/bin/python3

"""
Tickets

Usage:
  tickets.py [--ticketfile=<n>]
  tickets.py --populate

Options:
    -t --ticketfile=<n>   File for tickets [default: /opt/data/tickets/parking].
    -p --populate         Populate Chicago Addresses Table
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
    args = docopt(__doc__)

    chicago_addrs = []
    unparsed_tktlines = fetchers.raw_tickets(args['--ticketfile'])
    time_format = '%m/%d/%Y %I:%M %p'

    count = 0
    for line in unparsed_tktlines:
        addr_str = line['Violation Location']

        chi_addr_str = "%s, CHICAGO, ILLINOIS" % addr_str
        #chi_parsed, usaddress_keyvals = addrparse.parse_address(chi_addr_str)

        pushers.insert_usaddress_keyvals(c, usaddress_keyvals)


        time_str = datetime.strptime(line['Issue Date'], time_format)
        pushers.insert_ticket_row(c,
                                  ticket_number=int(line['Ticket Number']),
                                  violation_code=line['Violation Code'], 
                                  addr_id=None,
                                  time=time_str,
                                  ticket_queue=line['Ticket Queue'],
                                  unit=line['Unit'],
                                  badge=line['Badge'],
                                  license_type=line['License Plate Type'],
                                  license_state=line['License Plate State'],
                                  license_number=line['License Plate Number'],
                                  car_make=line['Ticket Make'],
                                  hearing_dispo=line['Hearing Dispo'],
                                  raw_location=addr_str)

        count += 1
        if (count % 100000) == 0:
            print(count) 
            db.commit()
