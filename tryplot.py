import pandas as pd
import numpy as np

from flask import Flask, render_template
app = Flask(__name__)

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, LabelSet, HoverTool


query = pd.read_csv("plot1_data.csv")

# print("\nquery.head():\n{}".format(query.head()))
## Rendering the plot
source = ColumnDataSource(data=dict(names = list(query.Description),
                                    opg=query.oppgain,
                                    pci=query.pci,
                                    dist=query.distance))


hover = HoverTool(tooltips=[("Desc", "@names"),
                            ("PCI", "$x"),
                            ("Oppgain", "$y"),
                            ("Distance", "@dist")],
                  formatters={'@names' : 'printf',},)


# p = figure(plot_width = 600,
#            plot_height = 600,
#            tools=['pan', hover,'zoom_out', 'zoom_in', 'reset']) #

p = figure()


p.scatter(x = 'pci',
          y = 'opg',
          size = 15,
          color = 'indigo',
          alpha = 0.6,
          source = source)

p.xaxis.axis_label = 'Product Complexity Index'
p.yaxis.axis_label = 'Opportunity Gain'

show(p)
