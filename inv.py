import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


h16 = pd.read_stata("H0_2016.dta")
idn16 = h16[(h16.exporter == 'IDN') | (h16.importer == 'IDN')]



# Checking whether the import and export is really equal everywhere
pivcom = idn16.pivot_table(index='commoditycode')
(pivcom.export_value == pivcom.import_value).all()

idn16 = idn16[idn16.exporter == 'IDN']


comnames = pd.read_excel("UN Comtrade Commodity Classifications.xlsx")
comnames = comnames[(comnames.Classification == 'H5')]

idn16 = pd.merge(idn16.loc[:,['exporter', 'importer', 'export_value', 'import_value', 'commoditycode']], comnames.loc[:,['Description', 'Code']], left_on='commoditycode', right_on='Code')
idn16.drop(columns='Code', inplace=True)
idn16 = idn16[idn16.commoditycode != '999999'] # Dropping undefined commodities

# Creating a metric for significant trade relations
idn16['impex'] = abs(idn16.export_value - idn16.import_value) * idn16.loc[:,['export_value', 'import_value']].min(axis=1)


print((abs(idn16.export_value - idn16.import_value) / (idn16.export_value + idn16.import_value)).sort_values())

# (abs(idn16.export_value - idn16.import_value) / (idn16.export_value + idn16.import_value) * (idn16.export_value + idn16.import_value)).sort_values()

impex = idn16.sort_values(by='impex', ascending=False).head(30)

print(impex.loc[:,['export_value', 'import_value']].sum() / idn16.loc[:,['export_value', 'import_value']].sum())

print(impex.importer.value_counts())
print(impex.Description.value_counts())

countries = impex.drop(columns='impex').groupby(by='importer').sum().stack().reset_index()
sns.barplot(data=countries, x='importer', hue='level_1', y=0)
