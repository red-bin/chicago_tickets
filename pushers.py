#!/usr/bin/python2.7

import addrparse
import csv

from pprint import pprint

def insert_usaddress_keyvals(cursor, keyvals):
    stmt = "INSERT INTO usaddresses_parse (token_key, token_val, position) VALUES (%s, %s, %s)"

    count = 1
    values = []
    for k, v in keyvals:
        values.append((k, v, count))
        count+=1

    cursor.executemany(stmt, values)

def insert_ticket_row(cursor, ticket_number=None, violation_code=None, address_num=None, 
        street_dir=None, street_name=None, street_type=None, time=None, 
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
                 ticket_queue,
                 unit,
                 badge,
                 license_type,
                 license_state,
                 license_number,
                 car_make,
                 hearing_dispo,
                 raw_location) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                       %s, %s, %s, %s, %s, %s, %s, %s)""" 

    cursor.execute(stmt, (ticket_number, violation_code, address_num, 
               addr_id, street_dir, street_name, street_type, time,
               ticket_queue, unit, badge, license_type, license_state, 
               license_number, car_make, hearing_dispo, raw_location))

    return stmt

def populate_chicago_table(db, unparsed_chiaddrs):
    chicago_addrs = []
    for unparsed in unparsed_chiaddrs:
        parsed_address, failures, parsed_list = addrparse.parse_address(unparsed['Address'])

        latitude = unparsed['LATITUDE']
        longitude = unparsed['LONGITUDE']

        try:
            latitude = float(latitude)
        except:
            print(latitude)
            latitude=0.0

        try:
            longitude = float(longitude)
        except:
            print(longitude)
            longitude=0.0

        entry = [ parsed_address['AddressNumber'],
            parsed_address['StreetNamePreDirectional'].rstrip(),
            parsed_address['StreetName'].rstrip(),
            parsed_address['StreetNamePostType'].rstrip(),
            latitude,
            longitude ]

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
    c.executemany(stmt, (l for l in r))
    db.commit()

def batch_inserts(db, stmt, values, n=10000):
    cursor = db.cursor()
    cursor.executemany(stmt, values)

    db.commit()
