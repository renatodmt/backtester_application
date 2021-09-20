from dash import dcc, html
from dash.dependencies import Input, Output
from main import app


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


available_indicators = [
    {'label': 'Cruzamento Média Móvel', 'value': 'mov_avg'},
    {'label': 'Bollinger Bands', 'value': 'bb'}
]

control_component = html.Div(children=[
    dcc.Dropdown(
        id='trading-indicators',
        options=available_indicators,
        value='mov_avg'
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

    html.Button('Atualizar', id='update-button', n_clicks=0)
])
