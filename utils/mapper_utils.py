#!/usr/bin/python3

import psycopg2
import pandas.io.sql as pandasql
import pandas as pd
import json
import folium
import geopandas as gpd

from bokeh.models import ColumnDataSource
rootpath = '/opt/data/shapefiles'

def pg_query(sqlstr, index_col=None):
    connstr = "dbname=tickets host=localhost user=tickets password=tickets"
    conn = psycopg2.connect(connstr)

    if index_col: 
        ret = pandasql.read_sql(sqlstr, conn, index_col=index_col)
    else:
        ret = pandasql.read_sql(sqlstr, conn)

    conn.close()
    return ret

def get_tickets(count=1000):
    sqlstr = """SELECT * FROM addresses as a 
                INNER JOIN tickets 
                ON tickets.violation_location = a.original LIMIT %s;""" % count

    return pg_query(sqlstr)

def mapbox_data():
    sqlstr = """SELECT a.latitude, a.longitude,
                        t.issue_date,
                        t.violation_code,
                        t.hearing_dispo 
                FROM addresses as a, 
                     tickets as t
                WHERE a.original = t.violation_location"""

    return pg_query(sqlstr)


def counts_by_alias(alias):
    alias_cols = {
       'neighborhoods':'neighborhood',
       "wards2003": 'ward_2003',
       "wards2015": 'ward_2015',
       "census_tracts": 'tractce10',
       "census_blocks": 'tract_bloc' }

    key = alias_cols[alias]
    
    sqlstr = """SELECT * from (select count(a.%s) as sum, a.%s
                from tickets t, addresses as a 
                WHERE t.violation_location = a.original
                AND a.%s is not null
                GROUP BY a.%s) as foo
                WHERE sum < 50000""" % (key, key, key, key)

    return pg_query(sqlstr), key

def sample_counts_neighborhood():
    return pg_query(sqlstr)

def sum_ts_by_key(key, duration):
    inputs = (duration, key, duration, key)

    sqlstr="""
    SELECT sum(cost), time_bucket('%s', issue_date), %s
      FROM violations as v, addresses AS a
      INNER JOIN tickets AS t
      ON t.violation_location = a.original
      WHERE v.code = t.violation_code
      GROUP BY time_bucket('%s', issue_date), %s
      ORDER BY sum""" % inputs

    return pg_query(sqlstr)
