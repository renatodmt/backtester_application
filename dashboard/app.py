# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import locale
from dash import html, dcc
from dash.dependencies import Input, Output
from control_component import control_component
from figures_component import figures_component
from main import app


app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.H1(id='title', children='Backtester de Estratégias'),
    control_component,
    figures_component
])


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    app.run_server(debug=True)