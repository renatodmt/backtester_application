from strategies_mappers import strategies_parameters, strategies_mapper
from indicators.StockTrades import StockTrades


def update_dash_using_button(
    trading_strategy,
    mov_avg_fast,
    mov_avg_slow,
    bollinger_mov_avg,
    bollinger_std,
    bollinger_std_period
):
    model_parameters = {
        'mov_avg_fast': mov_avg_fast,
        'mov_avg_slow': mov_avg_slow,
        'bollinger_mov_avg': bollinger_mov_avg,
        'bollinger_std': bollinger_std,
        'bollinger_std_period': bollinger_std_period
    }

    # Placeholder for ticker, start_date and end_date. They will come from the UI after.
    ticker = 'petr4'
    start_date = '2020-01-01'
    end_date = '2021-01-01'

    pathname = f'/ticker={ticker}$start_date={start_date}$end_date={end_date}$strategy={trading_strategy}'
    for parameter in strategies_parameters:
        if trading_strategy == parameter['strategy']:
            pathname += f"${parameter['parameter']}={model_parameters[parameter['parameter']]}"

    model = StockTrades(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        model_parameters=model_parameters,
        calculate_trades=strategies_mapper[trading_strategy]
    )

    return \
        model.price_graph, \
        model.profit_and_loss_graph, \
        model.indicators_graph, \
        model.summary_trades_table.to_dict('records'), \
        [{"name": i, "id": i} for i in model.summary_trades_table.columns], \
        pathname
