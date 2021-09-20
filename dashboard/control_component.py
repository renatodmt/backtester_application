from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from main import app
from strategies_mappers import available_indicators


@app.callback(
    Output('mov-avg-cross-parameters', 'style'),
    Output('bollinger-bands-parameters', 'style'),
    Input('trading-indicators', 'value')
)
def change_visibility_models_parameters(trading_strategy):
    mov_avg = {'display': 'none'}
    bollinger = {'display': 'none'}

    if trading_strategy == 'mov_avg':
        mov_avg = {'display': 'flex'}
    elif trading_strategy == 'bb':
        bollinger = {'display': 'flex'}

    return mov_avg, bollinger


control_component = html.Div(children=[
    dcc.Dropdown(
        id='trading-indicators',
        options=available_indicators,
        value='mov_avg'
    ),

    html.Div(
        id='mov-avg-cross-parameters',
        className='model-parameters',
        children=[
            html.Div(
                className='parameters-col',
                children=[
                    html.Label(children='Média Móvel Curta'),
                    html.Label(children='Média Móvel Longa')
                ]
            ),
            html.Div(
                className='parameters-col',
                children=[
                    dcc.Input(
                        id='mov-avg-fast',
                        type="number",
                        min=1,
                        max=365,
                        step=1,
                        value=10,
                    ),
                    dcc.Input(
                        id='mov-avg-slow',
                        type="number",
                        min=1,
                        max=365,
                        step=1,
                        value=60,
                    )
                ]
            )
        ]
    ),

    html.Div(
        id='bollinger-bands-parameters',
        children=[
            html.Div(
                className='parameters-col',
                children=[
                    html.Label(children='Média Móvel'),
                    html.Label(children='Desvio Padrão'),
                    html.Label(children='Período Desvio Padrão')
                ]
            ),
            html.Div(
                className='parameters-col',
                children=[
                    dcc.Input(
                        id='bollinger-mov-avg',
                        type="number",
                        min=1,
                        max=365,
                        step=1,
                        value=14,
                    ),
                    dcc.Input(
                        id='bollinger-std',
                        type="number",
                        min=0.1,
                        max=4,
                        step=0.1,
                        value=2,
                    ),
                    dcc.Input(
                        id='bollinger-std-period',
                        type="number",
                        min=2,
                        max=365,
                        step=1,
                        value=20,
                    )
                ]
            )
        ]
    ),

    dbc.Button(
        children="Atualizar",
        color="primary",
        id='update-button',
        n_clicks=0
    )
])
