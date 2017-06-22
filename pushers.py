#!/usr/bin/python2.7

import addrparse
import csv

user_stuff = """
CREATE USER tickets PASSWORD 'tickets' ;
alter table chicago_addresses owner to "tickets" ;                     
alter table tickets owner to "tickets" ;
alter table violations owner to "tickets" ;
"""

tickets_sql = """
CREATE TABLE tickets (
  id SERIAL PRIMARY KEY,
  ticket_id BIGINT,
  ticket_number BIGINT,
  violation_code CHAR(15),
  address_num INTEGER,
  addr_id INTEGER REFERENCES chicago_addresses (id),
  street_dir CHAR(10),
  street_name TEXT,
  street_type CHAR(20),
  time TIMESTAMP,
  weekday INTEGER,
  ticket_queue CHAR(20),
  unit CHAR(20),
  badge CHAR(10),
  license_type CHAR(20),
  license_state CHAR(5),
  license_number CHAR(15),
  car_make CHAR(20),
  hearing_dispo CHAR(20),
  raw_location CHAR(50))
"""
chicago_addresses_sql= """
CREATE TABLE chicago_addresses (
    id SERIAL PRIMARY KEY,
    address_number INTEGER,
    street_dir CHAR(10),
    street_name CHAR(50),
    street_type CHAR(20),
    latitude FLOAT,
    longitude FLOAT)
"""

ticket_desc_sql = """
    CREATE TABLE violations (
      id SERIAL PRIMARY KEY,
      code TEXT,
      description TEXT,
      cost FLOAT)
"""
      


def insert_ticket_row(cursor, ticket_number=None, violation_code=None, address_num=None, 
        street_dir=None, street_name=None, street_type=None, time=None, weekday=None, 
        ticket_queue=None, unit=None, badge=None, license_type=None, license_state=None, 
        license_number=None, car_make=None, hearing_dispo=None, raw_location=None, addr_id=None):

    stmt = """INSERT INTO tickets 
                (ticket_number,
                 violation_code,
                 address_num, 
                 addr_id,
                 street_dir, 
                 street_name, 
                 street_type, 
                 time,
                 weekday,
                 ticket_queue,
                 unit,
                 badge,
                 license_type,
                 license_state,
                 license_number,
                 car_make,
                 hearing_dispo,
                 raw_location) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                       %s, %s, %s, %s, %s, %s, %s, %s)""" 


    cursor.execute(stmt, (ticket_number, violation_code, address_num, 
               addr_id, street_dir, street_name, street_type, time, weekday, 
               ticket_queue, unit, badge, license_type, license_state, 
               license_number, car_make, hearing_dispo, raw_location))

    return stmt

def populate_chicago_table(db, unparsed_chiaddrs):
    chicago_addrs = []
    for unparsed in unparsed_chiaddrs:
        parsed_address,fails = addrparse.parse_address(unparsed['Address'])
        latitude = unparsed['LATITUDE']
        longitude = unparsed['LONGITUDE']

        try:
            entry = [ int(parsed_address['AddressNumber']),
                parsed_address['StreetNamePreDirectional'],
                parsed_address['StreetName'],
                parsed_address['StreetNamePostType'],
                float(latitude),
                float(longitude) ]

        except:
            try:
                entry = [ parsed_address['AddressNumber'],
                    parsed_address['StreetNamePreDirectional'],
                    parsed_address['StreetName'],
                    parsed_address['StreetNamePreType'],
                    latitude,
                    longitude ]
            except:
                entry = None

        if entry:
            chicago_addrs.append(entry)

    stmt = 'INSERT INTO chicago_addresses (address_number, street_dir, street_name, street_type, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s)'

    c = db.cursor()
    c.executemany(stmt, chicago_addrs)
    db.commit()

def populate_violations(db, filename):
    fh = open(filename,'r')

    r = csv.reader(fh)
    r.next()

    c = db.cursor()

    stmt = "INSERT INTO violations (code, description, cost) VALUES (%s, %s, %s)"
    c.executemany(stmt, [l for l in r])
    db.commit()

def batch_inserts(db, stmt, values, n=10000):
    cursor = db.cursor()

    cursor.executemany(stmt, values)

    db.commit()
