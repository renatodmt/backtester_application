import pandas as pd
from .StockTrades import StockTrades
from .support_functions import moving_average


class BollingerBands(StockTrades):
    def __init__(
            self,
            ticker: str,
            start_date: str,
            end_date: str,
            bands_mov_avg_period: int,
            bands_std: int,
            band_std_period: int,
            start_money: int = 1000
    ):
        self.bands_mov_avg_period = bands_mov_avg_period
        self.bands_std = bands_std
        self.band_std_period = band_std_period

        super().__init__(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            start_money=start_money
        )

    def calculate_trades(self):
        self.indicators = {'Moving Average': moving_average(
            prices=self.prices,
            mov_avg=self.bands_mov_avg_period
        )}
        self.indicators['Bollinger Band Up'] = self.indicators['Moving Average'] + \
            self.indicators['Moving Average'].rolling(self.band_std_period).std() * self.bands_std
        self.indicators['Bollinger Band Down'] = self.indicators['Moving Average'] - \
            self.indicators['Moving Average'].rolling(self.band_std_period).std() * self.bands_std

        self.trades = pd.Series(
            data=[0] * len(self.prices),
            index=self.prices.index
        )
        self.trades.where(
            cond=self.indicators['Bollinger Band Up'] < self.prices,
            other=1,
            inplace=True
        )
        self.trades.where(
            cond=self.indicators['Bollinger Band Down'] > self.prices,
            other=-1,
            inplace=True
        )
        self.trades.where(
            cond=~(self.indicators['Bollinger Band Up'].isna() | self.indicators['Bollinger Band Down'].isna()),
            other=0,
            inplace=True
        )

        super().calculate_trades()
