import sqlite3
import os
import pandas as pd
import database
from .support_functions import date_to_epoch


def database_connection():
    absolute_path = os.path.abspath(database.__file__)
    absolute_path = absolute_path.replace('__init__.py', '')
    return sqlite3.connect(absolute_path + 'prices')


def get_prices(ticker, start_date, end_date):
    con = database_connection()
    start_date = date_to_epoch(start_date)
    end_date = date_to_epoch(end_date)
    query = f"SELECT date_exchange, last_price FROM {ticker} WHERE epoch_time BETWEEN {start_date} AND {end_date}"
    df = pd.read_sql_query(query, con)
    df['date_exchange'] = pd.to_datetime(df['date_exchange'], yearfirst=True)
    df.set_index('date_exchange', inplace=True)
    return df['last_price']


def get_corporative_events(ticker, start_date, end_date):
    con = database_connection()
    start_date = date_to_epoch(start_date)
    end_date = date_to_epoch(end_date)
    query = f"SELECT date_ex, dividend FROM corporative_events_{ticker} WHERE epoch_time BETWEEN {start_date} AND {end_date}"
    df = pd.read_sql_query(query, con)
    df = df.groupby('date_ex').sum().reset_index() # Since it can have more than 1 dividend per day, this code aggregates days with more than 1 dividend.
    df['date_ex'] = pd.to_datetime(df['date_ex'], yearfirst=True)
    df.set_index('date_ex', inplace=True)
    return df['dividend']


def calculated_adjusted_prices(prices, dividends):
    print(prices)
    print(dividends)
    dataf = pd.DataFrame()
    dataf['prices'] = prices
    dataf['dividends'] = dividends
    dataf['dividends'].fillna(0, inplace=True)
    dataf['cum_sum_dividends'] = dataf['dividends'].cumsum()
    return dataf['prices'] - dataf['cum_sum_dividends']


def get_adjusted_prices(ticker, start_date, end_date):
    prices = get_prices(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date
    )
    dividends = get_corporative_events(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date
    )
    return calculated_adjusted_prices(
        prices=prices,
        dividends=dividends
    )
