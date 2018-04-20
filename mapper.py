#!/usr/bin/python3

import psycopg2

import numpy as np
import pandas.io.sql as pandasql

from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.models.widgets import RangeSlider, Slider, Select, TextInput
from bokeh.io import curdoc
from bokeh.sampledata.movies_data import movie_path

from os.path import dirname, join

def query(sqlstr):
    connstr = "dbname=tickets host=localhost user=tickets password=tickets"
    conn = psycopg2.connect(connstr)
    ret = pandasql.read_sql(sqlstr, conn)
    conn.close()

    return ret

def get_tickets():
    sqlstr = """SELECT 
                 issue_date, violation_code, 
                 hearing_dispo, latitude, longitude
               FROM tickets LIMIT 10000
             """

    return query(sqlstr)

def select_tickets():
    selected = tickets

    viol_selected = viol_selecter.value
    dispo_selected = dispo_selecter.value
    if viol_selected != "All":
        selected = selected[selected.violation_code.str.contains(viol_selected)==True]
    if dispo_selected != "All":
        selected = selected[selected.hearing_dispo.str.contains(dispo_selected)==True]

    return selected 

def update():
    df = select_tickets()
    source.data = dict(
      x=df['longitude'],
      y=df['latitude'],
      hearing_dispo=df['hearing_dispo'],
      violation=df['violation_code'],
    )

tickets = get_tickets()
viol_list = ['All'] + open('violations.txt', 'r').readlines()

viol_title = "Violation Code"
dispo_title = "Hearing Disposition"

dispo_list = ['All', 'Denied', 'Stricken', 'Granted', 'Withdrawn', 'DOR Withdraw', 'Liable', 'Paid', 'DUMMY CASE CREATED', 'Preliminary', 'Not Liable', 'Continued']

viol_selecter = Select(title=viol_title, value="All", options=viol_list)
dispo_selecter = Select(title=dispo_title, value="All", options=dispo_list)

controls = (viol_selecter, dispo_selecter)
source = ColumnDataSource(data=dict(x=[], y=[], violation=[], lat=[], lon=[]))

p = figure(plot_height=1000, plot_width=750, title="Tickets!",
             toolbar_location=None)

p.circle(x="x", y="y", source=source, size=7)

for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'
inputs = widgetbox(*controls, sizing_mode=sizing_mode)

desc = Div(text=open(join(dirname(__file__), "page.html")).read(), width=800)

update()  # initial load of the data
l = layout([ [desc], [inputs, p]], sizing_mode=sizing_mode)
print("Got here")

curdoc().add_root(l)
curdoc().title = "lolwut"
