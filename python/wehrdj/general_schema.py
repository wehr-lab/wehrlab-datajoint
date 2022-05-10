import datajoint as dj
import wehrdj as wdj

from element_lab import lab
from element_animal import subject
from element_session import session

#%% Connecting to the database, activating, and checking current schema
wdj.connect()
schema = dj.schema("wehr_test", locals())
wdj.elements.activate()

#%% Defining out rough schema for how our data will be connected
dj.Diagram(lab)

# @schema
# class Project(dj.Manual):
#     definition = """
#     project_name    : varchar(40)
#     ---
#     project_lead    : varchar(40)
#     project_start   : date
#     project_end     : date
#     """
#
# @schema
# class
