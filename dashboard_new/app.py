import locale
from dash import html, Input, Output, Dash
import dash_bootstrap_components as dbc
import control_form.control_form as control_form
from control_form.callbacks import parameters_visibility_callback
from graph_carrousel.carrousel import carrousel, carrousel_callback
from dashboard_update_button import update_button_callback
from strategies import strategies_mapper


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
parameters_visibility_callback(app)
carrousel_callback(app)
update_button_callback(app)

app.layout = html.Div(
    children=[
        control_form.control_form,
        carrousel
    ]
)

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    app.run_server(debug=True)
