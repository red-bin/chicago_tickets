#!/usr/bin/python3

"""
Tickets

Usage:
  tickets.py [--infile=<n>]

Options:
    -i --infile=<n>    Infile [default: /opt/data/tickets/parking/all_tickets.orig.txt]
"""

from docopt import docopt
import csv

#import psycopg2
from prometheus_client import start_http_server, Counter, CollectorRegistry, write_to_textfile

if __name__ == '__main__':
    args = docopt(__doc__)

    in_filepath = args['--infile']
    in_fh = open(in_filepath, 'r')
    r = csv.reader(in_fh)
    keys = r.__next__()


    keys = ['ticket_no', 'plate_no', 'plate_state', 'plate_type', 'car_make', 'timestamp', 'addr', 'code', 'badge', 'unit', 'queue', 'dispo']

    registry = CollectorRegistry()
    c = Counter('tickets', 'Parking tickets', labelnames=keys, registry=registry)

    for ticket_no, plate_no, plate_state, plate_type, car_make, timestamp, addr, code, description, badge, unit, queue, dispo in r:
        c.labels(ticket_no, plate_no, plate_state, plate_type, car_make, timestamp, addr, code, badge, unit, queue, dispo).inc()

    write_to_textfile('/dev/shm/registry.prom', registry)
