#!/usr/bin/python3

import json
import folium

from os.path import exists
from requests import get

geocache_dir = '/opt/data/tickets/cache/geodata'

def download_data(page_id, place_name=None, file_format="GeoJSON"):
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
    geojson_fp = "%s/%s.geojson" % (geocache_dir, place_name)
    print("checking: %s" % geojson_fp)
    if not exists(geojson_fp):
        print("does not exist")
        if place_name == "neighborhoods":
            geo_data = download_data("bbvz-uum9", place_name=place_name)
        elif place_name == "wards2003":
            geo_data = download_data("xt4z-bnwh", place_name=place_name)
        elif place_name == "wards2015":
            geo_data = download_data("sp34-6z76", place_name=place_name)
        elif place_name == "census_blocks":
            geo_data = download_data("5jrd-6zik", place_name=place_name)
        else:
            return None

    else:
        print("file already exists")
        geo_data = json.load(open(geojson_fp,'r'))

    if geo_data:
        return geo_data

    print('geodata doesn\'t exist.')
    return
