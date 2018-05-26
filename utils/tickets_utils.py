#!/usr/bin/python3

import csv
import usaddress
import psycopg2

from multiprocessing import Pool

def pg_conn():
    connstr = "dbname=tickets host=localhost user=tickets password=tickets"
    conn = psycopg2.connect(connstr)

    return conn

datadir='/opt/data/prod_data'
tickets_path = '%s/all_tickets.orig.txt.semicolongood.txt' % datadir
conn = pg_conn()

def ticket_addresses():
    sqlstr = "SELECT DISTINCT(violation_location) from tickets"
    c = conn.cursor()
    c.execute(sqlstr)
    c.fetchone()

    addresses = [ a[0].title() for a in c.fetchall() ]
    return addresses

def insert_tickets():
    fh = open(tickets_path, 'r')
    reader = csv.reader(fh)
    sqlstr = """
      COPY tickets FROM '%s'
        WITH (FORMAT CSV, DELIMITER ';', NULL '', QUOTE '|', HEADER) ; 
      """ % tickets_path

    cursor = conn.cursor()
    print("Inserting tickets from %s into tickets table" % tickets_path)
    cursor.execute(sqlstr)
    print("Fixing capitalization of violation_location")
    cursor.execute("UPDATE tickets set violation_location = initcap(violation_location)")
    print("done")
    conn.commit()
    cursor.close()

def tickets():
    sqlstr = "SELECT * from tickets"
    c = conn.cursor()
    c.execute(sqlstr)
    c.fetchone()

    return c.fetchall()
