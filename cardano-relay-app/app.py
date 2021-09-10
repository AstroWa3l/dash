# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import json
import time
import requests
import math as m
import matplotlib.pyplot as plt
import numpy as np
import descartes
import geopandas as gpd

#import relay data
file = open('relay_info.json')
data = json.load(file)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Make the dataframe from the json file

df1 = pd.DataFrame()
for i in range(len(data)):
    df1 = df1.append(pd.DataFrame(data[i]['relays']), sort=True)

df1.dropna(inplace=True)
df1.sort_values(by=['countryCode'], inplace=True)

#Create new df2 and then us only df2 to create the map
df2 = df1.copy()
df2.set_index('country', inplace=True)
df_us = df2[df2.countryCode == 'US']
df_us.sort_values(by=['region'], inplace=True)

df_us_region = df_us['region'].value_counts().to_frame()
df_us_region['State'] = df_us_region.index
df_us_region.rename(columns = {'region':'Relay Count'}, inplace = True)


# fig = px.choropleth(locations=df_us_region['State'], locationmode="USA-states", color=df_us_region['Relay Count'], scope="usa", labels={'color':'Relay Count'})
# Plotly Express
fig = px.choropleth(
    data_frame=df_us_region,
    locationmode='USA-states',
    locations='State',
    scope="usa",
    color='Relay Count',
    hover_data=['State', 'Relay Count'],
    color_continuous_scale=px.colors.sequential.Plasma,
    )


app.layout = html.Div([
    dcc.Graph(
        id='USA Relay Distribution',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)