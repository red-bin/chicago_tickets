#!/usr/bin/python3

from bokeh.io import curdoc
from bokeh.layouts import layout, widgetbox, column
from bokeh.models import Div, LogColorMapper, ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.plotting import figure, show

import utils.mapper_utils as mapper_utils

shapefile_aliases = ["Wards (2003-2015)", "Wards (2015-Present)", "Neighborhoods"]

class TicketsApp():
    def __init__(self, test=True):
        self.min_long = -87.52
        self.min_lat = 41.625
        self.max_long = -87.875
        self.max_lat = 42.05

        self.boundary_lines = None
        self.boundary_fig = None

        colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce",
                  "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]

        self.color_mapper = LogColorMapper(palette=colors, low=10, high=50000)

        if test:
            self.tickets = mapper_utils.get_tickets(100000)
        else:
            self.tickets = mapper_utils.get_tickets(60000000)

        self.mapfigure = self.map_figure()
        #self.boundary_fig = self.shapefile_figure("Neighborhoods")
        self.mapped_controls = [self.shapefile_selecter()]

    def create_layout(self):
        inputs = widgetbox(*self.mapped_controls, sizing_mode='fixed')
        desc = column()


        bokeh_objs = [inputs, self.boundary_fig, self.mapfigure]

        ret = layout([[desc], bokeh_objs], sizing_mode='fixed')

        return ret

    def map_figure(self):
        mapped_figure = figure(plot_height=400, plot_width=400, title="Tickets!",
                               x_range=(self.max_long, self.min_long),
                               y_range=(self.min_lat, self.max_lat),
                               background_fill_color=None)

        mapped_figure.toolbar.active_scroll = mapped_figure.tools[1]

        mapped_figure.xgrid.grid_line_color = None
        mapped_figure.ygrid.grid_line_color = None

        return mapped_figure

    #def shapefile_selecter(self):
    #    selecter.on_change('value', lambda attr, old, new: self.update(new))
#
#        return selecter

    def plot_tickets(self):
        fill_color = {'field': 'count', 'transform': self.color_mapper}

        return ticket_circles

    def plot_shapefile(self):
        ret = {}
        self.boundary_lines = mapper_utils.get_boundaries(shapefile_alias)
        opts = dict(xs='xs',
                    ys='ys',
                    source = self.boundary_lines,
                    line_color='red', visible=True)

        boundary_fig = self.mapfigure.multi_line(**opts)

        return boundary_fig

    def heatmap_figure(self):
        fig = figure(plot_height=300, plot_width=750, title="Heatmap!",)
        fig.xgrid.grid_line_color = None
        fig.ygrid.grid_line_color = None

        return fig

    def plot_heatmap(self):
        source = mapper_utils.get_heatmap_tickets()

        fill_color = {'field': 'count', 'transform': self.color_mapper}
        rect = self.heatmapfigure.rect(x='doy', y='year', width=1, height=1, 
                                       fill_color=fill_color, source=source)

        return rect

    def update(self):
        shapefile_val = self.controls['shapefile'].value

tickets_source = mapper_utils.get_tickets()

app = TicketsApp()
tickets_doc = curdoc()

app.plot_tickets()

selecter = Select(title="Boundaries", value="Neighborhoods", options=shapefile_aliases)
controls = [selecter]

for control in controls:
    control.on_change('value', lambda attr, old, new: app.update())

self.mapfigure.circle(x='longitude', y='latitude', source=tickets_source, 
                      size=2.5, fill_color=fill_color, 
                      fill_alpha=.5, line_color='blue')
layout = app.create_layout()
tickets_doc.add_root(layout)
tickets_doc.title = "Parking Tickets!"
#app.plot_heatmap()
#app.plot_shapefile("Neighborhoods")
#show(column(app.mapfigure, *app.mapped_controls))
