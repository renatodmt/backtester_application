import plotly.graph_objects as go
from dash import html, dcc, Output, Input, callback_context
from dash.exceptions import PreventUpdate


def carrousel_callback(app):
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
        print(callback_context.triggered)
        print(callback_context.triggered[0]['prop_id'].split('.')[0])
        if not callback_context.triggered:
            print('prevented')
            raise PreventUpdate
        pressed_button = callback_context.triggered[0]['prop_id'].split('.')[0]
        print(pressed_button)
        trades_style = {'display': 'none'}
        profit_loss_style = {'display': 'none'}
        indicators_style = {'display': 'none'}
        if pressed_button == 'button-graph-trades':
            trades_style = {'display': 'block'}
        elif pressed_button == 'button-graph-profit-loss':
            profit_loss_style = {'display': 'block'}
        elif pressed_button == 'button-graph-indicators':
            indicators_style = {'display': 'block'}
        print(trades_style)
        print(profit_loss_style)
        print(indicators_style)
        return \
            trades_style,\
            profit_loss_style,\
            indicators_style


carrousel = html.Div(
    children=[
        dcc.Graph(
            id='carrousel-graph-trades',
            figure=go.Figure()
        ),
        dcc.Graph(
            id='carrousel-graph-profit-loss',
            figure=go.Figure(),
            style={'display': 'none'}
        ),
        dcc.Graph(
            id='carrousel-graph-indicators',
            figure=go.Figure(),
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
            ],
            id='button-grid'
        )
    ]
)
