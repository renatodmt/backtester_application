import datetime
from dash import html, dcc, dash_table
from strategies_mappers import strategies_mapper
from indicators.StockTrades import StockTrades
from indicators.prices_strategies import get_prices_from_our_database


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
    ticker = 'PETR3'
    start_date = datetime.datetime(2018, 1, 1)
    end_date = datetime.datetime(2021, 1, 1)
    years = (end_date - start_date).days / 365

    model = StockTrades(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        model_parameters=model_parameters,
        calculate_trades=strategies_mapper[trading_strategy],
        get_prices=get_prices_from_our_database
    )

    return [
        dcc.Graph(id='price-graph', figure=model.fig_subplots),
        html.Div(
            children=[dash_table.DataTable(
                id='trade-summary',
                data=model.main_summary_trades_table.to_dict('records'),
                columns=[{"name": i, "id": i} for i in model.main_summary_trades_table.columns],
                style_cell={'textAlign': 'center'},
                style_data_conditional=[
                    {
                        'if': {
                            'filter_query': '{Ação} > {Trade}',
                            'column_id': 'Ação',
                            'row_index': 3
                        },
                        'backgroundColor': 'green',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'filter_query': '{Ação} < {Trade}',
                            'column_id': 'Trade',
                            'row_index': 3
                        },
                        'backgroundColor': 'green',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'filter_query': '{Ação} < {Trade}',
                            'column_id': 'Ação',
                            'row_index': 4
                        },
                        'backgroundColor': 'green',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'filter_query': '{Ação} > {Trade}',
                            'column_id': 'Trade',
                            'row_index': 4
                        },
                        'backgroundColor': 'green',
                        'color': 'white'
                    }
                ]

            ),
            dash_table.DataTable(
                id='trade-summary',
                data=model.summary_trades_table.to_dict('records'),
                columns=[{"name": i, "id": i} for i in model.summary_trades_table.columns],
                style_cell={'textAlign': 'center'}
                )
            ]
        )
    ]
