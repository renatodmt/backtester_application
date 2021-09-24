import datetime
from dash import html, dcc
from dashboard_new.strategies import strategies_mapper


ticker_input = dcc.Input(
    id='ticker-input',
    value='Ticker',
    type='text'
)

data_range = dcc.DatePickerRange(
    id='my-date-picker-range',
    min_date_allowed=datetime.date(2016, 1, 1),
    max_date_allowed=datetime.date(2021, 9, 20),
    initial_visible_month=datetime.date(2020, 1, 1),
    end_date=datetime.date(2021, 1, 1)
)

investiment_input = dcc.Input(
    id='investment-input',
    value='1000.00',
    type='number'
)

strategy_picker = dcc.Dropdown(
    id='trading-indicators',
    options=[strategies_mapper[i]['input'] for i in strategies_mapper],
    value='mov_avg'
)

permanent_control_labels = html.Div(
    children=[
        html.Label('Ticker:'),
        html.Label('Data:'),
        html.Label('Investimento Inicial:'),
        html.Label('Estratégia:')
    ]
)

permanent_control_controls = html.Div(
    children=[
        ticker_input,
        data_range,
        investiment_input,
        strategy_picker
    ]
)

permanent_control = html.Div(
    children=[
        permanent_control_labels,
        permanent_control_controls
    ]
)