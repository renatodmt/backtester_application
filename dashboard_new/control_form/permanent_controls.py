import datetime
from dash import html, dcc
from dashboard_new.strategies import strategies_mapper


ticker_input = dcc.Input(
    id='ticker-input',
    value='Ticker',
    type='text'
)

data_range = dcc.DatePickerRange(
    id='date-picker-range',
    min_date_allowed=datetime.date(2016, 1, 1),
    max_date_allowed=datetime.date(2021, 9, 20),
    start_date=datetime.date(2020, 1, 1),
    end_date=datetime.date(2021, 1, 1)
)

investiment_input = dcc.Input(
    id='investment-input',
    value=1000,
    type='number'
)

strategy_picker = dcc.Dropdown(
    id='trading-indicators',
    options=[strategies_mapper[i]['input'] for i in strategies_mapper],
    value='mov_avg'
)

permanent_control = html.Div(
    children=[
        html.Label('Ticker:'),
        ticker_input,
        html.Label('Data:'),
        data_range,
        html.Label('Investimento Inicial:'),
        investiment_input,
        html.Label('Estratégia:'),
        strategy_picker
    ],
    id='control-grid'
)