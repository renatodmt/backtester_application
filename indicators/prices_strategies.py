import yfinance as yf
import pandas_datareader as pdr
import database.database_api as database_api


def get_prices_from_yahoo(self):
    self.prices = pdr.get_data_yahoo(
        self.ticker,
        self.start_date,
        self.end_date,
    )["Adj Close"]


def get_prices_from_our_database(self):
    self.prices = database_api.get_adjusted_prices(
        ticker=self.ticker,
        start_date=self.start_date,
        end_date=self.end_date
    )