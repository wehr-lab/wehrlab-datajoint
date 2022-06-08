"""
Ingest the colony database into datajoint

.. todo::

    Still need to add the rest of the genotyping and litter information.
    Remove Arch-GFP "II" that has trailing space after it in spreadsheet

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
    "+": "Present",
    "-": "Absent",
    "hom": "Homozygous",
    "het": "Heterozygous",
    "pos": "Present",
    "neg": "Absent",
    "wt": "Absent",
    "homo": "Homozygous",
}

MOUSE_GENE_MAP = {
    "Gene 1": "allele",
    "Gene 2": "allele",
    "Result": "zygosity",
    "Result.1": "zygosity",
    "cdh23": "zygosity"
}
"""
Mapping between values in our database and names in the datajoint model
"""

# May add these definitions under the class MouseDB and then add a function
# to the class to ingest a csv
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
    df["Gene 1"] = df["Gene 1"].str.rstrip(" *")
    df["Gene 2"] = df["Gene 2"].str.rstrip(" *")
    # Remap Allele names
    df[["Result", "Result.1", "cdh23"]] = df[["Result", "Result.1", "cdh23"]].replace(MOUSE_DB_MAP)

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
    # Filter out nans
    mousedb = filter_nans(mousedb)
    subject.SubjectDeath.insert(mousedb, skip_duplicates=True)


def insert_subject_zygosity(mousedb:MouseDB):
    """
    Populates subject.Zygosity and subject.Allele for the loaded datajoint database. Alters
    MouseDB a bit to stack genes to allow for easier ingestion since DataJoint
    does not natively allow multiple genes to be associated with one mouse in one
    entry.

    Args:
        mousedb (:class: `.MouseDB`): the loaded mouse database

    """
    mousedb = mousedb[['subject', 'Gene 1', 'Result', 'Gene 2', 'Result.1', 'cdh23']]
    allele_df1 = mousedb[['subject', 'Gene 1', 'Result']]
    allele_df1 = allele_df1.rename(columns=MOUSE_GENE_MAP)
    allele_df1 = filter_nans(allele_df1)
    allele_df2 = mousedb[['subject', 'Gene 2', 'Result.1']]
    allele_df2 = allele_df2.rename(columns=MOUSE_GENE_MAP)
    allele_df2 = filter_nans(allele_df2)
    cdh23_df = mousedb[['subject', 'cdh23']]
    cdh23_df = cdh23_df.rename(columns=MOUSE_GENE_MAP)
    cdh23_df['allele'] = "cdh23"
    cdh23_df = filter_nans(cdh23_df)
    stacked_frame = pd.concat([allele_df1, allele_df2, cdh23_df], axis=0)
    stacked_frame = stacked_frame[stacked_frame["subject"].str.contains("-") == False]
    # Drop all alleles we have no information for
    stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains("TMF") == False]
    stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains("not") == False]
    stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains("Not") == False]
    stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains("no") == False]
    stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains("waiting") == False]
    stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains("check") == False]
    #TODO: Remove/alter the rest of the zygosities from stacked_frame.zygosity.unique()
    return stacked_frame
    # alleles = stacked_frame["allele"].unique()
    # print(alleles)
    # subject.Allele.insert(pd.DataFrame({"allele": alleles}), skip_duplicates=True)
    # subject.Zygosity.insert(stacked_frame, skip_duplicates=True)
