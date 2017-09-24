#!/usr/bin/python3

"""
Tickets

Usage:
  tickets.py [--filepath=<n>]

Options:
    --filepath=<n>   File for tickets [default: /opt/data/tickets/parking].
"""

from docopt import docopt

import pushers
import fetchers
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

    unparsed_chiaddrs = fetchers.chiaddrs(args['--filepath'])

    pushers.populate_chicago_table(db, unparsed_chiaddrs)
    print("Done inserting.")
