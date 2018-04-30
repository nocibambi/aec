# Atlas of economic coplexity EDA

# Importing packages
import pandas as pd

#h0 = pd.read_stata("H0_cpy_all.dta")
#s2 = pd.read_stata("S2_final_cpy_all.dta")

h2016 = pd.read_stata("H0_2016.dta")

print(h0.info())
h0.describe()
