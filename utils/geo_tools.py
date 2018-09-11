#!/usr/bin/python3

import json
import folium

from os.path import exists
from requests import get

geocache_dir = '/opt/data/tickets/cache/geodata'

def download_data(page_id, place_name=None, file_format="GeoJSON"):
    print("Downloading map %s.." % page_id)
    url = "https://data.cityofchicago.org/api/geospatial/%s?method=export&format=%s"
    url = url % (page_id, file_format)

    resp = get(url)

    try:
        resp_json = resp.json()
    except:
        resp_json = None
 
    if resp_json:
        fp = "%s/%s.geojson" % (geocache_dir, place_name)
        fh = open(fp, 'w')
        json.dump(resp_json, fh)

        return resp_json

    else:
        print("unable to get geodata of %s" % place_name)
        return None

def geojson_by_boundary_alias(place_name, save=False, file_format="GeoJSON"):
    key = None
    if place_name == "neighborhoods":
        path_id = "bbvz-uum9"
        key = 'sec_neigh'
    elif place_name == "wards2003":
        path_id = "xt4z-bnwh"
        key = 'ward'
    elif place_name == "wards2015":
        path_id = "sp34-6z76"
        key = 'ward'
    elif place_name == "census_tracts":
        path_id = "5jrd-6zik"
        key = 'tractce10'
    elif place_name == "census_blocks":
        path_id = "mfzt-js4n"
        key = 'tract_bloc'

    geojson_fp = "%s/%s.geojson" % (geocache_dir, place_name)
    if not exists(geojson_fp) and key:
        download_data(path_id, place_name=place_name)
        geo_data = geojson_by_boundary_alias(place_name)

    else:
        geo_data = json.load(open(geojson_fp,'r'))

    return geo_data, key
