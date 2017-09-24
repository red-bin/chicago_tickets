#!/usr/bin/python3

"""
Tickets

Usage:
  tickets.py [--infile=<n>] [--outfile=<n>]

Options:
    -i --infile=<n>    Infile [default: /opt/data/tickets/parking/all_tickets.orig.txt]
    -o --outfile=<n>   Outfile [default: /opt/data/tickets/tickets.csv]
"""

from docopt import docopt
import csv

if __name__ == '__main__':
    args = docopt(__doc__)

    in_filepath = args['--infile']
    out_filepath = args['--outfile']

    in_fh = open(in_filepath, 'r')
    out_fh = open(out_filepath, 'w')

    r = csv.reader(in_fh, delimiter=';')
    r.__next__() #throw away header

    w = csv.writer(out_fh)
    header = ['ticket_number','plate_number','license_state',
              'license_type','car_make','issue_date','violation_location',
              'violation_code','badge','unit','ticket_queue','hearing_dispo']

    w.writerow(header)
    w.writerows(r)

    in_fh.close()
    out_fh.close()
