from dash import Output, Input
from dashboard_new.strategies import strategies_mapper


def parameters_visibility_callback(app):
    callback_inputs_and_outputs = tuple(Output(strategy.replace('_', '-') + '-parameters', 'style') for strategy in strategies_mapper)
    callback_inputs_and_outputs = (*callback_inputs_and_outputs, Input('trading-indicators', 'value'))
    @app.callback(
        callback_inputs_and_outputs
    )
    def change_parameters_visibility(trading_indicators):
        styles = []
        for strategy in strategies_mapper:
            if trading_indicators == strategy:
                styles.append({'display': 'grid'})
            else:
                styles.append({'display': 'none'})
        return tuple(styles)
