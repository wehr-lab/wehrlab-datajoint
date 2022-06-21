"""
Ingest the colony database into datajoint

.. todo::

    Still need to add the rest of the genotyping and litter information.
    How to deal with/classify these for zygosity:
    ['not genotyped',
       'no genotyping data', 'waiting on 362-00', 'check 336-00', 'hom?',
       'confirm 275-00', 'check males in same litter',
       'supposed positive', 'no genotyping done', 'check litter 228-00',
       'check litter 229-00', 'Not clipped...', '++', 'pos?', '?',
       'retest', 'check 356-01', 'het?', 'not genoryped',
       'need genotyped', ' +', '          +?', '     +', 'WT', ' + ',
       ' - ', '?+', '12/18/2015', '+ ']

    Need to link Breeding Pairs with Litters for our lines.
"""
import numpy as np
import pandas as pd
from pathlib import Path

# from element_animal import subject

from wehrdj.ingest.utils import col_to_datetime, filter_nans
from wehrdj import elements
from wehrdj.elements import subject, genotyping

MOUSE_DB_MAP = {
    'Unnamed: 0': 'subject',
    'ID': 'subject',
    'Sex': 'sex',
    'DOB': 'subject_birth_date',
    "Date Sac'd": "death_date",
    'Protocol': 'protocol',
    "+": "Present",
    "++": "Present",
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
    df["Gene 1"] = df["Gene 1"].str.strip(" *")
    df["Gene 2"] = df["Gene 2"].str.strip(" *")
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
    TODO: Decide whether we want to scrape data from the genotyping spreadsheet as well

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
    wanted_zygosities = ["Heterozygous", "Homozygous", "Absent", "Present"]
    # Remove excess spaces from spreadsheet and convert gene results a second time to see if we can rescue more
    stacked_frame["zygosity"] = stacked_frame["zygosity"].str.strip().replace(MOUSE_DB_MAP)
    # Now just only grab the genotyping results we can interpret. The rest will need to be rescued some other way
    stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains('|'.join(wanted_zygosities), regex=True) == True]
    # Old method of filtering out undesirables instead of above filtering in desireables.
    # stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains("TMF") == False]
    # stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains("not") == False]
    # stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains("Not") == False]
    # stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains("no") == False]
    # stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains("waiting") == False]
    # stacked_frame = stacked_frame[stacked_frame["zygosity"].str.contains("check") == False]
    # return stacked_frame  # Return statement for capturing the frame before insertion for debugging
    alleles = stacked_frame["allele"].unique()
    subject.Allele.insert(pd.DataFrame({"allele": alleles}), skip_duplicates=True)
    subject.Zygosity.insert(stacked_frame, skip_duplicates=True)


def insert_gene_lines(mouse_line_csv_path:Path, mouse_mating_csv_path:Path):
    """
    NOTE: There is the question of do we load a separate csv for this, or make a
    separate function to load a unique csv for this info into a MouseDB and then
    have that MouseDB be our input here

    Args:
        path:

    Returns:

    """
    GENE_LINE_MAP = {
        "Line": "line_description",
        "Origin": "source",
        "Also known as...": "alt_names"

    }
    line_db = MouseDB(pd.read_csv(mouse_line_csv_path))
    mating_db = MouseDB(pd.read_csv(mouse_mating_csv_path))
    line_db = line_db.rename(columns=GENE_LINE_MAP)
    mating_db["line"] = mating_db["Cross"].str.split(" x ")
    # Flatten the series and then strip the zygosity from the line names (stuff inbetween [])
    mating_db = mating_db.explode("line")
    mating_db["line"] = mating_db["line"].str.replace('\[.+?\]', '', regex=True).str.split("/")
    mating_db = mating_db.explode("line")
    mating_db["Cross"] = mating_db["Cross"].str.replace('\[.+?\]', '', regex=True).str.replace('/\S+', '', regex=True)
    # whole_frame = pd.concat([mating_db, line_db], axis=1)
    mating_db["is_active"] = 0
    insert_frame = mating_db[["line", "is_active"]]
    subject.Line.insert(insert_frame, skip_duplicates=True)
    cross_frame = mating_db[["Cross", "is_active"]]
    cross_frame = cross_frame.rename(columns={"Cross": "line"})
    cross_frame["is_active"] = 1
    subject.Line.insert(cross_frame, skip_duplicates=True)


def insert_breeding_pairs(mouse_mating_csv_path:Path):
    """
    Uses the matings csv from our colony spreadsheet to insert current lines and
    pair ID's into datajoint.
    Args:
        mouse_mating_csv_path:

    """
    mating_db = MouseDB(pd.read_csv(mouse_mating_csv_path))
    # Replace anything between square brackets (including the brackets), with nothing
    mating_db["Cross"] = mating_db["Cross"].str.replace('\[.+?\]', '', regex=True).str.replace('/\S+', '', regex=True)
    mating_db["Start Date"] = col_to_datetime(mating_db["Start Date"])
    ingestion_frame = mating_db[["Cross", "Start Date"]].rename(columns={"Cross": "line", "Start Date": "bp_start_date"})
    ingestion_frame["bp_description"] = mating_db["F ID"] + " & " + mating_db["M ID"]
    ingestion_frame["breeding_pair"] = mating_db["Cage #"]
    ingestion_frame = filter_nans(ingestion_frame)
    genotyping.BreedingPair.insert(ingestion_frame, skip_duplicates=True)


def insert_litters(mousedb:MouseDB):
    """
    Uses the main sheet of our colony spreadsheet to group litters and pull date
    info. There is no way to associate litter with breeding pair currently with
    the data we have recorded.

    Currently not functional since I haven't decided how to resolve that the same
    mouse lines are written in multiple different ways/some aren't in our mating
    or line spreadsheets, and therefor have no easy method of being ingested into
    the database for subject.Line and genotyping.BreedingPair

    Args:
        mousedb:

    """
    litter_db_summary = mousedb.groupby("Litter Number")["subject_birth_date"].describe(datetime_is_numeric=True)
    gene_db_summary = mousedb.groupby("Litter Number")[["Gene 1", "Gene 2"]].describe()
    columns = ["line", "breeding_pair", "litter_birth_date", "num_of_pups", "litter_notes"]
    insert_frame = pd.DataFrame(columns=columns)
    for position, (index, row) in enumerate(gene_db_summary.iterrows()):
        # Check to see if mouse has one or two genes of note
        if pd.isna(row["Gene 1"]["top"]):
            line = row["Gene 2"]["top"]
        elif pd.isna(row["Gene 2"]["top"]):
            line = row["Gene 1"]["top"]
        else:
            line = row["Gene 1"]["top"] + " x " + row["Gene 2"]["top"]
        insert_frame.at[position, "line"] = line
    insert_frame["litter_birth_date"] = pd.to_datetime(litter_db_summary["mean"], format="%y/%m/%d").values
    insert_frame["num_of_pups"] = litter_db_summary["count"].astype("float32").values
    insert_frame["litter_notes"] = litter_db_summary.index
    insert_frame["breeding_pair"] = litter_db_summary.index.str.split("-").str[0]
    insert_frame = filter_nans(insert_frame)
    genotyping.Litter.insert(insert_frame, skip_duplicates=True)
