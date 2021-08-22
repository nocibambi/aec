# Project proposal: Atlas of Economic Complexity
## Motivation
Economic trade and technological development are perhaps the most robust causes of socio-economic dynamics and the global distribution, organization and movement of commodities, technologies and productibility power. Businesses, especially if they intend to sustain and grow in the long term and especially on the global level, can make good use of this kind of information (see the 'Business uses' section below).

The data source I propose is the data behind the Atlas of Economic Complexity drawing on the UN's Comtrade database. The Atlas is primarily a visualization tool which allows people to learn about countries' economic structure and complexity. In order, however, to create it, the researchers behind it had to clean and further standardize it and to render a number of measures regarding the complexity of interchanges. This both makes preliminary analysis easier and can provide already useful insights for a possible further analysis.

## Data
The data shows import/export values for product group/country/year combinations. It does not cover services (Although the UN Comtrade database separately collects some of it too).

### Dataset groups
The dataset is groped along the following dimensions:
1. Detail:
    1. Country-Product-Year ('CPY'): Exported product groups and their values by countries. It also includes the additional attributes generated by the Atlas researchers (discussed at data description)
    2. 'CCPY': More detailed breakdown of product destination.
2. Standardization:
    1. Harmonized System ('H0'): More detailed list of products, but is available only from 1995.
    2. Standardized International Trade Classification, Revision 2 ('S2'): Less detailed but available from 1962.

### Specifications
* Size: The Harmonized Standardization (H0) data tables are almost 7GB, the S2 tables are more than 4GB.
* Format: The tables are in STATA format, which python pandas can handle well with the `pd.read_stata()` function.

During the exploratory data analysis, I focused only on the Harmonized System (H0) data and first only on the summarized (CPY) tables also containing the generated attributes. The columns of the two datasets

H0_2016.dta columns (i.e. data for 2016):
* year: int16
* exporter: object
* importer: object
* commoditycode: object
* export_value: float32
* quantity: float32
* code_unit: float64
* import_value: float32

H0_cpy_all.dta columns (attributes marked with '*' are generated data by the Atlas researchers explained below):
* year: int16
* exporter: objectx
* commoditycode: object
* inatlas: int8
* export_value: float32
* population: float32
* rca*: float32
* rpop*: float32
* mcp*: int8
* eci*: float32
* pci*: float32
* oppval*: float32
* oppgain*: float32
* distance*: float32
* import_value: float64

### Atlas-specific features
The Atlas data's differences from the United States public Comtrade database:
- The Atlas is cleaned for reporting inconsistencies.
- It uses only a four-digit product classification (instead of the Comtrade's six or more digit level).
- Attributes created by the Atlas researchers:
    - Distance (`distance`): "The extent of a location's existing capabilities to make the product" based on the products distance to current exports as measured by co-export probabilities.
    - Economic complexity index (`eci`): Country rank base on its export basket's diversification and complexity.
    - Complexity Outlook Index (`oppval`): "A measure of how many complex products are near (to) a country’s current set of productive capabilities"
    - Opportunity gain (`oppgai`): How much a location could benefit from developing a particular product.
    - Product complexity index (`pci`): "Ranks the diversity and sophistication of production know-how required to produce a product" based on the other number of countries producing that product and their economic complexity.
    - Revealed comparative advantage (`rca`): Whether a country is an 'effective' exporter of a product (i.e. exports more than its 'fair share`). The bigger the value, the more important exporter the country is.
    - Per capita export intensity (`rpop`): An alternative measure of export intensity. The ratio of exports per capita of a country-product over the exports per capita of that product in the world.
    - Country-Product connection (`mcp`): Marks whether the particular country exports the specific product with an `rca` greater than 1. This also allows us to measure country diversity and product ubiquity.


### UN Comtrade
Because of the Atlas' reliance on the UN Comtrade data, it is important to highlight its methodological attributes:
* Commodity values are in US dollars
* Quantities are in metric units
* Commodities are reported in the most recent classification (HS2012)
* Information about the [Harmonized System](https://unstats.un.org/unsd/tradekb/Knowledgebase/50018/Harmonized-Commodity-Description-and-Coding-Systems-HS)
* [Product type codes and descriptions](http://unstats.un.org/unsd/tradekb/Attachment439.aspx?AttachmentType=1)
* [Comtrade country codes](https://unstats.un.org/unsd/tradekb/Knowledgebase/Comtrade-Country-Code-and-Name)
* [More details about the Comtrade](https://unstats.un.org/unsd/tradekb/Default.aspx)

#### Data API
The UN Comtrade data can be accessed most easier through quandl which provides easy access to country/product type pairs time series data:

```py
import quandl
silk_canada = quandl.get("UCOM/SILK_CAN")
```
* Country and product type codes are behind the [following link](https://www.quandl.com/data/UCOM-United-Nations-Commodity-Trade/documentation/data-organization).
* Besides, the UN also provides its own data API service based on the SDMX standard (https://comtrade.un.org/data/dev/portal).

## Business value
The research group behind the Atlas published the cleaned data set only relatively recently, and most of their publications so far has been about country-level economic development and much less about direct business usability. Compared to contemporary unstructured data this set also benefits from its relatively broad geographic coverage and historical continuity.

### Possible business uses
- Companies interested in the technological and infrastructural requirements of local opportunities and global expansion.
- Production companies would like to gain an overview of their supply chain possibilities.
- Investors interested in the growth possibilities and the interrelationship between production sectors and national economies.
- HR specialists, educators creating long-term training plans or learners seeking to acquiring new skills for long-term and geographically specific usefulness.
- Governmental and international institutions interested in trade and economic policy and technological trends.

# Plots
## [1st Plot](https://floating-shore-10682.herokuapp.com/)

The graph helps users to identify production opportunities within a country.

It shows the 30 least 'distant' but yet not produced products in a country (in this case, Indonesia). That is, starting to produce them would be relatively easy (in relation to the whole product universe), but nonetheless, the country is not an 'effective' exporter of them.

Axes:
* X: 'Product complexity index': An index showing the relative complexity of that particular product as based on the diversity of countries producing it and the ubiquity of countries these countries make. That is, products with high PCI are typically produced by only a few countries with a wide product line.
* Y: 'Opportunity gain': The degree with which new opportunities emerge to more complex countries when producing that particular product.

Accordingly, the graph can help users to see those product types which are
1. easy to produce,
2. not produced within the country and
3. can lead to novel valuable skills and know-how.

## [2nd Plot](https://nbviewer.jupyter.org/github/nocibambi/aec/blob/master/2nd%20plot.ipynb)
The graph shows the correlations from different countries between overal imports within a significatn product group.

For this, first we identified those products which
1. belong to the top 30 effective export products of the country (we continued to work with Indonesia),
2. had the highest opporunity gain value from among them,

After that, we accessed the UN Comtrade data API through Quandl and downloaded all trade data related to that wider product group (in this case Plastics). Based on this, we calculated correlations between the the top 10% of imported products based on their import value.

The workflow and graph can help those who are interested in producing a particular product type with significant opporunity gain. For them it shows those products from the same product group, which are also imported into the same countries as the original and shows their close relationship with other products based on their main import destinations. This allows users to shift their production line gainfully while still staying at the same geogprhically market. This graph and data can also provide a good picture of the country in terms of its opportunity- and production-related co-optations and the possible efficiency gaps in terms of its international economic relations.

