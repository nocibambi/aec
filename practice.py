import pandas as pd
import numpy as np

from flask import Flask, render_template
app = Flask(__name__)

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, LabelSet, HoverTool

# # Loading the data
# h0 = pd.read_stata("H0_cpy_all.dta")
# comnames = pd.read_excel("UN Comtrade Commodity Classifications.xlsx") # from http://unstats.un.org/unsd/tradekb/Attachment439.aspx?AttachmentType=1
#
# # Attributes
# # Selecting columns to explore:
# h0 = h0.loc[:,['year',
#                'exporter',
#                'commoditycode',
#                'export_value',
#                'population',
#                'rca',
#                'mcp',
#                'eci',
#                'pci',
#                'oppgain',
#                'distance',
#                'import_value']]
#

# # First plot
# ## Getting the data
# comtoexp = h0[(h0.year == 2016)].drop(columns=['year', 'population']).copy()
#
# query = comtoexp[(comtoexp.exporter == 'IDN') & (comtoexp.mcp == 0)]
# query.sort_values(by='distance').head()
#
# comnames.head()
# comnames = comnames[(comnames.Classification == 'H5')]
#
# query = pd.merge(comnames[comnames.isLeaf ==  0].loc[:,['Code','Description']],
#                  query.loc[:,['commoditycode',
#                              'mcp',
#                              'distance',
#                              'pci',
#                              'oppgain']],
#                  left_on='Code',
#                  right_on='commoditycode').drop(columns=['Code', 'commoditycode'])
#
# query = query.sort_values(by='distance').head(30)
#
# query.to_csv("plot1_data.csv", index=False)


@app.route("//")
def chart():
    query = pd.read_csv("plot1_data.csv")
    ## Rendering the plot
    source = ColumnDataSource(data=dict(names = list(query.Description),
                                        opg=query.oppgain,
                                        pci=query.pci,
                                        dist=query.distance))

    hover = HoverTool(tooltips=[("Desc", "@names"),
                                ("PCI", "$x"),
                                ("Oppgain", "$y"),
                                ("Distance", "@dist")],
                      formatters={'@names' : 'printf',})

    p = figure(plot_width = 600,
               plot_height = 600,
               tools=['pan', hover, 'zoom_out', 'zoom_in', 'reset'])

    p.scatter(x = 'pci',
              y = 'opg',
              size = 15,
              color = 'indigo',
              alpha = 0.6,
              source = source)

    p.xaxis.axis_label = 'Product Complexity Index'
    p.yaxis.axis_label = 'Opportunity Gain'

    script, div = components(p)
    plot_title = "The first plot generated from the data."

    return render_template("chart.html", plot_title=plot_title, the_div=div, the_script=script) # Uses a template from the Jinja2 engine to output html

# Allow to run this application on the localhost in debug mode
if __name__ == "__main__":
    app.run(port=33507) # debug=True,  do not use debug mode outised testing
    # app(foo, p) # do not use debug mode outised testing
