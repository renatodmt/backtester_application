import pandas as pd


def moving_average(prices: pd.Series, mov_avg: int):
    if mov_avg < 0:
        raise Exception("Moving Average should be a positive number.")

    return prices.rolling(mov_avg).mean()
