#!/usr/bin/python3

from os import listdir
import re
import folium

import moviepy.editor as mpy
import numpy as np

import pickle

from selenium import webdriver
from time import sleep

from multiprocessing import Pool
from utils import mapper_utils
from utils import geo_tools

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

def create_bucket_map(bucket_data, shape_alias='census_blocks'):
    print("shape alias: %s", shape_alias)

    m = folium.Map(tiles=None, location=(41.8481, -87.731), 
                zoom_start=10.5, height=900, 
                width=700, no_touch=True)

    geo_data = geo_tools.geojson_by_boundary_alias(shape_alias)
    if geo_data:
        m.choropleth(geo_data=geo_data,
                 data=bucket_data,
                 columns=['sum'],
                 key_on = 'feature.properties.tract_bloc',
                 fill_color='YlOrRd',
                 threshold_scale=dist_threshold)
    else:
        print(":(")
        return None

    return m

def pngs_to_webm(filepaths):
    clip = mpy.ImageSequenceClip(filepaths, fps=24, load_images=True)
    clip.write_videofile('/opt/data/test.webm')

def html_to_png(page_fp):
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=firefox_options)

    page_path = "file://%s" % page_fp
    driver.get(page_path)

    #delete zoom
    try:
        zoom_elem = driver.find_element_by_xpath("/html/body/div/div[2]/div[1]")
        driver.execute_script("""var element = arguments[0];
                            element.parentNode.removeChild(element);""", zoom_elem)
    except:
        print("unable to remove zoom...")

    #save map elem
    filename = re.split('[/.]', page_fp)[-2]
    screenshot_savepath = "/opt/data/tickets/cache/screenshots/%s" % filename
    map_elem = driver.find_element_by_tag_name("div")
    map_elem.screenshot(screenshot_savepath) 

    driver.quit()

    return screenshot_savepath

def save_bucket_as_png(bucket_name):
    bucket_data = timeseries_data[(timeseries_data['time_bucket'] == bucket_name)]
    if len(bucket_data) == 0:
        return None

    bucket_map = create_bucket_map(bucket_data, shape_alias='census_blocks')
    if not bucket_map:
        return None

    prefix = str(bucket_name).split(' ')[0]
    html_filename = "/opt/data/tickets/cache/html/%s.html" % prefix
    bucket_map.save(html_filename)

    png_filename = html_to_png(html_filename)

    return png_filename

def create_map_video():
    time_buckets = sorted(list(set(timeseries_data['time_bucket'])))

    pool = Pool(processes=33)
    png_paths = pool.map(save_bucket_as_png, time_buckets)
    png_paths = sorted([p for p in png_paths if p != None])

    pngs_to_webm(png_paths)

#timeseries_data = mapper_utils.get_census_blocks_timeseries()
#pickle.dump(timeseries_data, open('/opt/data/timeseries_data.pkl','wb'))

timeseries_data = pickle.load(open('/opt/data/timeseries_data.pkl','rb'))
#shape_path = "/opt/data/shapefiles/neighborhoods/neighborhoods.geo.json"
#dist_threshold = list(reversed(np.histogram(timeseries_data['sum'], bins='sturges')[0]))
dist_threshold = sorted(list(reversed(np.histogram(timeseries_data['sum'], bins=6)[0])))
#create_map_video()
