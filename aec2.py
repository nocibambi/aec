# Importing libraries
import pandas as pd
import numpy as np

import quandl
quandl.ApiConfig.api_key = "ybsysG4Eemy9AWq9_Kfc"

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
h16 = pd.read_stata("H0_2016.dta")
idn16 = h16[(h16.exporter == 'IDN') | (h16.importer == 'IDN')]

# import matplotlib.pyplot as plt
# import seaborn as sns

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LabelSet, HoverTool
from bokeh.embed import components

# Checking whether the import and export is really equal everywhere
pivcom = idn16.pivot_table(index='commoditycode')
pivcom.export_value == pivcom.import_value
(pivcom.export_value == pivcom.import_value).all()

idn16 = idn16[idn16.exporter == 'IDN']


comnames = pd.read_excel("UN Comtrade Commodity Classifications.xlsx")
comnames = comnames[(comnames.Classification == 'H5')]
idn16 = pd.merge(idn16.loc[:,['exporter', 'importer', 'export_value', 'import_value', 'commoditycode']], comnames.loc[:,['Description', 'Code']], left_on='commoditycode', right_on='Code')
idn16.drop(columns='Code', inplace=True)
idn16 = idn16[idn16.commoditycode != '999999'] # Dropping undefined commodities

# Creating a measure to
idn16['impex'] = abs(idn16.export_value - idn16.import_value) * idn16.loc[:,['export_value', 'import_value']].min(axis=1)



print((abs(idn16.export_value - idn16.import_value) / (idn16.export_value + idn16.import_value)).sort_values())

# (abs(idn16.export_value - idn16.import_value) / (idn16.export_value + idn16.import_value) * (idn16.export_value + idn16.import_value)).sort_values()

impex = idn16.sort_values(by='impex', ascending=False).head(30)

print(impex.loc[:,['export_value', 'import_value']].sum() / idn16.loc[:,['export_value', 'import_value']].sum())

print(impex.importer.value_counts())
print(impex.Description.value_counts())

countries = impex.drop(columns='impex').groupby(by='importer').sum().stack().reset_index()
from flask import Flask, render_template
app = Flask(__name__)

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LabelSet, HoverTool
from bokeh.embed import components

#output_notebook()

# Loading the data
h0 = pd.read_stata("H0_cpy_all.dta")
comnames = pd.read_excel("UN Comtrade Commodity Classifications.xlsx") # from http://unstats.un.org/unsd/tradekb/Attachment439.aspx?AttachmentType=1

# Attributes
# Selecting columns to explore:
h0 = h0.loc[:,['year',
               'exporter',
               'commoditycode',
               'export_value',
               'population',
               'rca',
               'mcp',
               'eci',
               'pci',
               'oppgain',
               'distance',
               'import_value']]

# The attributes of the dataset and its data types:
h0.info()
h0.describe()

# The data contains more than 6M rows.

# Explanation for some of the data created by the Atlas researchers:
# - Distance ('distance'): "The extent of a location's existing capabilities to make the product" based on the products distance to current exports as measured by co-export probabilities.
# - Economic complexity index ('eci'): Country rank base on its export basket's diversification and complexity.
# - Opportunity gain ('oppgai'): How much a location could benefit by deveoping a particular product.
# - Product complexity index ('pci'): "Ranks the diversity and sophistication of productio know-how required to produce a product" based on other number of countries producing that product and their economic complexity.
# - Revealed comparative advantage ('rca'): Whether a country is an 'effective' exporter of a product (i.e. exports more than its 'fair share'). The bigger the value, the more important exporter the country is.
# - Country-Product connection ('mcp'): Marks whether the particular country export the specific product with an `rca` greater than 1. This also allows us to measure country diversity and product ubiquity.

# Example rows
# A row stands for an exporter country-commodity-year summary data.
h0.sample(10)
h0[(h0.commoditycode == '0409') & (h0.exporter == 'FIN')] # The annual summary data for Finland and 'natural honey'

# Missing values
# This is a cleaned dataset and, therefore, there are no missing values.
h0.isna().describe()

# Attribute distributions
# Examining the distributions of the variables:
h0.hist(figsize=(24, 24))

# However, because this is a summary dataset which also tries to be consistent, a number of  attributes contains lots of zero values (e.g. import/export values, rce and mcp). These rows, nevertheless, give information about the country's distance and possible opportunity gain in relation that particular products and therefore we do not drop them.
h0[(h0.export_value == 0) & (h0.import_value == 0)]

# First plot
## Getting the data
comtoexp = h0[(h0.year == 2016)].drop(columns=['year', 'population']).copy()

query = comtoexp[(comtoexp.exporter == 'IDN') & (comtoexp.mcp == 0)]
query.sort_values(by='distance').head()

comnames.head()
comnames = comnames[(comnames.Classification == 'H5')]

