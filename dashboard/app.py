# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html
import dash_table
from indicators.MovingAverageCross import MovingAverageCross

app = dash.Dash(__name__)

stock_trades = MovingAverageCross(
    ticker='PETR4',
    start_date='2021-01-01',
    end_date='2021-09-01',
    mov_avg_fast=10,
    mov_avg_slow=100
)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='price-graph',
        figure=stock_trades.price_graph
    ),

    dcc.Graph(
        id='profit-and-loss-graph',
        figure=stock_trades.profit_and_loss_graph
    ),

    dcc.Graph(
        id='indicators-graph',
        figure=stock_trades.indicators_graph
    ),

    html.Div(
        children=dash_table.DataTable(
            id='tbl', data=stock_trades.summary_trades_table.to_dict('records'),
            columns=[{"name": i, "id": i} for i in stock_trades.summary_trades_table.columns],
        )
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)