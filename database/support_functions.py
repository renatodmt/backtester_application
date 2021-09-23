import pandas as pd


def date_to_epoch(date: pd.Series):
    return (date - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")
