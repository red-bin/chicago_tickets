#!/usr/bin/python3

import geopandas as gpd
import json

from csv import DictReader
from multiprocessing import Pool
import pickle

shapefile_dir = '/opt/data/shapefiles/'

datadir='/opt/data/prod_data'
smarty_streets_path = '%s/smartystreet_successes.csv' % datadir

conn = misc_utils.pg_conn()

def neighborhood_blocks():
    hoods = dict([ (c,[]) for c in  hoods_geom.community ])
    hoods_len = len(hoods)
    for _, block_polyinfo in blocks_geom.T.iteritems():
        for _, hood_polyinfo in hoods_geom.T.iteritems():
            community = hood_polyinfo.community
            if block_polyinfo.geometry.within(hood_polyinfo.geometry):
                hoods[community].append(block_polyinfo)

    return hoods

neighborhood_census_blocks = neighborhood_blocks()
#fh = open('/dev/shm/census_blocks.pkl','rb')
#neighborhood_census_blocks = pickle.load(fh)

def census_block_from_point(geopoint, neighborhood=None):
    if neighborhood:
        for block in neighborhood_census_blocks[neighborhood]:
            if 'geometry' not in block.keys():
                print("%s :(" % str(block.keys()))
                continue

            if geopoint.within(block['geometry']):
                return dict(block)

    return None

def neighborhood_from_point(geopoint):
    count = 0
    for hood in hoods_geom['geometry']:
        if geopoint.within(hood):
            hood_name = hoods_geom['community'][count]
            return hood_name

        count+=1

    return None

def ward2003_from_point(geopoint):
    count = 0
    for ward in wards2003_geom['geometry']:
        if geopoint.within(ward):
            ward_no = wards2003_geom.ward[count]
            return ward_no

        count+=1

    return None

def ward2015_from_point(geopoint):
    count = 0
    for ward in wards2015_geom['geometry']:
        if geopoint.within(ward):
            ward_no = wards2015_geom.ward[count]
            return ward_no

        count+=1

    return None

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

def smarty_data():
    fh = open(smarty_streets_path)
    reader = DictReader(fh)

    ret = []
    for line in reader:
        line['latitude'] = float(line['latitude'])
        line['longitude'] = float(line['longitude'])
        ret.append(line)
    return ret
