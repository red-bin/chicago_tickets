#!/usr/bin/python3

import csv
import usaddress
import psycopg2


def pg_conn():
    connstr = "dbname=tickets host=localhost user=tickets password=tickets"
    conn = psycopg2.connect(connstr)

    return conn

datadir='/opt/data/prod_data'
tickets_path = '%s/all_tickets.orig.txt.semicolongood.txt' % datadir
conn = pg_conn()

def ticket_addresses():
    sqlstr = "SELECT DISTINCT(violation_location) from raw_tickets"
    c = conn.cursor()
    c.execute(sqlstr)
    c.fetchone()

    addresses = [ a[0].title() for a in c.fetchall() ]
    return addresses

def insert_raw_tickets():
    sqlstr = """
      COPY raw_tickets FROM '%s'
        WITH (FORMAT CSV, DELIMITER ';', NULL '', QUOTE '|', HEADER) ; 
      """ % tickets_path

    cursor = conn.cursor()
    cursor.execute(sqlstr)
    conn.commit()
    cursor.close()

def tag_addr(addr):
    tag_mapping = {
        'AddressNumber': 'unit',
        'StreetNamePreDirectional': 'direction',
        'StreetName': 'street_name',
        'StreetNamePostType': 'suffix',
        'AddressNumberPrefix': 'unit_prefix',
        'AddressNumberSuffix': 'unit_suffix',
        'Recipient': 'recipient',
        'StreetNamePreModifier': 'pre_mod',
        'StreetNamePreType': 'pre_type',
        'StreetNamePostDirectional': 'post_dir',
        'StreetNamePostModifier': 'scrap_pile',
        'CornerOf': 'corner_of',
        'USPSBoxGroupID': 'usps_group_id',
        'USPSBoxGroupType': 'usps_group_type',
        'USPSBoxID': 'usps_id',
        'PlaceName': 'place_name',
        'StateName': 'state_name',
        'ZipCode': 'zip',
        'USPSBoxType': 'usps_type',
        'BuildingName': 'building_name',
        'OccupancyType': 'occupancy_type',
        'OccupancyIdentifier': 'occupancy_id',
        'SubaddressIdentifier': 'subaddr_id',
        'SubaddressType': 'subaddr_type',
        'LandmarkName': 'landmark_name',
        'IntersectionSeparator': 'intersection_sep',
     }

    tagged_address, address_type = usaddress.tag(addr, tag_mapping=tag_mapping)

    return tagged_address

def raw_tickets():
    sqlstr = "SELECT * from raw_tickets"
    c = conn.cursor()
    c.execute(sqlstr)
    c.fetchone()

    return c.fetchall()
