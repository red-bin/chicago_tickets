#!/usr/bin/python3

import csv
import distance
import psycopg2

from pprint import pprint

street_range_filepath = '~/git/chicago_tickets/data/Chicago_Street_Names.csv'

def postgres_conn():
    connstr = "dbname=tickets host=%s user=tickets password=tickets" % "localhost"
    conn = psycopg2.connect(connstr)

    return conn

def valid_streets(db):
    streets = []
    cursor = db.cursor()

    cursor.execute("SELECT DISTINCT(street) FROM street_ranges")
    [ streets.append(l[0].strip()) for l in cursor.fetchall() if l ]

    return streets

def ticket_streets(db):
    streets = []
    cursor = db.cursor()

    cursor.execute("SELECT DISTINCT(street_name) FROM tickets")
    [ streets.append(l[0].strip()) for l in cursor.fetchall() if l ]

    return streets

def closest_leven(token, comparers, n=1):
    levens = [ (c, distance.nlevenshtein(token, c)) for c in comparers ]
    
    lowest_val = 1
    lowest_comparers = []
    for comparer, levens_dist in levens:
        if levens_dist < lowest_val:
            lowest_comparers = [(comparer, levens_dist)]
            lowest_val = levens_dist

        elif levens_dist == lowest_val:
            lowest_comparers.append((comparer, levens_dist))

    if lowest_comparers[:n]:
        return lowest_comparers[:n]

    else:
        return None

if __name__ == '__main__':
    db = postgres_conn()
    good_streets = valid_streets(db)
    tkt_streets = ticket_streets(db)

    unknowns = [ t for t in tkt_streets if t not in good_streets ]
    closests = [ (t,closest_leven(t, good_streets)) for t in unknowns ]
    useful = [ (b[0], b[1][0]) for b in [ c for c in closests if c ] if b[1][0][1] < .2 ]
    pprint(useful)


    out_fh = open('/tmp/levens.csv','w')
    writer = csv.writer(out_fh)
    writer.writerows(useful)
