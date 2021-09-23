import pandas as pd
import os
import sqlite3
from typing import Dict
from database.support_functions import date_to_epoch


def read_row_b3(row: str) -> Dict:
    """Transform a row of B3 files to a dictionary"""
    return {
        'type_of_register': row[0:2],
        'date_exchange': row[2:10],
        'bdi_code': row[10:12],
        'ticker': row[12:24],
        'type of market': row[24:27],
        'abbreviated_name': row[27:39],
        'paper_specification': row[39:49],
        'forward_market_term_in_days': row[49:52],
        'reference_currency': row[52:56],
        'open_price': row[56:69],
        'max_price': row[69:82],
        'low_price': row[82:95],
        'avg_price': row[95:108],
        'last_price': row[108:121],
        'best_bid': row[121:134],
        'best_ask': row[134:147],
        'n_of_trades': row[147:152],
        'n_of_papers': row[152:170],
        'volume': row[170:188],
        'strike': row[188:201],
        'indopc': row[201:202],
        'maturity_date': row[202:210],
        'factor': row[210:217],
        'strike_points': row[217:230],
        'isin': row[230:242],
        'paper_dist_number': row[242:245]
    }


def read_data_from_b3(ticker: str) -> pd.DataFrame:
    """This function goes file by file in the b3_files folders and search from rows of a ticker"""
    files_from_b3 = [file for file in os.listdir('assets/b3_files') if 'COTAHIST' in file]
    stock_data = []
    for file_name in files_from_b3:
        with open('assets/b3_files/' + file_name) as file:
            data_from_b3 = file.readlines()
        stock_data += [read_row_b3(row) for row in data_from_b3 if ticker == row[12:24].strip()]
    return pd.DataFrame(stock_data)


def database_upload(table_name: str, data: pd.DataFrame, dtype: Dict) -> None:
    conn = sqlite3.connect('prices')
    data.to_sql(
        name=table_name,
        con=conn,
        if_exists='replace',
        index=False,
        dtype=dtype
    )


def save_stock_from_b3_into_database(ticker: str) -> None:
    """This function reads files the B3 files, convert the format of the data and populate the database with close prices
    from a selected stock ticker"""
    df = read_data_from_b3(ticker)
    print(df)
    df = df[['date_exchange', 'last_price']]
    df['epoch_time'] = pd.to_datetime(df['date_exchange'], yearfirst=True).apply(date_to_epoch).astype(int)
    df['last_price'] = df['last_price'].astype(int)/100

    dtype = {
        'date_exchange': 'TEXT',
        'last_price': 'REAL',
        'epoch_time': 'INTEGER'
    }
    print(df)
    database_upload(table_name=ticker, data=df, dtype=dtype)


def read_corporative_events(ticker: str) -> pd.DataFrame:
    return pd.read_csv(f'assets/corporative_events/{ticker}.csv')


def save_corporative_events_into_database(ticker: str) -> None:
    df = read_corporative_events(ticker)
    df['epoch_time'] = pd.to_datetime(df['date_ex']).apply(date_to_epoch).astype(int).astype(int)
    df['date_ex'] = pd.to_datetime(df['date_ex']).dt.strftime('%Y%m%d')
    dtype = {
        'date_ex': 'TEXT',
        'dividend': 'REAL',
        'epoch_time': 'INTEGER'
    }
    database_upload(table_name='corporative_events_' + ticker, data=df, dtype=dtype)


stock_list = [
    'PETR3'
]

if __name__ == '__main__':
    for stock in stock_list:
        save_stock_from_b3_into_database(stock)
        save_corporative_events_into_database(stock)
