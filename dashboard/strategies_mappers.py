"""This file helps the translation of parameters from the url to the object and map the strategy with the function that
will be used to calculate the trades."""

from indicators.model_strategies import  \
    calculate_trades_bollinger_bands, \
    calculate_trades_moving_average_cross


strategies_parameters = [
    {'strategy': 'mov_avg', 'parameter': 'mov_avg_fast', 'conversion': int},
    {'strategy': 'mov_avg', 'parameter': 'mov_avg_slow', 'conversion': int},
    {'strategy': 'bb', 'parameter': 'bollinger_std', 'conversion': float},
    {'strategy': 'bb', 'parameter': 'bollinger_std_period', 'conversion': int},
    {'strategy': 'bb', 'parameter': 'bollinger_mov_avg', 'conversion': int}
]

strategies_mapper = {
    'mov_avg': calculate_trades_moving_average_cross,
    'bb': calculate_trades_bollinger_bands
}

available_indicators = [
    {'label': 'Cruzamento Média Móvel', 'value': 'mov_avg'},
    {'label': 'Bollinger Bands', 'value': 'bb'}
]
