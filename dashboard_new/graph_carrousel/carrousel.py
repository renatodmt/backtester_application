from dash import html, dcc, Output, Input, callback_context
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dashboard_new.main import app


@app.callback(
    Output('carrousel-graph-trades', 'style'),
    Output('carrousel-graph-profit-loss', 'style'),
    Output('carrousel-graph-indicators', 'style'),
    Input('button-graph-trades', 'n_clicks'),
    Input('button-graph-profit-loss', 'n_clicks'),
    Input('button-graph-indicators', 'n_clicks'),
)
def change_graph_carrousel(
    trades_n_clicks,
    profit_loss_n_clicks,
    indicators_n_clicks
):
    if not callback_context.triggered:
        raise PreventUpdate
    pressed_button = callback_context.triggered[0]['prop_id'].split('.')[0]
    trades_style = {'display': 'none'}
    profit_loss_style = {'display': 'none'}
    indicators_style = {'display': 'none'}
    if pressed_button == 'button-graph-trade':
        trades_style = {'display': 'show'}
    elif pressed_button == 'button-graph-profit-loss':
        profit_loss_style = {'display': 'show'}
    elif pressed_button == 'button-graph-indicators':
        indicators_style = {'display': 'show'}

    return \
        trades_style,\
        profit_loss_style,\
        indicators_style


carrousel = html.Div(
    children=[
        dcc.Graph(
            id='carrousel-graph-trades',
        ),
        dcc.Graph(
            id='carrousel-graph-profit-loss',
            style={'display': 'none'}
        ),
        dcc.Graph(
            id='carrousel-graph-indicators',
            style={'display': 'none'}
        ),
        html.Div(
            children=[
                html.Button(
                    children='Entradas/Saídas',
                    id='button-graph-trades'
                ),
                html.Button(
                    children='Ganhos/Perdas',
                    id='button-graph-profit-loss'
                ),
                html.Button(
                    children='Indicadores da Estratégia',
                    id='button-graph-indicators'
                )
            ]
        )
    ]
)
