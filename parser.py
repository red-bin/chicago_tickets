#!/usr/bin/python3

import csv
import psycopg2

import geopandas as gpd

from shapely import geometry

import usaddress

datadir='/opt/data/prod_data'

chi_addrs_path = '%s/chicago_addresses.csv' % datadir
tickets_path = '%s/all_tickets.orig.txt.semicolongood.txt' % datadir
levens_path = '%s/corrections/levens.csv' % datadir
street_ranges_path = '%s/street_ranges.csv' % datadir
smarty_streets_path = '%s/smartystreet_successes.csv' % datadir

def pg_conn():
    connstr = "dbname=tickets host=localhost user=tickets password=tickets"
    conn = psycopg2.connect(connstr)

    return conn

conn = pg_conn()

def insert_raw_tickets():
    sqlstr = """
      COPY raw_tickets FROM '%s'
        WITH (FORMAT CSV, DELIMITER ';', NULL '', QUOTE '|', HEADER) ; 
      """ % tickets_path

    cursor = conn.cursor()
    cursor.execute(sqlstr)
    conn.commit()
    cursor.close()

def ticket_addresses():
    sqlstr = "SELECT DISTINCT(violation_location) from raw_tickets"
    c = conn.cursor()
    c.execute(sqlstr)
    c.fetchone()

    for addr in c.fetchall():
        yield addr[0].title()

    c.close()

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

    
    row = c.fetchone()
    while row:
        yield row
        row = c.fetchone()

    c.close()


def smarty_corrections():
    fh = open(smarty_streets_path)
    r = csv.reader(fh)

    headers = ['original', 'delivery_line_1', 'delivery_line_2', 'unit', 
               'street_predirection', 'street_name', 'street_postdirection', 
               'suffix', 'zipcode', 'latitude', 'longitude']

    for line in r:
        ret = dict(zip(headers, line))
        yield ret

    fh.close()

def smarty_corrected_map():
    addrs = ticket_addresses()
    ss_corrections = smarty_corrections()

    original_map = {}
    for correction in ss_corrections:
        original_map[correction['original']] = correction

    return original_map

       
class Ticket():
    def __init__(self, ticket_number, plate_number, license_state, license_type, car_make, issue_date, violation_location, violation_code, violation_desc, badge, unit, ticket_queue, hearing_dispo):
        self.id = id
        self.ticket_number = ticket_number
        self.license_plate = plate_number
        self.license_state = license_state
        self.license_type = license_type
        self.car_make = car_make
        self.badge = badge
        self.unit = unit
        self.ticket_queue = ticket_queue
        self.hearing_dispo = hearing_dispo

        self.issue_date = issue_date

        self.violation_code = violation_code
        self.violation_desc = violation_desc

        self.raw_location = violation_location.title()
        self.street_unit_no = None
        self.street_predirection = None
        self.street_postdirection = None
        self.street_name = None
        self.street_suffix = None
        
        self.zip = None
        self.latitude = None
        self.longitude = None

        self.geopoint = None
        self.neighborhood = None
        self.ward2003 = None
        self.ward2015 = None

        self.location = None
        self.corrected_by = None

        self.ready = False

    def graph_info(self):
        return {
            'issue_date': self.issue_date,
            'violation_code': self.violation_code,
            'badge':self.badge,
            'hearing_dispo': self.hearing_dispo,
            'unit_no':self.street_unit_no,
            'street_dir':self.street_predirection,
            'street_name':self.street_name,
            'street_suffix':self.street_suffix,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    def pg_info(self):
        return (self.issue_date, self.violation_code, self.badge, 
                self.hearing_dispo, self.street_unit_no, 
                self.street_predirection,  self.street_name, 
                self.street_suffix, self.latitude, self.longitude,
                self.ward2003, self.ward2015, self.neighborhood)

def neighborhood_shapedata():
    shapefile_dir = '/opt/data/shapefiles/'
    filename = 'geo_export_11129122-2d69-48a4-9b49-ae802351855f.shp'
    filepath = '%s/neighborhoods/%s' % (shapefile_dir, filename)

    shape_data = gpd.read_file(filepath)

    return shape_data

def wards2015_shapedata():
    shapefile_dir = '/opt/data/shapefiles/'
    filename = 'geo_export_21178b31-9758-4895-adcc-24ce80929959.shp'
    filepath = '%s/wards2015/%s' % (shapefile_dir, filename)

    shape_data = gpd.read_file(filepath)

    return shape_data

def wards2003_shapedata():
    shapefile_dir = '/opt/data/shapefiles/'
    filename = 'geo_export_40f24d1b-c326-4d93-ad6f-33c8a1b35fe6.shp'
    filepath = '%s/wards2003/%s' % (shapefile_dir, filename)

    shape_data = gpd.read_file(filepath)

    return shape_data

def neighborhood_from_point(geopoint, shapedata):
    count = 0
    for hood in shapedata['geometry']:
        if geopoint.within(hood):
            hood_name = shapedata['community'][count]
            return hood_name.title()

        count+=1

    return None

def ward2003_from_point(geopoint, shapedata):
    count = 0
    for ward in shapedata['geometry']:
        if geopoint.within(ward):
            ward_no = shapedata.ward[count]
            return ward_no

        count+=1

    return None

def ward2015_from_point(geopoint, shapedata):
    count = 0
    for ward in shapedata['geometry']:
        if geopoint.within(ward):
            ward_no = shapedata.ward[count]
            return ward_no

        count+=1

    return None


def clean_tickets():
    print("Throwing smartystreets data into memory for fast lookup")
    smarty_corrected = smarty_corrected_map()

    wards2015_geom = wards2015_shapedata()
    wards2003_geom = wards2003_shapedata()
    hoods_geom = neighborhood_shapedata()

    count = 0
    print("Starting cleanup process")

    good_hoods = 0
    bad_hoods = 0

    for t in raw_tickets():
        ticket = Ticket(*t)

        if ticket.raw_location in smarty_corrected:
            ticket.corrected_by = "smarty"
            addr_info = smarty_corrected[ticket.raw_location]

            ticket.street_unit_no = addr_info['unit']
            ticket.street_predirection = addr_info['street_predirection']
            ticket.street_name = addr_info['street_name']
            ticket.street_postdirection = addr_info['street_postdirection']
            ticket.street_suffix = addr_info['suffix']
            ticket.zipcode = addr_info['zipcode']

            ticket.latitude = float(addr_info['latitude'])
            ticket.longitude = float(addr_info['longitude'])

            ticket.ready = True

        if ticket.latitude and ticket.longitude:
            ticket.geopoint = geometry.Point(ticket.longitude, ticket.latitude)
            ticket.neighborhood = neighborhood_from_point(ticket.geopoint, hoods_geom)
            ticket.ward2003 = str(ward2003_from_point(ticket.geopoint, wards2003_geom))
            ticket.ward2015 = str(ward2015_from_point(ticket.geopoint, wards2015_geom))

            if ticket.neighborhood:
                good_hoods+=1

            else:
                bad_hoods+=1
           
        if ticket.ready:
            yield ticket
            count+=1

            if count % 10000 == 0:
                print("Hood good: %s, hood bad: %s" % (good_hoods, bad_hoods))
                conn.commit()

def insert_tickets(tickets):
    curs = conn.cursor()
    sqlstr = """INSERT INTO tickets VALUES 
             (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    for t in tickets:
        curs.execute(sqlstr, t.pg_info())

print("Inserting raw tickets' data")
insert_raw_tickets()

print("Inserting clean tickets data")

insert_tickets(clean_tickets())
