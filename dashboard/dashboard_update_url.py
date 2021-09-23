"""This script deal with logic behind updating the dashboard via URL parameter"""
import datetime
from dash import html, dcc, dash_table
from dash.exceptions import PreventUpdate
from strategies_mappers import strategies_parameters, strategies_mapper
from indicators.StockTrades import StockTrades
from indicators.prices_strategies import get_prices_from_our_database


def sanitize_creation_dict(object_creation_dict):
    """This function checks if the object is valid to create a trade model object and change the string inputs to their
    respective formats"""
    mandatory_keys = [
        'ticker',
        'start_date',
        'end_date',
        'strategy'
    ]

    for key in mandatory_keys:
        if key not in object_creation_dict:
            print(key)
            raise ValueError

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
                object_creation_dict[parameter['parameter']] = parameter['conversion'](
                    object_creation_dict[parameter['parameter']])

    except (KeyError, ValueError):
        raise ValueError

    return object_creation_dict


def update_dash_using_url(pathname):
    """This function create a dict with parameters from the URL and create an object """
    if pathname == '/':
        raise PreventUpdate

    object_creation_dict = {}
    for i in pathname[1:].split("$"):
        x = i.split('=')
        object_creation_dict[x[0]] = x[1]

    try:
        object_creation_dict = sanitize_creation_dict(object_creation_dict)
    except ValueError:
        raise PreventUpdate

    model = StockTrades(
        ticker=object_creation_dict['ticker'],
        start_date=object_creation_dict['start_date'],
        end_date=object_creation_dict['end_date'],
        model_parameters=object_creation_dict,
        calculate_trades=strategies_mapper[object_creation_dict['strategy']],
        get_prices=get_prices_from_our_database

    )

    return [
        dcc.Graph(id='price-graph', figure=model.fig_subplots),
        html.Div(
            children=dash_table.DataTable(
                id='trade-summary',
                data=model.summary_trades_table.to_dict('records'),
                columns=[{"name": i, "id": i} for i in model.summary_trades_table.columns],
                style_cell={'textAlign': 'center'}
            )
        )
    ]
