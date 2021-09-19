import pandas as pd
from .support_functions import moving_average


def calculate_trades_moving_average_cross(self):
    self.indicators = {
        'Mov. Avg. Curta': moving_average(
            prices=self.prices,
            mov_avg=self.model_parameters['mov_avg_fast']
        ),
        'Mov. Avg. Longa': moving_average(
            prices=self.prices,
            mov_avg=self.model_parameters['mov_avg_slow']
        )
    }
    # Create trade prices where if the fast moving avg is greater than the slow it is equal to 1,
    # in case it is less it is equal to -1, and if any of the moving averages is na then it is 0
    self.trades = pd.Series(
        data=[0] * len(self.prices),
        index=self.prices.index
    )
    self.trades.where(
        cond=self.indicators['Mov. Avg. Curta'] > self.indicators['Mov. Avg. Longa'],
        other=-1,
        inplace=True
    )
    self.trades.where(
        cond=self.indicators['Mov. Avg. Curta'] < self.indicators['Mov. Avg. Longa'],
        other=1,
        inplace=True
    )
    self.trades.where(
        cond=~(self.indicators['Mov. Avg. Curta'].isna() | self.indicators['Mov. Avg. Longa'].isna()),
        other=0,
        inplace=True
    )
    self.trades.iat[-1] = 0  # This is a hack to force the last trade to close


def calculate_trades_bollinger_bands(self):
    self.indicators = {'Média Móvel': moving_average(
        prices=self.prices,
        mov_avg=self.model_parameters['bollinger_mov_avg']
    )}
    bands_size = self.indicators['Média Móvel'].rolling(self.model_parameters['bollinger_std_period']).std() \
        * self.model_parameters['bollinger_std']
    self.indicators['BB Superior'] = self.indicators['Média Móvel'] + bands_size
    self.indicators['BB Inferior'] = self.indicators['Média Móvel'] - bands_size
    self.trades = pd.Series(
        data=[0] * len(self.prices),
        index=self.prices.index
    )
    self.trades.where(
        cond=self.indicators['BB Superior'] < self.prices,
        other=1,
        inplace=True
    )
    self.trades.where(
        cond=self.indicators['BB Inferior'] > self.prices,
        other=-1,
        inplace=True
    )
    self.trades.where(
        cond=~(self.indicators['BB Superior'].isna() | self.indicators['BB Inferior'].isna()),
        other=0,
        inplace=True
    )
    self.trades.iat[-1] = 0 #This is a hack to force the last trade to close

def calculate_trades_rsi(self):
    pass