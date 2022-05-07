"""
Ingest the colony database into datajoint

.. todo::

    Still need to add the rest of the genotyping and litter information.

"""
import pandas as pd
from pathlib import Path

from element_animal import subject

from wehrdj.ingest.utils import col_to_datetime, filter_nans

MOUSE_DB_MAP = {
    'Unnamed: 0': 'subject',
    'Sex': 'sex',
    'DOB': 'subject_birth_date',
    "Date Sac'd": "death_date",
    'Protocol': 'protocol'
}
"""
Mapping between values in our database and names in the datajoint model
"""

class MouseDB(pd.DataFrame):
    """Trivial subtype of dataframe to indicate this is a mouse db dataframe"""


def load_mouse_db(path:Path) -> MouseDB:
    """
    Load the mouse database from a .csv export of the "Mice" sheet from the colony database

    Args:
        path (:class:`pathlib.Path`): The path of the csv exported from google sheets

    Returns:
        :class:`.MouseDB`
    """
    df = MouseDB(pd.read_csv(path))
    # rename columns
    df = df.rename(columns=MOUSE_DB_MAP)
    # reformat date columns to strings
    df['subject_birth_date'] = col_to_datetime(df['subject_birth_date'])
    df['death_date'] = col_to_datetime(df['death_date'])
    df['subject'].str.zfill(4)
    return df



def insert_subjects(mousedb:MouseDB):
    """
    Insert the loaded subject database into the datajoint database.

    :func:`wehrdj.connect` must have already been called.

    Args:
        mousedb (:class:`.MouseDB`): the loaded mouse database

    """
    mousedb = mousedb[['subject', 'sex', 'subject_birth_date']]
    # filter nans
    mousedb = filter_nans(mousedb)
    subject.Subject.insert(mousedb, skip_duplicates=True)