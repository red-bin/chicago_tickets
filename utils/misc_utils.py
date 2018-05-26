#!/usr/bin/python3

import psycopg2
import requests

from lxml import html

def pg_conn():
    connstr = "dbname=tickets host=localhost user=tickets password=tickets"
    conn = psycopg2.connect(connstr)

    return conn

def insert_violations():
    url = "https://www.cityofchicago.org/city/en/depts/fin/supp_info/revenue/general_parking_ticketinformation/violations.html"
    resp = requests.get(url)

    tree = html.fromstring(resp.content)
    table_elem = tree.xpath("/html/body/div/div[2]/div/div/div/div/div[1]/div[3]/div/div/table/tbody/tr/td/table") 
    raw_rows = table_elem[0].text_content().split('\n\n\n')
    rows = [r.split('\n') for r in raw_rows if '$' in r]

    conn = pg_conn()
    curs = conn.cursor()
    sqlstr = "INSERT INTO violations VALUES (%s, %s, %s)"
    for violation_code, violation_desc, cost in rows:
        violation_code = violation_code.split('*')[0]
        violation_desc = violation_desc.strip()

        cost = int(float(cost.split('$')[-1]))
        curs.execute(sqlstr, (violation_code, violation_desc, cost))

    conn.commit()
    conn.close()
