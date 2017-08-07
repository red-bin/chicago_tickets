#!/usr/bin/python2.7

import psycopg2
import fetchers

def postgres_conn():
    connstr = "dbname=tickets host=%s user=tickets password=tickets" % "localhost"
    conn = psycopg2.connect(connstr)

    return conn

db = postgres_conn()
ticket_descripts = fetchers.ticket_descriptions(db)

datadir = '/opt/data/tickets'
raw_tickets = '%s/parking/all_tickets.orig.txt' % datadir
chiaddrs = '%s/chicago_addresses.csv' % datadir

fix_addrs = True
