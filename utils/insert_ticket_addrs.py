#!/usr/bin/python3

import csv
import psycopg2

def postgres_conn():
    connstr = "dbname=tickets host=%s user=tickets password=tickets" % "localhost"
    conn = psycopg2.connect(connstr)

    return conn

def to_from_data(db, filepath='/home/matt/git/chicago_tickets/data/levens.csv'):
    fh = open(filepath,'r')
    reader = csv.reader(fh)

    reader.__next__()
    values = [ ['street_name', f, t, 'direct'] for f,t in reader ] 

    cursor = db.cursor()
    stmt = """INSERT INTO corrections (field_type, change_from, change_to, mod_type) 
              VALUES (%s, %s, %s, %s)"""

    cursor.executemany(stmt, values)
    db.commit()
    return values

if __name__ == '__main__':
    db = postgres_conn()
    to_from_data(db)
