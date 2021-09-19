import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


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
        self.price_graph = None
        self.profit_and_loss_graph = None
        self.indicators_graph = None
        self.summary_trades_table = None

        self.get_prices()
        self.calculate_trades()
        self.calculate_profit_and_loss()
        self.create_price_graph()
        self.create_profit_loss_graph()
        self.create_indicators_graph()
        self.create_table_of_trades()

    def get_prices(self):
        """This method populates the prices attribute with a series with data as index and adjusted price as data,
        currently the method is not implemented, just returning random prices"""
        self.prices = pd.Series(
            data=np.random.choice(
                a=range(1000, 1100),
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
        self.trades.iat[-1] = 0 #This is a hack to force the last trade to close

    def calculate_profit_and_loss(self):
        """This method calculates the accumulated returns of each period and multiply by the start money."""

        stock_returns = (self.prices.shift(1) / self.prices - 1) * self.trades + 1
        self.profit_and_loss = stock_returns.cumprod() * self.start_money

    def calculate_summary_of_trades(self):
        """This method is not implemented yet. It will create a table with summary information of the trade, such as
        sharpe, drawdown and etc."""
        pass

    def create_price_graph(self):
        """This method create the price with the dots showing longs and short positions"""
        self.price_graph = go.Figure()
        line_dict = [
            {
                'trade': [-1, 0, 1],
                'color': 'gray',
                'name': 'No Trade'
            },
            {
                'trade': [1],
                'color': 'green',
                'name': 'Buy'
            },
            {
                'trade': [-1],
                'color': 'red',
                'name': 'Short'
            }
        ]
        for line in line_dict:
            self.price_graph.add_trace(
                go.Scatter(
                    y=self.prices.where(
                        self.trades.isin(line['trade']),
                        None
                    ),
                    x=self.prices.index,
                    mode='lines',
                    line_color=line['color'],
                    name=line['name']
                )
            )

    def create_profit_loss_graph(self):
        """This method create a graph showing the profit and loss of the model."""
        self.profit_and_loss_graph = px.line(
            y=self.profit_and_loss,
            x=self.profit_and_loss.index
        )

    def create_indicators_graph(self):
        """This method create the graph showing indicators value"""
        self.indicators_graph = go.Figure()
        for indicator in self.indicators:
            self.indicators_graph.add_trace(
                go.Scatter(
                    y=self.indicators[indicator],
                    x=self.indicators[indicator].index,
                    mode='lines',
                    line_color='gray',
                    name=indicator
                )
            )

    def create_table_of_trades(self):
        """This method creates a table summarizing when the model started a trade and when it ended and it profit."""
        self.summary_trades_table = pd.DataFrame()
        for trade_position in [-1, 1]:
            if trade_position == -1:
                trade_type = 'short'
            else:
                trade_type = 'buy'

            trades = pd.DataFrame()
            trades['start_date'] = self.trades[
                (self.trades.shift(1) != trade_position) & (self.trades == trade_position)].index
            trades['end_date'] = self.trades[
                (self.trades.shift(1) == trade_position) & (self.trades != trade_position)].index
            trades['position'] = trade_type
            trades['start_price'] = self.prices[self.prices.index.isin(trades['start_date'])].values
            trades['end_price'] = self.prices[self.prices.index.isin(trades['end_date'])].values
            trades['trade_return'] = (trades['end_price'] - trades['start_price']) \
                / trades['start_price'] * trade_position
            self.summary_trades_table = pd.concat([self.summary_trades_table, trades])

        self.summary_trades_table.sort_values('start_date', inplace=True)
