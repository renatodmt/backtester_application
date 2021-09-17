import pandas as pd
from StockTrades import StockTrades


def moving_average(prices: pd.Series, mov_avg: int):
    if mov_avg < 0:
        raise Exception("Moving Average should be a positive number.")

    return prices.rolling(mov_avg).mean()


class MovingAverageCross(StockTrades):
    def __init__(
            self,
            ticker: str,
            start_date: str,
            end_date: str,
            mov_avg_fast: int,
            mov_avg_slow: int,
            start_money: int = 1000
    ):
        super.__init__(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            start_money=start_money
        )

        self.mov_avg_fast = mov_avg_fast
        self.mov_avg_slow = mov_avg_slow

        self.calculte_trades()

    def calculate_trades(self):
        super().calculate_trades()

        self.indicators = {
            'mov_avg_fast': moving_average(
                prices=self.prices,
                mov_avg=self.mov_avg_fast
            ),
            'mov_avg_slow': moving_average(
                prices=self.prices,
                mov_avg=self.mov_avg_slow
            )
        }

        # Create trade prices where if the fast moving avg is greater than the slow it is equal to 1,
        # in case it is less it is equal to -1, and if any of the moving averages is na then it is 0
        self.trades = pd.Series(
            data=[0] * len(self.prices),
            index=self.prices.index
        )
        self.trades.where(
            cond=self.indicators['mov_avg_fast'] > self.indicators['mov_avg_slow'],
            other=-1,
            inplace=True
        )
        self.trades.where(
            cond=self.indicators['mov_avg_fast'] < self.indicators['mov_avg_slow'],
            other=1,
            inplace=True
        )
        self.trades.where(
            cond=~(self.indicators['mov_avg_fast'].isna() | self.indicators['mov_avg_slow'].isna()),
            other=0,
            inplace=True
        )

