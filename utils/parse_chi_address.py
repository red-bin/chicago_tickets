#!/usr/bin/python3

import csv
import usaddress
import psycopg2

def postgres_conn():
    connstr = "dbname=tickets host=localhost user=tickets password=tickets"
    conn = psycopg2.connect(connstr)

    return conn

def pull_addresses(cursor):
    sql = "SELECT concat(unit,' ', addrstr_raw) FROM chicago_addrs"
    cursor.execute(sql)
    ret = (i[0] for i in cursor.fetchall() )

    return ret

def tag_addr(addr_str):
    tag_mapping = {
        'AddressNumber': 'unit',
        'StreetNamePreDirectional': 'street_dir',
        'StreetName': 'street_name',
        'StreetNamePostType': 'street_type',
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
        tagged_address, address_type = usaddress.tag(addr_str, tag_mapping=tag_mapping)

    except:
        print(addr_str)
        tagged_address = None

    return tagged_address

def parse_address(addr_str):
    tagged = tag_addr(addr_str)
    if not tagged:
        return None, None, None, None
    keys = tagged.keys()

    unit, street_dir, street_name, street_type = None, None, None, None
    scrap_pile = None

    if 'unit' in keys:
        unit = tagged['unit']
        #todo: move this to psql
        if not unit.isnumeric():
            unit = None

    if 'street_dir' in keys:
        street_dir = tagged['street_dir']
    if 'street_name' in keys:
        street_name = tagged['street_name']
    if 'street_type' in keys:
        street_type = tagged['street_type']
    if 'scrap_pile' in keys:
        scrap_pile = tagged['scrap_pile']

    return addr_str, unit, street_dir, street_name, street_type, scrap_pile

conn = postgres_conn()
cursor = conn.cursor()

parsed = ( parse_address(addr_str) for addr_str in pull_addresses(cursor) )
valid_parsed = ( parsed_addr for parsed_addr in parsed if list(set(parsed_addr))[0])

fh = open('/home/matt/data/tickets/parsed_chi_addresses.csv','w')
header = ('raw_addr', 'unit', 'street_dir', 'street_name', 'street_type', 'scrap_pile')

writer = csv.writer(fh)
writer.writerow(header)
writer.writerows(valid_parsed)
