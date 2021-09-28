import datetime
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from strategies import strategies_mapper
from indicators.StockTrades import StockTrades
from indicators.prices_strategies import get_prices_from_our_database


def update_button_callback(app):
    callback_outputs = [
        Output('carrousel-graph-trades', 'figure'),
        Output('carrousel-graph-profit-loss', 'figure'),
        Output('carrousel-graph-indicators', 'figure')
    ]

    callback_initial_inputs = [
        Input('update-button', 'n_clicks'),
        State('ticker-input', 'value'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date'),
        State('trading-indicators', 'value'),
        State('investment-input', 'value')
    ]
    initial_parameter_len = len(callback_initial_inputs)
    parameter_argument_callback = [
        State(parameter, 'value')
        for strategy in strategies_mapper
        for parameter in strategies_mapper[strategy]['parameters']
    ]
    callback_inputs_and_outputs = tuple(
        callback_outputs +
        callback_initial_inputs +
        parameter_argument_callback
    )


    def get_model_parameters_from_args(args):
        """This function helps to create a dict of parameters and values to pass to the StockTrade object since dash pass
        the arguments of the function by position"""
        model_parameters = {}
        args_counter = initial_parameter_len
        for strategy in strategies_mapper:
            for parameter in strategies_mapper[strategy]['parameters']:
                model_parameters[parameter] = args[args_counter]
                args_counter += 1
        return model_parameters


    @app.callback(
        callback_inputs_and_outputs
    )
    def update_dash_via_button(*args):
        start_date = datetime.datetime.strptime(args[2], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(args[3], '%Y-%m-%d')
        if args[0] is None:
            raise PreventUpdate
        model_parameters = get_model_parameters_from_args(args)

        model = StockTrades(
            ticker=args[1],
            start_date=start_date,
            end_date=end_date,
            model_parameters=model_parameters,
            calculate_trades=strategies_mapper[args[4]]['function'],
            get_prices=get_prices_from_our_database,
            start_money=args[5]
        )

        return\
            model.price_graph,\
            model.profit_and_loss_graph,\
            model.indicators_graph
