"""This file contain the callbacks that updates the dashboard."""
from dash import Output, Input, State, callback_context
from dash.exceptions import PreventUpdate
from main import app
from dashboard_update_url import update_dash_using_url
from dashboard_update_button import update_dash_using_button
from strategies_mappers import strategies_parameters


@app.callback(
    Output('update-button', 'disabled'),
    Input('update-button', 'n_clicks'),
    Input('trading-indicators', 'value'),
    Input('mov-avg-fast', 'value'),
    Input('mov-avg-slow', 'value'),
    Input('bollinger-mov-avg', 'value'),
    Input('bollinger-std', 'value'),
    Input('bollinger-std-period', 'value')
)
def change_button_status(
    n_clicks,
    trading_strategy,
    mov_avg_fast,
    mov_avg_slow,
    bollinger_mov_avg,
    bollinger_std,
    bollinger_std_period
):
    if callback_context.triggered[0]['prop_id'] == 'update-button.n_clicks':
        if n_clicks > 0:
            return True
    else:
        return False


@app.callback(
    Output('url', 'pathname'),
    Input('update-button', 'n_clicks'),
    State('trading-indicators', 'value'),
    State('mov-avg-fast', 'value'),
    State('mov-avg-slow', 'value'),
    State('bollinger-mov-avg', 'value'),
    State('bollinger-std', 'value'),
    State('bollinger-std-period', 'value')
)
def update_url(
    n_clicks,
    trading_strategy,
    mov_avg_fast,
    mov_avg_slow,
    bollinger_mov_avg,
    bollinger_std,
    bollinger_std_period
):
    if n_clicks == 0:
        raise PreventUpdate

    # Placeholder for ticker, start_date and end_date. They will come from the UI after.
    ticker = 'petr4'
    start_date = '2020-01-01'
    end_date = '2021-01-01'

    model_parameters = {
        'mov_avg_fast': mov_avg_fast,
        'mov_avg_slow': mov_avg_slow,
        'bollinger_mov_avg': bollinger_mov_avg,
        'bollinger_std': bollinger_std,
        'bollinger_std_period': bollinger_std_period
    }

    pathname = f'/ticker={ticker}$start_date={start_date}$end_date={end_date}$strategy={trading_strategy}'
    for parameter in strategies_parameters:
        if trading_strategy == parameter['strategy']:
            pathname += f"${parameter['parameter']}={model_parameters[parameter['parameter']]}"
    return pathname


@app.callback(
    Output('graphs', 'children'),
    Input('update-button', 'n_clicks'),
    State('url', 'pathname'),
    State('trading-indicators', 'value'),
    State('mov-avg-fast', 'value'),
    State('mov-avg-slow', 'value'),
    State('bollinger-mov-avg', 'value'),
    State('bollinger-std', 'value'),
    State('bollinger-std-period', 'value')
)
def update_dash(
    n_clicks,
    pathname,
    trading_strategy,
    mov_avg_fast,
    mov_avg_slow,
    bollinger_mov_avg,
    bollinger_std,
    bollinger_std_period
):
    if n_clicks == 0:
        return update_dash_using_url(pathname)
    else:
        return update_dash_using_button(
            trading_strategy=trading_strategy,
            mov_avg_fast=mov_avg_fast,
            mov_avg_slow=mov_avg_slow,
            bollinger_mov_avg=bollinger_mov_avg,
            bollinger_std=bollinger_std,
            bollinger_std_period=bollinger_std_period
        )
