#!/usr/bin/python3

import psycopg2
import pandas.io.sql as pandasql
import geopandas as gpd

from bokeh.models import ColumnDataSource

def pg_query(sqlstr):
    connstr = "dbname=tickets host=localhost user=tickets password=tickets"
    conn = psycopg2.connect(connstr)
    ret = pandasql.read_sql(sqlstr, conn)
    conn.close()
    return ret

def get_tickets(count=1000):
    sqlstr = """SELECT 1 as count,
                  violation_code,
                  latitude,
                  longitude
                FROM tickets
                LIMIT %s
             """ % count

    return pg_query(sqlstr)

def get_heatmap_tickets():
    sqlstr = """SELECT COUNT(EXTRACT(DOY FROM issue_date)) as count,
                       EXTRACT(DOY FROM issue_date) as doy,
                       EXTRACT(YEAR FROM issue_date) as year
                FROM tickets
                GROUP BY year, doy"""
    heatmap_data = pg_query(sqlstr)
    return heatmap_data

def get_boundaries(selected_shapefile=None):
    filepath = None
    boundaries = []
    if selected_shapefile == "Wards (2003-2015)":
        filedir = '/opt/data/shapefiles/wards2003'
        filepath = '%s/geo_export_40f24d1b-c326-4d93-ad6f-33c8a1b35fe6.shp' % filedir

    elif selected_shapefile == "Wards (2015-Present)":
        filedir = '/opt/data/shapefiles/wards2015'
        filepath = '%s/geo_export_21178b31-9758-4895-adcc-24ce80929959.shp' % filedir

    elif selected_shapefile == "Neighborhoods":
        filedir = '/opt/data/shapefiles/neighborhoods/'
        filepath = '%s/geo_export_11129122-2d69-48a4-9b49-ae802351855f.shp' % filedir

    if filepath:
        boundaries = shapefile_to_columndata(filepath)

    return boundaries

def shapefile_to_columndata(filepath):
    lines = gpd.read_file(filepath)

    boundary_lines = []
    xs = []
    ys = []
    for lines_geometry in lines['geometry']:
        geom_xys = []
        shapefile_gpd = gpd.GeoDataFrame()

        try:
            xs += lines_geometry.boundary.xy[0]
            ys += lines_geometry.boundary.xy[1]
        except:
            pass

    print("x: ", len(xs), "y:", len(ys))
    column_data = ColumnDataSource(dict(xs=xs, ys=ys))

    return dict(xs=xs, ys=ys)
