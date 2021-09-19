# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output, State
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

    html.Div(
        id='mov-avg-cross-parameters',
        children=[
            html.Label(
              children='Média Móvel Curta'
            ),

            dcc.Input(
                id='mov-avg-fast',
                type="number",
                min=1,
                max=365,
                step=1,
                value=10,
            ),

            html.Label(
                children='Média Móvel Longa'
            ),

            dcc.Input(
                id='mov-avg-slow',
                type="number",
                min=1,
                max=365,
                step=1,
                value=60,
            )
        ],
        style={'display': 'block'}
    ),

    html.Div(
        id='bollinger-bands-parameters',
        children=[
            html.Label(
                children='Média Móvel Centro'
            ),

            dcc.Input(
                id='bollinger-mov-avg',
                type="number",
                min=1,
                max=365,
                step=1,
                value=14,
            ),

            html.Label(
                children='Desvio Padrão'
            ),

            dcc.Input(
                id='bollinger-std',
                type="number",
                min=0.1,
                max=4,
                step=0.1,
                value=2,
            ),

            html.Label(
                children='Período Desvio Padrão'
            ),

            dcc.Input(
                id='bollinger-std-period',
                type="number",
                min=2,
                max=365,
                step=1,
                value=20,
            )
        ],
        style={'display': 'none'}
    ),

    html.Button('Atualizar', id='update-button', n_clicks=0),

    dcc.Graph(id='price-graph'),

    dcc.Graph(id='profit-and-loss-graph'),

    dcc.Graph(id='indicators-graph'),

    html.Div(
        children=dash_table.DataTable(
            id='trade-summary',
            data=[]
        )
    )
])


@app.callback(
    Output('mov-avg-cross-parameters', 'style'),
    Output('bollinger-bands-parameters', 'style'),
    Input('trading-indicators', 'value')
)
def change_visibility_models_parameters(trading_strategy):
    if trading_strategy == 'Moving Average Cross':
        mov_avg = {'display': 'block'}
        bollinger = {'display': 'none'}
    elif trading_strategy == 'Bollinger Bands':
        mov_avg = {'display': 'none'}
        bollinger = {'display': 'block'}

    return mov_avg, bollinger


@app.callback(
    Output('price-graph', 'figure'),
    Output('profit-and-loss-graph', 'figure'),
    Output('indicators-graph', 'figure'),
    Output('trade-summary', 'data'),
    Output('trade-summary', 'columns'),
    Input('update-button', 'n_clicks'),
    State('trading-indicators', 'value'),
    State('mov-avg-fast', 'value'),
    State('mov-avg-slow', 'value'),
    State('bollinger-mov-avg', 'value'),
    State('bollinger-std', 'value'),
    State('bollinger-std-period', 'value')
)
def update(
    n_clicks,
    trading_strategy,
    mov_avg_fast,
    mov_avg_slow,
    bollinger_mov_avg,
    bollinger_std,
    bollinger_std_period
):
    if trading_strategy == 'Moving Average Cross':
        model = MovingAverageCross(
            ticker='PETR4',
            start_date='2021-01-01',
            end_date='2021-09-01',
            mov_avg_fast=mov_avg_fast,
            mov_avg_slow=mov_avg_slow
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
            bands_mov_avg_period=bollinger_mov_avg,
            bands_std=bollinger_std,
            band_std_period=bollinger_std_period,
        )

    return \
        model.price_graph, \
        model.profit_and_loss_graph, \
        model.indicators_graph, \
        model.summary_trades_table.to_dict('records'), \
        [{"name": i, "id": i} for i in model.summary_trades_table.columns]


if __name__ == '__main__':
    app.run_server(debug=True)