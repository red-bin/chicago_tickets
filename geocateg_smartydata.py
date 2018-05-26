#!/usr/bin/python3

import utils.addr_utils as a_utils
import csv
print("Done importing addr_utils")

import multiprocessing, logging
import tqdm
import psycopg2

from shapely import geometry

from multiprocessing import Pool

def pg_conn():
    connstr = "dbname=tickets host=localhost user=tickets password=tickets"
    conn = psycopg2.connect(connstr)

    return conn

conn = pg_conn()

def geometadata_addr(addr):
    geopoint = geometry.Point(addr['longitude'], addr['latitude'])
    neighborhood = a_utils.neighborhood_from_point(geopoint)
    ward_2003 = a_utils.ward2003_from_point(geopoint)
    ward_2015 = a_utils.ward2015_from_point(geopoint)

    ret = addr #return back generated data AND original data

    if neighborhood:
        census_neighborhood = a_utils.neighborhood_census_blocks[neighborhood]
        census_block = a_utils.census_block_from_point(geopoint, 
                                                       neighborhood=neighborhood)
    else:
        census_block = None

    ret.update(neighborhood=neighborhood,
               ward_2003=ward_2003,
               ward_2015=ward_2015)

    if census_block:
        if 'geometry' in census_block.keys():
            census_block.pop('geometry')

        ret.update(census_block)
    else:
        keys = ['blockce10', 'countyfp10', 'geoid10', 'name10', 
                'statefp10', 'tract_bloc', 'tractce10']
        census_block_empty = dict([ (k,None) for k in keys])
        ret.update(census_block_empty)

    return ret

def insert_addresses(values=None):
    sqlstr = """INSERT INTO addresses (
                  original, delivery_line_1, delivery_line_2,
                  unit, street_predirection, street_name,
                  suffix, street_postdirection, zipcode,
                  longitude, latitude, neighborhood,
                  ward_2003, ward_2015, blockce10,
                  tract_bloc, statefp10, geoid10,
                  name10, tractce10, countyfp10)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s)"""

    if not values:
        try:
            fh = open('/opt/data/smartystreets_augmented.csv','r')
            values = csv.DictReader(fh)

        except:
            print("Cached metadata doesn't exist. Quitting")

    curs = conn.cursor()
    for row in values:
        sql_vals = [ 
          row['original'],
          row['delivery_line_1'],
          row['delivery_line_2'],
          row['unit'],
          row['street_predirection'],
          row['street_name'],
          row['suffix'],
          row['street_postdirection'],
          row['zipcode'],
          row['longitude'],
          row['latitude'],
          row['neighborhood'],
          row['ward_2003'],
          row['ward_2015'],
          row['blockce10'],
          row['tract_bloc'],
          row['statefp10'],
          row['geoid10'],
          row['name10'],
          row['tractce10'],
          row['countyfp10']]
        curs.execute(sqlstr, sql_vals)

    conn.commit()
    conn.close()

print("Loading smartystreets data")
smarty_data = a_utils.smarty_data()

print("Creating pools")
pool = Pool(processes=32)
print("Pools created - running stuff")
metadata_results = pool.map(geometadata_addr, smarty_data)

insert_addresses(metadata_results)

#fh = open('/opt/data/smartystreets_augmented.csv','w')
#w = csv.DictWriter(fh, fieldnames=list(result[0].keys()))
#w.writeheader()
#w.writerows(result)
#fh.close()
