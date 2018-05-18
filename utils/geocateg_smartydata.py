#!/usr/bin/python3

import addr_utils as a_utils
import csv
print("Done importing addr_utils")
import multiprocessing, logging
import tqdm

from shapely import geometry

from multiprocessing import Pool

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

print("Loading smartystreets data")
smarty_data = a_utils.smarty_data()

print("Creating pools")
pool = Pool(processes=32)
print("Pools created - running stuff")
result = pool.map(geometadata_addr, smarty_data)

fh = open('/opt/data/smartystreets_augmented.csv','w')
w = csv.DictWriter(fh, fieldnames=list(result[0].keys()))
w.writeheader()
w.writerows(result)
fh.close()
