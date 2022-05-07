"""
Utility functions for ingestion! what else!
"""

import warnings

import pandas as pd


def col_to_datetime(column:pd.Series) -> pd.Series:
    """
    Fix date column with improperly padded m/d/y formatting
    """
    # remove any nonnumeric, nonslash characters
    column = column.str.replace(r'[^\d/]', '', regex=True)
    split_date = column.str.split('/', expand=True).rename(columns={0: 'month', 1: "day", 2: "year"})
    # zfill months and days
    split_date['month'] = split_date['month'].str.zfill(2)
    split_date['day'] = split_date['day'].str.zfill(2)
    # strip preceding "20" on some dates
    split_date['year'] = split_date['year'].str[-2:]
    # recombine
    date_join = split_date['year'] + '/' + split_date['month'] + '/' + split_date['day']
    date = pd.to_datetime(date_join, format="%y/%m/%d", errors='coerce')
    return date


def filter_nans(df:pd.DataFrame) -> pd.DataFrame:
    """filter any rows with NANs with warning"""
    na_rows = df.isna().any(axis=1)
    if sum(na_rows) > 0:
        warnings.warn(f"Dropping {sum(na_rows)} rows with NaNs in them:\n{df[na_rows]}")
    df = df[~na_rows]
    return df