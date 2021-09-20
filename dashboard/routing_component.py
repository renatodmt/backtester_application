import datetime
from dash.dependencies import Input, Output
from main import app
from indicators.StockTrades import StockTrades
from indicators.model_strategies import calculate_trades_bollinger_bands, calculate_trades_moving_average_cross, \
    calculate_trades_rsi


@app.callback(
    Output('price-graph', 'figure'),
    Output('profit-and-loss-graph', 'figure'),
    Output('indicators-graph', 'figure'),
    Output('trade-summary', 'data'),
    Output('trade-summary', 'columns'),

)
def routing(pathname):
    strategies_mapper = {
        'mov_avg': calculate_trades_moving_average_cross,
        'bb': calculate_trades_bollinger_bands,
        'rsi': calculate_trades_rsi
    }

    try:

        object_creation_dict = {}
        for i in pathname[1:].split("$"):
            x = i.split('=')
            object_creation_dict[x[0]] = x[1]

        model = StockTrades(
            ticker=object_creation_dict['ticker'],
            start_date=datetime.datetime.strptime(object_creation_dict['start_date']),
            end_date=datetime.datetime.strptime(object_creation_dict['end_date']),
            model_parameters=object_creation_dict,
            calculate_trades=strategies_mapper[object_creation_dict['strategy']]
        )
        print('Success Routing')
        return \
            model.price_graph, \
            model.profit_and_loss_graph, \
            model.indicators_graph, \
            model.summary_trades_table.to_dict('records'), \
            [{"name": i, "id": i} for i in model.summary_trades_table.columns]

    except:
        print('Error Routing')
        return \
            [],\
            [],\
            [],\
            [],\
            []


