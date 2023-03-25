# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 18:45:24 2023

@author: gusta
"""


import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import dash.dependencies as dd
Input = dd.Input
Output = dd.Output
# Charger les données
df = pd.read_csv('//wsl.localhost/Ubuntu/home/gustave/output.csv', header=None, names=['date', 'time', 'price'], delimiter=',', decimal='.')
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format= '%Y-%m-%d %H:%M:%S')
df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)
df['price'] = df['price'].fillna(method='ffill')
df["variation"] = df["price"].diff()
# Créer une série temporelle
ts = pd.Series(df['price'].values, index=df['datetime'])

def get_color(variation):
    if variation.iloc[-1] < variation.mean():
        return "red"
    else :
        return "green"

# Calculer des statistiques
volatility = round(ts.pct_change().std() * 100, 2)
mean_price = '${:,.2f}'.format(round(ts.mean(), 2))
current_price = '${:,.2f}'.format(round(ts.iloc[-1], 2))
daily_return = round((ts.iloc[-1]-ts.iloc[0])/ts.iloc[0]*100, 2)

# Initialiser l'application Dash
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.Div(children=[
        html.Img(src='https://hpg.com.br/wp-content/uploads/2023/09/GateToken-Vale-A-Pena-2023-Onde-Comprar-1000x600.jpeg', style={'width': '20%'}),
        html.H3(children='Presentation of the Gate Token',style={'text-align': 'center','font-weight': 'bold', 'font-size': '45px','margin-left': '40px','margin-right': '40px'}),      
        html.Table(
            children=[
                html.Tr(
                    children=[
                        html.Td(children=' '),
                        html.Td(children='Performance'),
                    ]
                ),
                html.Tr(
                    children=[
                        html.Td(children='Daily return'),
                        html.Td(children='{:.2f}%'.format(daily_return),style={'color': 'red' if daily_return < 0 else 'green'},id='daily_return')
                    ]
                 ),
                html.Tr(
                    children=[
                        html.Td(children='Volatility'),
                        html.Td(children=f'{volatility}%', style={'color': 'red' if volatility > 10 else 'green'},id='volatility')
                    ]
                ),
                html.Tr(
                    children=[
                        html.Td(children='Mean'),
                        html.Td(children=mean_price,id='mean_price')
                    ]
                ),
            html.Tr(
                children=[
                    html.Td(children='Actual Price'),
                    html.Td(children=current_price,id='actual_price')
                ]
            )
        ]
    ),

    ], style={'display': 'flex'}),

    html.Br(),
    html.Br(),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=ts.index.min().date(),
        end_date=ts.index.max().date(),
        min_date_allowed=ts.index.min().date(),
        max_date_allowed=ts.index.max().date()
        ),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Graph(
        id='graph',
        figure={
            'data': [
                {'x': ts.index, 'y': ts.values, 'type': 'line', 'name': 'Prix', 'line' : {'color': get_color(ts)} }
            ],
            'layout':  go.Layout(
                title='Gate Token',
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white'),
                xaxis=dict(title='Time', titlefont=dict(color='white')),
                yaxis=dict(title='Price', titlefont=dict(color='white')),
            )
            
        }
    ),
    html.H3(children='Evolution of the Price of the Gate Token', style={'text-align': 'center'}),
],style = {'border': '1px solid black', 'width': '90%', 'margin-left': 'auto', 'margin-right': 'auto', 'text-align': 'right', 'background-color': 'black', 'color': 'white', 'padding': '10px', 'height': '1000vh'}
)

# Mettre à jour le graphique en fonction de la plage de dates sélectionnée
@app.callback(
    [Output('graph', 'figure'),
     Output('daily_return', 'children'),
     Output('volatility', 'children'),
     Output('mean_price', 'children'),
     Output('actual_price', 'children')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)

def update_graph(start_date, end_date):
    filtered_ts = ts.loc[start_date:end_date]
    # Calculer des statistiques pour les données filtrées
    volatility = round(filtered_ts.pct_change().std() * 100, 2)
    mean_price = '${:,.2f}'.format(round(filtered_ts.mean(), 2))
    daily_return = round((filtered_ts.iloc[-1] - filtered_ts.iloc[0]) / filtered_ts.iloc[0] * 100, 2)
    current_price = '${:,.2f}'.format(round(filtered_ts.iloc[-1], 2))

    figure = {
        'data': [
            {'x': filtered_ts.index, 'y': filtered_ts.values, 'type': 'line', 'name': 'Prix', 'line': {'color': get_color(filtered_ts)}}
        ],
        'layout': go.Layout(
            title='Gate Token',
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            xaxis=dict(title='Time', titlefont=dict(color='white')),
            yaxis=dict(title='Price', titlefont=dict(color='white')),
        )
    }
    return figure, '{:.2f}%'.format(daily_return), f'{volatility}%', mean_price, current_price


if __name__ == "__main__":
        app.run_server(host="0.0.0.0",port=8050)
