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


file = open('relay_info.json')
data = json.load(file)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df1 = pd.DataFrame()
for i in range(len(data)):
    df1 = df1.append(pd.DataFrame(data[i]['relays']), sort=True)

df1.dropna(inplace=True)
df1.sort_values(by=['countryCode'], inplace=True)

df1.set_index('country', inplace=True)
df_us = df1[df1.countryCode == 'US']
df_us.sort_values(by=['region'], inplace=True)

df_us_region = df_us['regionName'].value_counts().to_frame()
df_us_region['State'] = df_us_region.index
df_us_region.rename(columns = {'regionName':'Relay Count'}, inplace = True)


fig = px.bar(df_us_region, x='State', y="Relay Count", color="Relay Count", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Relay Information',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)