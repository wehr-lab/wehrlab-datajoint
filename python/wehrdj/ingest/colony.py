"""
Ingest the colony database into datajoint
"""
import pandas as pd
import typing
from pathlib import Path

from element_animal import subject, genotyping

MOUSE_DB_MAP = {
    'Unnamed: 0': 'subject',
    'Sex': 'sex',
    'DOB': 'subject_birth',
    "Date Sac'd": "death_date",
    'Protocol': 'protocol'
}

class MouseDB(pd.DataFrame):
    """Trivial subtype of dataframe to indicate this is a mouse db dataframe"""

def col_to_datetime(column:pd.Series) -> pd.Series:
    """Date column with improperly padded m/d/y formatting"""
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





def load_mouse_db(path:Path) -> MouseDB:
    df = MouseDB(pd.read_csv(path))
    # rename columns
    df = df.rename(columns=MOUSE_DB_MAP)
    # reformat date columns to strings
    df['subject_birth'] = col_to_datetime(df['subject_birth'])
    df['death_date'] = col_to_datetime(df['death_date'])

    return df



def insert_subjects(mousedb:MouseDB):
    subject.Subject.insert(mousedb[['subject', 'sex', 'subject_birth']])