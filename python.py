# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 10:00:56 2023

@author: gusta
"""

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# Lecture du fichier CSV
df = pd.read_csv('/home/gustave/output.csv', header=None, names=['date', 'time', 'price'], delimiter=';', decimal='.')

# Concaténation de la colonne date et de la colonne time pour créer une colonne datetime
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%Y %H:%M:%S')

# Conversion de la colonne price en float
df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)

# Création de la time series
ts = pd.Series(df['price'].values, index=df['datetime'])

# Calcul de la volatilité, de la moyenne, du premier prix, du dernier prix et du prix actuel
volatility = round(ts.pct_change().std() * 100, 2)
mean_price = '${:,.2f}'.format(round(ts.mean(), 2))
first_price = '${:,.2f}'.format(round(ts.iloc[0], 2))
last_price = '${:,.2f}'.format(round(ts.iloc[-1], 2))
current_price = '${:,.2f}'.format(round(ts.iloc[-1], 2))

# Création de l'application Dash
app = dash.Dash(__name__)

# Création de la mise en page de l'application
app.layout = html.Div(children=[
    html.H1(children='Price of Gate Token'),

    dcc.Graph(
        id='graph',
        figure={
            'data': [
                {'x': ts.index, 'y': ts.values, 'type': 'line', 'name': 'Prix'}
            ],
            'layout': {
                'title': 'Gate Token'
            }
        }
    ),

    html.H3(children='Informations sur le Gate Token'),
    html.Table(
        children=[
            html.Tr(
                children=[
                    html.Td(children='Volatilité'),
                    html.Td(children=f'{volatility}%')
                ]
            ),
            html.Tr(
                children=[
                    html.Td(children='Moyenne'),
                    html.Td(children=mean_price)
                ]
            ),
            html.Tr(
                children=[
                    html.Td(children='Premier prix'),
                    html.Td(children=first_price)
                ]
            ),
            html.Tr(
                children=[
                    html.Td(children='Dernier prix'),
                    html.Td(children=last_price)
                ]
            ),
            html.Tr(
                children=[
                    html.Td(children='Prix actuel'),
                    html.Td(children=current_price)
                ]
            )
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)



