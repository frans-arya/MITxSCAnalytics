import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("tinyco312.csv")

#change the date column object into date time according to the format python accepts (https://strftime.org/)
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

df = df.dropna(how="any")
df = df.astype({'DB_ID':str,'Unit Sales':int,'SKU':'category','Store':str})

#For Store 312, which month had the largest average sales in dollars for the products from MA Excellent Products?

df_MA = df[(df['SKU']=='8000451112') | (df['SKU']=='7312455520') | (df['SKU']=='8000520021')]

df_MA.groupby(df['Date'].dt.strftime('%B'))['Dollar Sales','Unit Sales'].sum()

#==============================================================================

#For Store 312, which day of the week would you recommend for running a promotion for MA Excellent Products?

df[(df['SKU']=='8000451112') | (df['SKU']=='7312455520') | (df['SKU']=='8000520021')]\
.groupby(df['Date'].dt.strftime('%A'))['Dollar Sales'].sum().sort_values(ascending = True)

#==============================================================================

#For Store 312, how would you characterize the correlation of unit sales per week for the three items from MA Excellent Products?

#first we add columns of SKU names, then as the values well put the unit sales if the SKU matches the SKU names
for sku in df_MA['SKU']:
    df_MA[sku] = df_MA['Unit Sales'][df_MA['SKU'] == sku]

#we then group it by year week, then ask the correlation    
df_MA['YearWeek']= df['Date'].dt.strftime('%Y%U')
df_MA.groupby('YearWeek').sum().corr()

#==============================================================================

skucost = {'8000520021':7.5,'8000451112':9.0,'7312455520':25.0}

costs = []
for sku in df_MA['SKU']:
    for skumap, cost in skucost.items():
        if sku == skumap:
            costs.append(skucost[sku])

df_MA['unitcost'] = costs

df_MA['cost'] = df_MA['unitcost'] * df_MA['Unit Sales']

#For Store 312, which specific week in the data set had the largest sales in dollars for the products from MA Excellent Products?
#Enter your response as YYYYWW, so that if it is the 3rd week of 2015, you would enter 201503

monthly = df_MA.groupby(df['Date'].dt.strftime('%Y%m')).sum()
monthly['profit_margin'] = (monthly['Dollar Sales'] - monthly['cost'])/monthly['cost']
monthly['profit_margin'].sort_values(ascending = False)
