# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output
from indicators.MovingAverageCross import MovingAverageCross
from indicators.BollingerBands import BollingerBands

app = dash.Dash(__name__)

available_indicators = [
    'Moving Average Cross',
    'Relative Strength Index',
    'Bollinger Bands'
]


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Dropdown(
        id='trading-indicators',
        options=[{'label': i, 'value': i} for i in available_indicators],
        value=available_indicators[0]
    ),

    dcc.Graph(
        id='price-graph'
    ),

    dcc.Graph(
        id='profit-and-loss-graph'
    ),

    dcc.Graph(
        id='indicators-graph'
    ),

    html.Div(
        children=dash_table.DataTable(
            id='trade-summary',
            data=[]
        )
    )
])


@app.callback(
    Output('price-graph', 'figure'),
    Output('profit-and-loss-graph', 'figure'),
    Output('indicators-graph', 'figure'),
    Output('trade-summary', 'data'),
    Output('trade-summary', 'columns'),
    Input('trading-indicators', 'value')
)
def update(trading_strategy):
    if trading_strategy == 'Moving Average Cross':
        model = MovingAverageCross(
            ticker='PETR4',
            start_date='2021-01-01',
            end_date='2021-09-01',
            mov_avg_fast=10,
            mov_avg_slow=100
        )
    elif trading_strategy == 'Relative Strength Index':
        model = MovingAverageCross(
            ticker='PETR4',
            start_date='2021-01-01',
            end_date='2021-09-01',
            mov_avg_fast=10,
            mov_avg_slow=100
        )
    elif trading_strategy == 'Bollinger Bands':
        model = BollingerBands(
            ticker='PETR4',
            start_date='2021-01-01',
            end_date='2021-09-01',
            bands_mov_avg_period=14,
            bands_std=2,
            band_std_period=20,
        )

    return \
        model.price_graph, \
        model.profit_and_loss_graph, \
        model.indicators_graph, \
        model.summary_trades_table.to_dict('records'), \
        [{"name": i, "id": i} for i in model.summary_trades_table.columns]


if __name__ == '__main__':
    app.run_server(debug=True)