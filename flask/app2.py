from flask import Flask, render_template

from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid, Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
# from bokeh.charts import Bar
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource

import random

app = Flask(__name__)

# A flask application which defines the chart function
@app.route ( "/<int:bars_count>/" )
def chart ( bars_count ):
    if bars_count <= 0 :
        bars_count = 1
    data = { "days" : [], "bugs" : [], "costs" : []}

    for i in range ( 1 , bars_count + 1 ):
        data['days'].append(i )
        data['bugs'].append(random . randint ( 1 , 100 ))
        data['costs'].append(random . uniform ( 1.00 , 1000.00 ))

    hover = create_hover_tool ()

    plot = create_bar_chart ( data , "Bugs found per day" , "days" , "bugs" , hover )
    script , div = components ( plot )

    return render_template ( "chart.html" , bars_count = bars_count , the_div = div , the_script = script )


def create_hover_tool():
    return None

def create_bar_chart(data, title, x_name, y_name, hover_tool=None, width=1200, height=300):
    """Creates a bar chart plot, uses centcom dashboard styling.
    Parameters:
    - data, dict
    - title, str
    - names of x and y axes, str
    - hover tool, html"""
    source = ColumnDataSource(data) # Gets the data for the plot
    # From the data gets the axis names
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0, end=max(data[y_name]) * 1.5)

    tools = []

    if hover_tool: # turns on the over tool if exists
        tools = [hover_tool,]

    # Defines the plot main figure
    plot = figure(title=title,
                  x_range=xdr, # value ranges
                  y_range=ydr,
                  plot_width=width,
                  plot_height=height,
                  h_symmetry=False,
                  v_symmetry=False,
                  min_borders=0,
                  toolbar_location="above",
                  tools=tools,
                  responsive=True,
                  outline_line_color="#666666")

    # Defines the plot's shape as a vertical bar and sets its parameters
    glyph = VBar(x=x_name,
                 top=y_name,
                 bottom=0,
                 width=.8,
                 fill_color="#e12127")

    # Adds the glyph to the plot with the data
    plot.add_glyph(source, glyph)

    # Defines the x, y axes
    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0

    plot.xaxis.axis_label = "Days after app deployment"
    plot.yaxis.axis_label = "Bugs found"

    plot.xaxis.major_label_orientation = 1

    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.ygrid.grid_line_alpha = 0.1

    return plot

# Allow to run this application on the localhost in debug mode
if __name__ == "__main__":
    app.run(debug=True) # do not use debug mode outised testing
