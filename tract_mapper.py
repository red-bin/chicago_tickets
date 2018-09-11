#!/usr/bin/python3

import folium
import numpy as np
from utils import geo_tools
from utils import mapper_utils


color_map = ['#fff7f3','#fde0dd','#fcc5c0','#fa9fb5','#f768a1','#dd3497','#ae017e','#7a0177','#49006a']

for alias in ('neighborhoods', 'wards2003', 'wards2015', 'census_tracts', 'census_blocks'):
    m = folium.Map(tiles=None, location=(41.8481, -87.731),
                   zoom_start=10.5, height=900,
                   width=700, no_touch=True)
    print("===",alias,"===")

    print(" Grabbing boundaries")
    geo_data, geo_key = geo_tools.geojson_by_boundary_alias(alias)
    print(" Grabbing data")
    timeseries_data, data_key = mapper_utils.counts_by_alias(alias)

    print(" Creating choropleth")

    #threshold_scale = list(np.histogram(timeseries_data['sum'], bins=5)[1])
    #print(threshold_scale)

    m.choropleth(geo_data=geo_data,
                 key_on = 'feature.properties.%s' % geo_key,
                 data = timeseries_data,
                 columns=[data_key, 'sum'],
                 fill_color='YlGnBu',
    #             threshold_scale = threshold_scale,
                 line_weight=.1)

    print(" Saving choropleth")
    m.save('/tmp/%s.html' % alias)
