import locale
from dash import html, Input, Output
from main import app
import control_form.control_form as control_form
import graph_carrousel.carrousel as carrousel
from strategies import strategies_mapper


@app.callback(
    Output('mov-avg-parameters', 'style'),
    Output('bb-parameters', 'style'),
    Input('trading-indicators', 'value')
)
def change_parameters_visibility(trading_indicators):
    styles = []
    for strategy in strategies_mapper:
        if trading_indicators == strategy:
            styles.append({'display': 'block'})
        else:
            styles.append({'display': 'none'})
    return tuple(styles)


app.layout = html.Div(
    children=[
        control_form.control_form,
        carrousel.carrousel
    ]
)

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    app.run_server(debug=True)
