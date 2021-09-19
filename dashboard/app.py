# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import locale
import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output, State
from indicators.StockTrades import StockTrades
from indicators.model_strategies import calculate_trades_bollinger_bands, calculate_trades_moving_average_cross, \
    calculate_trades_rsi

locale.setlocale(locale.LC_ALL, 'pt_BR')

app = dash.Dash(__name__)

available_indicators = [
    'Cruzamento Média Móvel',
    #'Relative Strength Index',
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
        style={'display': 'flex', 'flex-direction': 'column'}
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
        style={'display': 'none', 'flex-direction': 'column'}
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
    if trading_strategy == 'Cruzamento Média Móvel':
        mov_avg = {'display': 'flex'}
        bollinger = {'display': 'none'}
    elif trading_strategy == 'Bollinger Bands':
        mov_avg = {'display': 'none'}
        bollinger = {'display': 'flex'}

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
    strategies_mapper = {
        'Cruzamento Média Móvel': calculate_trades_moving_average_cross,
        'Bollinger Bands': calculate_trades_bollinger_bands,
        'Relative Strength Index': calculate_trades_rsi
    }

    model_parameters = {
        'mov_avg_fast': mov_avg_fast,
        'mov_avg_slow': mov_avg_slow,
        'bollinger_mov_avg': bollinger_mov_avg,
        'bollinger_std': bollinger_std,
        'bollinger_std_period': bollinger_std_period
    }

    model = StockTrades(
        ticker='PETR4',
        start_date='2021-01-01',
        end_date='2021-09-01',
        model_parameters=model_parameters,
        calculate_trades=strategies_mapper[trading_strategy]
    )

    return \
        model.price_graph, \
        model.profit_and_loss_graph, \
        model.indicators_graph, \
        model.summary_trades_table.to_dict('records'), \
        [{"name": i, "id": i} for i in model.summary_trades_table.columns]


if __name__ == '__main__':
    app.run_server(debug=True)