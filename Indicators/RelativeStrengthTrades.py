import pandas as pd
from StockTrades import StockTrades



class MovingAverageCross(StockTrades):
    def __init__(
            self,
            ticker: str,
            start_date: str,
            end_date: str,
            rsi_period: int,
            rsi_up: int,
            rsi_down: int,
            start_money: int = 1000
    ):
        super.__init__(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            start_money=start_money
        )

        self.rsi_period = rsi_period
        self.rsi_up = rsi_up
        self.rsi_down = rsi_down

        self.calculte_trades()

    def calculate_trades(self):
        super().calculate_trades()


