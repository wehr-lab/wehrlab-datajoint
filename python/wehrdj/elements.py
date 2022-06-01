"""
Module that contains imports and activations for datajoint elements schemas.

Other schema should be written elsewhere, presumably in a schema module, and
then given a central ``activate`` function..

Don't be fooled by the "module imported but not used" errors your linter will give you,
for some reason you do have to import `Subject` et al even if they aren't used directly.
Don't ask me why.
"""

import datetime

import datajoint as dj
import wehrdj
from element_session import session_with_id as session
from element_animal import subject, genotyping
from element_lab import lab


from element_animal.subject import Subject
from element_animal.genotyping import Sequence, BreedingPair, Cage,\
                                      SubjectCaging, GenotypeTest
from element_lab.lab import Source, Lab, Protocol, User, Project, ProjectUser, \
                            ProjectKeywords, ProjectPublication, ProjectSourceCode
from element_session.session_with_id import Session, SessionDirectory, \
                            SessionExperimenter, SessionNote, \
                            ProjectSession
from element_animal.export.nwb import subject_to_nwb
from element_lab.export.nwb import element_lab_to_nwb_dict
from element_array_ephys import ephys_chronic as ephys
from element_array_ephys import probe
from element_array_ephys.ephys_chronic import ClusterQualityLabel
from element_deeplabcut import train, model
import pathlib
# Installed all using pip install --force-reinstall --no-deps git+https://github.com/datajoint/element-lab.git@main

wehrdj.connect()  # Wrapper for dj.conn(), can be replaced with the normal DJ function if needed

dj.config["custom"] = {"database.prefix": "wehr_"}
db_prefix = dj.config['custom'].get('database.prefix', '')

__all__ = ['genotyping', 'session', 'Subject', 'Source', 'Lab', 'Protocol', 'User',
           'Project', 'ProjectKeywords', 'ProjectPublication', 'ProjectSourceCode',
           'ProjectUser', 'Session', 'SessionDirectory', 'SessionExperimenter',
           'SessionNote', 'ProjectSession', 'Sequence', 'BreedingPair', 'Cage',
           'SubjectCaging', 'GenotypeTest', 'ClusterQualityLabel']

Experimenter = lab.User

# linking_module = "wehrdj.elements"
linking_module = __name__
# Defining classes and fuctions to add to base elements/those needed to load
# in specific elements


@lab.schema
class SkullReference(dj.Lookup):
    definition = """
    skull_reference   : varchar(60)
    """
    contents = zip(['Bregma', 'Lambda'])


@lab.schema
class Equipment(dj.Manual):
    definition = """
    equipment             : varchar(32)
    ---
    modality              : varchar(64)
    description=null      : varchar(256)
    """
    contents = [
        ["Camera1", "Pose Estimation", "Panasonic HC-V380K"],
        ["Camera2", "Pose Estimation", "Panasonic HC-V770K"],
    ]


# Two functions needed for importing elements-DLC
def get_dlc_root_data_dir():
    dlc_root_dirs = dj.config.get("custom", {}).get("dlc_root_data_dir")
    if not dlc_root_dirs:
        return None
    elif not isinstance(dlc_root_dirs, list):
        return list(dlc_root_dirs)
    else:
        return dlc_root_dirs


def get_dlc_processed_data_dir() -> str:
    """Returns session_dir relative to custom 'dlc_output_dir' root"""
    from pathlib import Path

    dlc_output_dir = dj.config.get("custom", {}).get("dlc_output_dir")
    if dlc_output_dir:
        return Path(dlc_output_dir)
    else:
        return get_dlc_root_data_dir()[0]


# Activating all elements so they can be called into other modules
lab.activate(db_prefix + "lab")
subject.activate(db_prefix + "subject", linking_module=linking_module)
session.activate(db_prefix + "session", linking_module=linking_module)
genotyping.activate(db_prefix + "genotyping", db_prefix + "subject", linking_module=linking_module)
ephys.activate(db_prefix + "ephys", db_prefix + "probe", linking_module=linking_module)
train.activate(db_prefix + "train", linking_module=linking_module)
model.activate(db_prefix + "model", linking_module=linking_module)

# Combined Schema object for diagramming with all neighbors above and below
total_schema = (dj.Diagram(lab) + dj.Diagram(genotyping) + dj.Diagram(session) + dj.Diagram(ephys)
                + dj.Diagram(train) + dj.Diagram(model) + 1 - 1 + 1 - 1)

# Currently it looks like it's better if these are not activated in a function as they can just be directly imported
# from this module instead of the respective datajoint elements modules
# def activate():
#     """
#     Call the activation functions from each of the imported elements.
#     Must have already called :func:`wehrdj.connect`
#
#     Currently:
#
#     * element_lab.lab
#     * element_animal.subject
#     * element_animal.genotyping
#     * element_session.session
#
#     It uses ``wehrdj.elements`` as the linking module, which I believe
#     is necessary because it looks for a particular context when instantiating
#     the schema? Not really sure on that one.
#
#
#     """
#     lab.activate('lab')
#     subject.activate('subject', linking_module='wehrdj.elements')
#     genotyping.activate('genotyping', 'subject', linking_module='wehrdj.elements')
#     session.activate('session', linking_module='wehrdj.elements')
#     #ephys_chronic.activate('ephys_chronic', linking_module='wehrdj.elements')
#     #model.activate("model", linking_module='wherdj.elements', )
#
