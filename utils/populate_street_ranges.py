#!/usr/bin/python

#!/usr/bin/python2.7

import csv
import psycopg2

street_range_filepath = '~/git/chicago_tickets/data/Chicago_Street_Names.csv'

def postgres_conn():
    connstr = "dbname=tickets host=%s user=tickets password=tickets" % "localhost"
    conn = psycopg2.connect(connstr)

    return conn

def insert_ranges(db_handle, filepath=street_range_filepath):
    fh = open('/home/matt/git/chicago_tickets/data/Chicago_Street_Names.csv','r')

    reader = csv.reader(fh)
    header = reader.next()

    lines = [ l for l in reader ]
    stmt = """INSERT INTO street_ranges 
             (full_name, direction, street, suffix, 
              suffix_dir, min_address, max_address) 
              VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    c = db_handle.cursor()
    c.executemany(stmt, lines)
    db.commit()

    return

if __name__ == '__main__':
    db = postgres_conn()
    insert_ranges(db)
