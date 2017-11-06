#!/usr/bin/python3

import csv
import usaddress
import psycopg2

def postgres_conn():
    connstr = "dbname=tickets host=localhost user=tickets password=tickets"
    conn = psycopg2.connect(connstr)

    return conn

def pull_addresses(cursor):
    sql = "SELECT DISTINCT(raw_addr) FROM addresses"
    cursor.execute(sql)
    ret = (i[0] for i in cursor.fetchall() )

    return ret

def tag_addr(raw_addr):
    tag_mapping = {
        'AddressNumber': 'unit',
        'StreetNamePreDirectional': 'direction',
        'StreetName': 'street_name',
        'StreetNamePostType': 'suffix',
        'AddressNumberPrefix': 'scrap_pile',
        'AddressNumberSuffix': 'scrap_pile',
        'Recipient': 'scrap_pile',
        'StreetNamePreModifier': 'scrap_pile',
        'StreetNamePreType': 'scrap_pile',
        'StreetNamePostDirectional': 'scrap_pile',
        'StreetNamePostModifier': 'scrap_pile',
        'CornerOf': 'scrap_pile',
        'USPSBoxGroupID': 'scrap_pile',
        'USPSBoxGroupType': 'scrap_pile',
        'USPSBoxID': 'scrap_pile',
        'PlaceName': 'scrap_pile',
        'StateName': 'scrap_pile',
        'ZipCode': 'scrap_pile',
        'USPSBoxType': 'scrap_pile',
        'BuildingName': 'scrap_pile',
        'OccupancyType': 'scrap_pile',
        'OccupancyIdentifier': 'scrap_pile',
        'SubaddressIdentifier': 'scrap_pile',
        'SubaddressType': 'scrap_pile',
        'LandmarkName': 'scrap_pile',
        'IntersectionSeparator': 'scrap_pile',
     }

    try:
        tagged_address, address_type = usaddress.tag(raw_addr, tag_mapping=tag_mapping)

    except: #usaddress.RepeatedLabelError as e :
        print(raw_addr)
        tagged_address = None

    return tagged_address

def parse_address(raw_addr):
    tagged = tag_addr(raw_addr)
    if not tagged:
        return None, None, None, None
    keys = tagged.keys()

    unit, direction, street_name, suffix = None, None, None, None
    scrap_pile = None

    if 'unit' in keys:
        unit = tagged['unit']
        #todo: move this to psql
        if not unit.isnumeric():
            unit = None

    if 'direction' in keys:
        direction = tagged['direction']
    if 'street_name' in keys:
        street_name = tagged['street_name']
    if 'suffix' in keys:
        suffix = tagged['suffix']
    if 'scrap_pile' in keys:
        scrap_pile = tagged['scrap_pile']

    return raw_addr, unit, direction, street_name, suffix, scrap_pile

conn = postgres_conn()
cursor = conn.cursor()

parsed = ( parse_address(raw_addr) for raw_addr in pull_addresses(cursor) )
valid_parsed = ( parsed_addr for parsed_addr in parsed if list(set(parsed_addr))[0])

fh = open('/home/matt/git/chicago_tickets/data/parsed_addresses.csv','w')

header = ('raw_addr', 'street_num', 'street_dir', 'street_name', 'street_type', 'scrap_pile')

writer = csv.writer(fh)
writer.writerow(header)
writer.writerows(valid_parsed)
