#!/usr/bin/python3

import geopandas as gpd
from shapely import geometry

def neighborhood_shapedata():
    shapefile_dir = '/opt/data/shapefiles/'
    filename = 'geo_export_11129122-2d69-48a4-9b49-ae802351855f.shp'
    filepath = '%s/neighborhoods/%s' % (shapefile_dir, filename)

    shape_data = gpd.read_file(filepath)

    return shape_data

def neighborhood_from_latlong(lat, lon):
    point = geometry.Point(lat, lon)

    count = 0
    for hood in shapedata['geometry']:
        point = geometry.Point(lat, lon)
        if point.within(hood):
            return shapedata['community'][count]
            
        count+=1

    return None


latlongs = ((-87.67632), (41.90311))
shapedata =  neighborhood_shapedata()


print(neighborhood_from_latlong(*latlongs))

#"https://data.cityofchicago.org/api/geospatial/cauq-8yn6?method=export&format=Shapefile"
