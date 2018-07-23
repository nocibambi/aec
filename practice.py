import pandas as pd

from flask import Flask, render_template
app = Flask(__name__)

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, LabelSet, HoverTool


@app.route("/")
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
    # port=33507
    # app(foo, p) # do not use debug mode outised testing
