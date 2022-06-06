"""
Ingest the colony database into datajoint

.. todo::

    Still need to add the rest of the genotyping and litter information.

"""
import pandas as pd
from pathlib import Path

# from element_animal import subject

from wehrdj.ingest.utils import col_to_datetime, filter_nans
from wehrdj import elements
from wehrdj.elements import subject

MOUSE_DB_MAP = {
    'Unnamed: 0': 'subject',
    'Sex': 'sex',
    'DOB': 'subject_birth_date',
    "Date Sac'd": "death_date",
    'Protocol': 'protocol',
    "+": "positive",
    "-": "negative",
    "hom": "Homozygous",
    "het": "Heterozygous",
    "pos": "Present",
    "neg": "Absent"
}
"""
Mapping between values in our database and names in the datajoint model
"""


class MouseDB(pd.DataFrame):
    """Trivial subtype of dataframe to indicate this is a mouse db dataframe"""


def load_mouse_db(path:Path) -> MouseDB:
    """
    Load the mouse database from a .csv export of the "Mice" sheet from the colony database
    Clean the database to match naming and format convention of datajoint models.

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
    # Remove stars from Allele names
    df[["Gene 1", "Gene 2"]].str.rstrip("*")
    # Remap Allele names
    df[["Result", "Result.1"]].replace(MOUSE_DB_MAP)

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


def insert_subject_death(mousedb:MouseDB):
    """
    Insert the subject and death date into the datajoint database.

    :func: `wehrdj.connect` must have already been called, and
    `wehrdj.elements` has been imported

    Args:
        mousedb (:class: `.MouseDB`): the loaded mouse database

    """
    mousedb = mousedb[['subject', 'death_date']]
    # Filter our nans
    mousedb = filter_nans(mousedb)
    subject.SubjectDeath.insert(mousedb, skip_duplicates=True)


def insert_alleles(mousedb:MouseDB):
    pass
