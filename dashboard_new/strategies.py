"""This file helps the translation of parameters from the url to the object and map the strategy with the function that
will be used to calculate the trades."""

from indicators.model_strategies import  \
    calculate_trades_bollinger_bands, \
    calculate_trades_moving_average_cross

strategies_mapper = {
    'mov_avg': {
        'function': calculate_trades_moving_average_cross,
        'input': {'label': 'Cruzamento Média Móvel', 'value': 'mov_avg'},
        'parameters': {
            'mov_avg_fast': {
                'label': 'Média Móvel Curta',
                'conversion': int,
                'max_value': 1000,
                'min_value': 1,
                'step': 1,
                'value': 10
            },
            'mov_avg_slow': {
                'label': 'Média Móvel Longa',
                'conversion': int,
                'max_value': 1000,
                'min_value': 1,
                'step': 1,
                'value': 10
            }
        }
    },
    'bb': {
        'function': calculate_trades_bollinger_bands,
        'input': {'label': 'Bollinger Bands', 'value': 'bb'},
        'parameters': {
            'bollinger-mov-avg': {
                'label': 'Média Móvel',
                'conversion': int,
                'max_value': 1000,
                'min_value': 1,
                'step': 1,
                'value': 14
            },
            'bollinger_std_period': {
                'label': 'Período Desvio Padrão',
                'conversion': int,
                'max_value': 1000,
                'min_value': 1,
                'step': 1,
                'value': 14
            },
            'bollinger_std': {
                'label': 'Desvio Padrão',
                'conversion': float,
                'max_value': 6,
                'min_value': 0.1,
                'step': 0.1,
                'value': 2
            }
        }
    }
}


