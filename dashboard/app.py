import locale
from dash import html, dcc
import dash_bootstrap_components as dbc
from control_component import control_component
from routing_callbacks import update_dash, change_button_status
from main import app

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.H1(id='title', children='Backtester de Estratégias'),
    html.Hr(),
    control_component,
    html.Hr(),
    dbc.Spinner(children=html.Div(id='graphs'), id='spinner')
])

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    app.run_server(debug=True)
