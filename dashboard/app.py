# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from indicators.MovingAverageCross import MovingAverageCross

app = dash.Dash(__name__)

stock_trades = MovingAverageCross(
    ticker='PETR4',
    start_date='2021-01-01',
    end_date='2021-09-01',
    mov_avg_fast=10,
    mov_avg_slow=100
)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=stock_trades.price_graph
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)