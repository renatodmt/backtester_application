import datetime
from dash import dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from main import app
from indicators.StockTrades import StockTrades
from indicators.model_strategies import calculate_trades_bollinger_bands, calculate_trades_moving_average_cross, \
    calculate_trades_rsi

strategies_parameters = [
    {'strategy': 'mov_avg', 'parameter': 'mov_avg_fast', 'conversion': int},
    {'strategy': 'mov_avg', 'parameter': 'mov_avg_slow', 'conversion': int},
    {'strategy': 'bb', 'parameter': 'bollinger_std', 'conversion': float},
    {'strategy': 'bb', 'parameter': 'bollinger_std_period', 'conversion': int},
    {'strategy': 'bb', 'parameter': 'bollinger_mov_avg', 'conversion': int}
]

def sanitize_creation_dict(object_creation_dict):
    mandatory_keys = [
        'ticker',
        'start_date',
        'end_date',
        'strategy'
    ]

    for key in mandatory_keys:
        if key not in object_creation_dict:
            print(key)
            raise PreventUpdate

    try:
        object_creation_dict['start_date'] = datetime.datetime.strptime(
            object_creation_dict['start_date'],
            '%Y-%m-%d'
        )
        object_creation_dict['end_date'] = datetime.datetime.strptime(
            object_creation_dict['end_date'],
            '%Y-%m-%d'
        )

        for parameter in strategies_parameters:
            if object_creation_dict['strategy'] == parameter['strategy']:
                object_creation_dict[parameter['parameter']] = parameter['conversion'](object_creation_dict[parameter['parameter']])

    except (KeyError, ValueError):
        raise PreventUpdate

    return object_creation_dict


@app.callback(
    Output('price-graph', 'figure'),
    Output('profit-and-loss-graph', 'figure'),
    Output('indicators-graph', 'figure'),
    Output('trade-summary', 'data'),
    Output('trade-summary', 'columns'),
    Output('url', 'pathname'),
    Input('update-button', 'n_clicks'),
    Input('url', 'pathname'),
    State('trading-indicators', 'value'),
    State('mov-avg-fast', 'value'),
    State('mov-avg-slow', 'value'),
    State('bollinger-mov-avg', 'value'),
    State('bollinger-std', 'value'),
    State('bollinger-std-period', 'value')
)
def update_figures(
    n_clicks,
    pathname,
    trading_strategy,
    mov_avg_fast,
    mov_avg_slow,
    bollinger_mov_avg,
    bollinger_std,
    bollinger_std_period
):
    if callback_context.triggered[0]['prop_id'] == 'url.pathname':
        if pathname == '/':
            raise PreventUpdate
        else:
            return figure_updater_url_route(pathname)

    if n_clicks == 0:
        raise PreventUpdate
    else:
        return figure_updater_button(
            trading_strategy=trading_strategy,
            mov_avg_fast=mov_avg_fast,
            mov_avg_slow=mov_avg_slow,
            bollinger_mov_avg=bollinger_mov_avg,
            bollinger_std=bollinger_std,
            bollinger_std_period=bollinger_std_period
        )


def figure_updater_url_route(pathname):
    strategies_mapper = {
        'mov_avg': calculate_trades_moving_average_cross,
        'bb': calculate_trades_bollinger_bands,
        'rsi': calculate_trades_rsi
    }

    object_creation_dict = {}
    for i in pathname[1:].split("$"):
        x = i.split('=')
        object_creation_dict[x[0]] = x[1]

    object_creation_dict = sanitize_creation_dict(object_creation_dict)

    model = StockTrades(
        ticker=object_creation_dict['ticker'],
        start_date=object_creation_dict['start_date'],
        end_date=object_creation_dict['end_date'],
        model_parameters=object_creation_dict,
        calculate_trades=strategies_mapper[object_creation_dict['strategy']]
    )

    return \
        model.price_graph, \
        model.profit_and_loss_graph, \
        model.indicators_graph, \
        model.summary_trades_table.to_dict('records'), \
        [{"name": i, "id": i} for i in model.summary_trades_table.columns],\
        pathname


def figure_updater_button(
    trading_strategy,
    mov_avg_fast,
    mov_avg_slow,
    bollinger_mov_avg,
    bollinger_std,
    bollinger_std_period
):
    strategies_mapper = {
        'mov_avg': calculate_trades_moving_average_cross,
        'bb': calculate_trades_bollinger_bands
    }

    model_parameters = {
        'mov_avg_fast': mov_avg_fast,
        'mov_avg_slow': mov_avg_slow,
        'bollinger_mov_avg': bollinger_mov_avg,
        'bollinger_std': bollinger_std,
        'bollinger_std_period': bollinger_std_period
    }

    #Placeholder for ticker, start_date and end_date. They will come from the UI after.
    ticker = 'petr4'
    start_date = '2020-01-01'
    end_date = '2021-01-01'

    model = StockTrades(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        model_parameters=model_parameters,
        calculate_trades=strategies_mapper[trading_strategy]
    )

    pathname = f'/ticker={ticker}$start_date={start_date}$end_date={end_date}$strategy={trading_strategy}'
    for parameter in strategies_parameters:
        if trading_strategy == parameter['strategy']:
            pathname += f"${parameter['parameter']}={model_parameters[parameter['parameter']]}"

    return \
        model.price_graph, \
        model.profit_and_loss_graph, \
        model.indicators_graph, \
        model.summary_trades_table.to_dict('records'), \
        [{"name": i, "id": i} for i in model.summary_trades_table.columns],\
        pathname


figures_component = html.Div(children=[
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
