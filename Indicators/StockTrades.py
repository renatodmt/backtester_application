import pandas as pd
import numpy as np


class StockTrades:
    def __init__(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        start_money: int = 1000
    ):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.start_money = start_money

        self.prices = None
        self.trades = None
        self.profit_and_loss = None
        self.indicators = None
        self.get_prices()

    def get_prices(self):
        """This method populates the prices attribute with a series with data as index and adjusted price as data,
        currently the method is not implemented, just returning random prices"""
        self.prices = pd.Series(
            data=np.random.choice(
                a=range(1000,1100),
                size=len(pd.date_range(
                    start=self.start_date,
                    end=self.end_date
                ))
            ),
            index=pd.date_range(
                start=self.start_date,
                end=self.end_date
            )
        )

    def calculate_trades(self):
        """This method calculate the trading series (1 for buy, -1 for sell and 0 for no trades), it should be
        implemented in the child objects, but we put the general error checking in here and call via super"""
        if not hasattr(self, 'prices'):
            raise Exception("You have to call get_prices method before calculating trades")

    def calculate_profit_and_loss(self):
        """This method calculates the accumulated returns of each period and multiply by the start money."""
        if not hasattr(self, 'trades'):
            raise Exception("You have to call calculate_trades method before calculating profit_and_loss")

        stock_returns = (self.prices.shift(1) / self.prices - 1) * self.trades + 1
        self.profit_and_loss = stock_returns.cumprod() * self.start_money

    def calculate_summary_of_trades(self):
        """This method is not implemented yet. It will create a table with summary information of the trade, such as
        sharpe, drawdown and etc."""
        pass
