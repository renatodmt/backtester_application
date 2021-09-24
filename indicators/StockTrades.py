import random
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
from plotly.subplots import make_subplots
from typing import Dict, Callable


templates = ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]


class StockTrades:
    """This class gets price from the api and calculate the figures and tables for the UI"""
    def __init__(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        model_parameters: Dict,
        calculate_trades: Callable,
        get_prices: Callable,
        start_money: int = 1000
    ):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.start_money = start_money
        self.model_parameters = model_parameters
        self.calculate_trades = calculate_trades
        self.get_prices = get_prices

        self.prices = None
        self.trades = None
        self.trade_profit_and_loss = None
        self.indicators = None
        self.price_graph = None
        self.profit_and_loss_graph = None
        self.stock_profit_and_loss = None
        self.indicators_graph = None
        self.main_summary_trades_table = None
        self.summary_trades_table = None
        self.fig_subplots = None
        self.stock_max_dd = None
        self.trade_max_dd = None

        self.get_prices(self)
        self.calculate_trades(self)
        self.calculate_profit_and_loss()
        self.create_price_graph()
        self.create_profit_loss_graph()
        self.create_indicators_graph()
        self.calculate_summary_of_trades()
        self.create_table_of_trades()
        self.create_subplot_graph()

    def calculate_profit_and_loss(self):
        """This method calculates the accumulated returns of each period and multiply by the start money."""

        trade_returns = (self.prices / self.prices.shift(1) - 1) * self.trades + 1
        self.trade_profit_and_loss = trade_returns.cumprod() * self.start_money

        stock_returns = (self.prices / self.prices.shift(1) - 1) + 1
        self.stock_profit_and_loss = stock_returns.cumprod() * self.start_money


    def calculate_summary_of_trades(self):
            """This method is not implemented yet. It will create a table with summary information of the trade, such as
            sharpe, drawdown and etc."""

            self.stock_max_dd = (((self.stock_profit_and_loss - self.stock_profit_and_loss.cummax()) / self.stock_profit_and_loss.cummax()).min() * 100).round(1).astype(str) + '%'
            self.trade_max_dd = (((self.trade_profit_and_loss - self.trade_profit_and_loss.cummax()) / self.trade_profit_and_loss.cummax()).min() * 100).round(1).astype(str) + '%'

            start_date = datetime.datetime(2018, 1, 1)
            end_date = datetime.datetime(2021, 1, 1)
            years = (end_date - start_date).days / 365

            resumo = {'': ['Montante Inicial',
                         'Montante Final',
                         'Retorno Total',
                         'CAGR',
                         'Máximo DrawDown',
                         'Índice Sharpe'],
                    'Ação': ['R$' + f'{self.start_money}',
                             'R$' + self.stock_profit_and_loss.iat[-1].round(2).astype(str),
                             ((self.stock_profit_and_loss.iat[-1] / self.start_money - 1) * 100).round(1).astype(str) + '%',
                             ((((self.stock_profit_and_loss.iat[-1] / self.start_money) ** (1 / years)) - 1) * 100).round(1).astype(str) + '%',
                             self.stock_max_dd,
                             "-"], #INDICE SHARPE = (Ret Ação – SELIC)/ DESV Ação
                    'Trade': ['R$' + f'{self.start_money}',
                              'R$' + self.trade_profit_and_loss.iat[-1].round(2).astype(str),
                              ((self.trade_profit_and_loss.iat[-1] / self.start_money - 1) * 100).round(1).astype(str) + '%',
                              ((((self.trade_profit_and_loss.iat[-1] / self.start_money) ** (1 / years)) - 1) * 100).round(1).astype(str) + '%',
                              self.trade_max_dd,
                              "-"]} #INDICE SHARPE = (Ret Trade – SELIC)/ DESV Trade

            self.main_summary_trades_table = pd.DataFrame(resumo)


    def create_price_graph(self):
        """This method create the price with the dots showing longs and short positions"""
        self.price_graph = []
        line_dict = [
            {
                'trade': [-1, 0, 1],
                'color': 'gray',
                'name': 'Sem Posição'
            },
            {
                'trade': [1],
                'color': 'green',
                'name': 'Comprado'
            },
            {
                'trade': [-1],
                'color': 'red',
                'name': 'Vendido'
            }
        ]
        for line in line_dict:
            self.price_graph.append(
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
        self.profit_and_loss_graph = go.Scatter(
            y=self.trade_profit_and_loss,
            x=self.trade_profit_and_loss.index,
            name='Profit & Loss',
            mode='lines'
        )

    def create_indicators_graph(self):
        """This method create the graph showing indicators value"""
        self.indicators_graph = []
        for indicator in self.indicators:
            self.indicators_graph.append(
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
                trade_type = 'Vendido'
            else:
                trade_type = 'Comprado'

            trades = pd.DataFrame()
            trades['Data Início'] = self.trades[
                (self.trades.shift(1) != trade_position) & (self.trades == trade_position)].index
            trades['Data Fim'] = self.trades[
                (self.trades.shift(1) == trade_position) & (self.trades != trade_position)].index
            trades['Posição'] = trade_type
            print(self.prices)
            print(self.prices.index.isin(trades['Data Início']))
            trades['Preço Entrada'] = self.prices[self.prices.index.isin(trades['Data Início'])].values
            trades['Preço Saída'] = self.prices[self.prices.index.isin(trades['Data Fim'])].values
            trades['Retorno (%)'] = (trades['Preço Saída'] - trades['Preço Entrada']) \
                / trades['Preço Entrada'] * trade_position * 100
            self.summary_trades_table = pd.concat([self.summary_trades_table, trades])

        self.summary_trades_table.sort_values('Data Início', inplace=True)
        self.summary_trades_table['Data Início'] = self.summary_trades_table['Data Início'].dt.strftime('%d/%b/%y')
        self.summary_trades_table['Data Fim'] = self.summary_trades_table['Data Fim'].dt.strftime('%d/%b/%y')
        self.summary_trades_table['Retorno (%)'] = self.summary_trades_table['Retorno (%)'].round(2).astype(str) + '%'
        self.summary_trades_table['Preço Entrada'] = self.summary_trades_table['Preço Entrada'].round(2)
        self.summary_trades_table['Preço Saída'] = self.summary_trades_table['Preço Saída'].round(2)

    def create_subplot_graph(self):
        """This graph is a subplot with prices graph, p&l and indicators """
        self.fig_subplots = make_subplots(
            rows=3,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05
        )

        for trace in self.price_graph:
            self.fig_subplots.add_trace(trace, row=1, col=1)

        self.fig_subplots.add_trace(self.profit_and_loss_graph, row=2, col=1)

        for trace in self.indicators_graph:
            self.fig_subplots.add_trace(trace, row=3, col=1)

        self.fig_subplots.update_layout(
            margin=dict(
                l=10,
                r=10,
                b=10,
                t=10
            )
        )

        self.fig_subplots['layout']['yaxis']['title'] = 'Preço'
        self.fig_subplots['layout']['yaxis2']['title'] = 'Dinheiro'
        self.fig_subplots['layout']['yaxis3']['title'] = 'Indicadores'
        self.fig_subplots.update_layout(template=random.choice(templates))