query = pd.merge(
                comnames[comnames.isLeaf ==  0].loc[:,['Code',
                                                       'Description']],
                query.loc[:,['commoditycode',
                             'mcp',
                             'distance',
                             'pci',
                             'oppgain']],

                left_on='Code',
                right_on='commoditycode'

                ).drop(columns=['Code', 'commoditycode'])

query = query.sort_values(by='distance').head(30)
query

## Rendering the plot
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
    plot_title = "AEC: 'Product Complexity Index' and 'Opportunity Gain' for Indonesia, 2016."

    return render_template("chart.html", plot_title=plot_title, the_div=div, the_script=script)

## Plot 1
# The graph can help users to identify opportunities for production within a country.
#
# It shows the least 30 least 'distant' but yet not produced prodcuts in a country (in this case, Indonesia). That is, starting to produce them would be relatively easy (in relation to the whole product universe), but nonetheless the country is not an 'effective' exporter of them.
#
# Axes:
# * X: 'Product complexity index': An index showing the relative complexity of that particular product as based on the diversity of countries producing it and the ubiquity of countries these countries make. That is, products with high PCI are typically produced by only a few countries with a wide procuction line.
# * Y: 'Opportunity gain': The degree with which new opporunities emerge to more complex countries when producing that particular product.
#
# Accordingly, the graph can help users to see those product types which are easy to produce, not produced within the country but can lead to novel valuable skills and know-how.

app.run(port=33507)

## Second part
# Loading the data
#h0 = pd.read_stata("H0_cpy_all.dta")

# comnames = pd.read_excel("UN Comtrade Commodity Classifications.xlsx") # from http://unstats.un.org/unsd/tradekb/Attachment439.aspx?AttachmentType=1
# comnames = comnames[(comnames.Classification == 'H5')]

ucom_codes = pd.read_csv('UCOM-datasets-codes.csv') # https://www.quandl.com/data/UCOM-United-Nations-Commodity-Trade/usage/export

# Identifying the most effective export products of a country with high opportunity value
comtoexp = h0[(h0.year == 2016)].drop(columns=['year', 'population']).copy()
comtoexp[
    (comtoexp.exporter == 'IDN')
    & (comtoexp.oppgain != 0)].sort_values(by='rca', ascending=False).head(30).sort_values(by='oppgain', ascending=False)

comnames[comnames.Code == str(3906)] # Identifying the product with the highest opportunity value
comnames[comnames.Code == str(39)] # Identifying the product group into which it belongs

# Acquiring trading data for that product type
# plas_query = ucom_codes[ucom_codes.iloc[:,0].str[5:-4] == 'PLAS'].iloc[:,0]
#
# plas_dat = pd.DataFrame()
#
# for i in range(len(plas_query)):
#     countrycode = plas_query.iloc[i]
#     row = quandl.get(countrycode, start_date='2016-12-31', end_date='2016-12-31')
#
#     if plas_dat.shape == (0,0):
#         plas_dat=pd.DataFrame(row)
#
#     else:
#         plas_dat = plas_dat.append(row)
#
# plas_dat.to_csv("plas_dat.csv", index=False)
plas_dat = pd.read_csv("plas_dat.csv")

# We focus only on the simple import values
imp_cols = (plas_dat.columns.str[-20:] == 'Import - Trade (USD)') & (plas_dat.columns.str[-23:] != 'Re-Import - Trade (USD)')
imp_dat = plas_dat.loc[:,imp_cols].dropna(how='all')
imp_dat.head()

# From among them we pick the top decile of the products based on their total import values
top_imp = imp_dat.sum().sort_values(ascending=False)
top_imp = top_imp[top_imp >= top_imp.quantile(q=0.90)].index

impcors = imp_dat.loc[:,imp_dat.columns.isin(top_imp)]
impcors.columns = impcors.columns.str[:-23]
impcors = impcors.corr()
impcors.head()


## Plot2
# The graph shows the correlations from different countries between overal imports within a significatn product group.
#
# For this, first we identified those products which
# 1. belong to the top 30 effective export products of the country (we continued to work with Indonesia),
# 2. had the highest opporunity gain value from among them,
#
# After that, we accessed the UN Comtrade data API through Quandl and downloaded all trade data related to that wider product group (in this case Plastics). Based on this, we calculated correlations between the the top 10% of imported products based on their import value.
#
# The workflow and graph can help those who are interested in producing a particular product type with significant opporunity gain. For them it shows those products from the same product group, which are also imported into the same countries as the original and shows their close relationship with other products based on their main import destinations. This allows users to shift their production line gainfully while still staying at the same geogprhically market. This graph and data can also provide a good picture of the country in terms of its opportunity- and production-related co-optations and the possible efficiency gaps in terms of its international economic relations.

plt.figure(figsize=(24,24))
sns.heatmap(impcors, xticklabels=True, yticklabels=True, cmap='mako_r', annot=True, cbar=False)
