"""
File for injecting the basic lab info into our Wehr DJ model. Also allows
testing of the import system for our schema.
"""
#TODO: This abomination of a file highlights why we need to be able to scrape
# the user data from somewhere. Python is not great for manually putting it all in.
import datajoint as dj
import pandas as pd
from element_lab import lab
from wehrdj import elements
from wehrdj import connect

connect()

db_prefix = dj.config['custom'].get('database.prefix', '')

#%% lab.Lab() setup
lab_dict = {
    "lab": "Wehr Lab",
    "lab_name": "Wehr Lab",
    "institution": "University of Oregon, Institute of Neuroscience",
    "address": "1440 Franklin Blvd., Eugene, 97403",
    "time_zone": "UTC-8",
}
lab.Lab.insert1(lab_dict, skip_duplicates=True)

# May need to add Offices/Mouse Facilities as needed for other modules
Location_dict = {
    "LISB 207B": "Rig Room 1",
    "LISB 207C": "Rig Room 2",
    "LISB 207D": "Rig Room 3",
    "LISB 207A": "Electronics Shop",
    "LISB 207": "Main Lab Space",
    "LISB 204C": "Computer and Server Room",
    "LISB 204A": "Histology Room",
    "LISB 204B": "Microscopy Room",
    "LISB 206": "Mouse Annex",
    "LISB 206A": "Rig Room 4",
    "LISB 206B": "Rig Room 5",
    "LISB 206C": "Mouse Room 1",
    "LISB 206D": "Mouse Room 2",
}
for key, value in Location_dict.items():
    lab.Location.insert1({"lab": "Wehr Lab", "location": key, "location_description": value,},
                         skip_duplicates=True)
#%% lab.User,LabMembership,UserRole setup
user_info_col_names = ["lab", 'user', 'user_role', 'user_email', 'project']
people_df = pd.DataFrame(columns=user_info_col_names)

# Maybe in hindsight I should have just made a user class to ingest this...
users = ["Matt Nardoci", 'Molly Shallow', 'Nick Sattler', 'Mike Wehr', 'Lucas Ott', 'Aldis Weible', 'Kip Keller', 'Jonny Saunders',
         'Sam Mehan', 'Tillie Morris', 'Alexa Wright', 'Loie Bonnet']

for index, person in enumerate(users):
    people_df.at[index, 'user'] = person
    if person in ['Matt Nardoci', 'Molly Shallow', 'Nick Sattler', 'Sam Mehan', 'Jonny Saunders']:
        people_df.at[index, 'user_role'] = 'Grad Student'
    elif person in ['Kip Keller', 'Aldis Weible']:
        people_df.at[index, 'user_role'] = 'Staff Scientist'
    elif person in ['Lucas Ott']:
        people_df.at[index, 'user_role'] = 'Research Tech'
    elif person in ['Mike Wehr']:
        people_df.at[index, 'user_role'] = 'P. Investigator'
    else:
        people_df.at[index, 'user_role'] = 'UGrad Researcher'

user_roles = ["Grad Student", "Staff Scientist", "Research Tech", "P. Investigator",
              "UGrad Researcher", "Post-doc Scholar"]

for index, person in enumerate(users):
    if person == "Molly Shallow":
        people_df.at[index, 'project'] = "ZI Activation"
        people_df.at[index, 'user_email'] = "mshallow@uoregon.edu"
    elif person == "Nick Sattler":
        people_df.at[index, 'project'] = "TBD"
        people_df.at[index, 'user_email'] = "nsattler@uoregon.edu"
    elif person == "Matt Nardoci":
        people_df.at[index, 'project'] = "Behavioral Modeling"
        people_df.at[index, 'user_email'] = "mnardoci@uoregon.edu"
    elif person == "Mike Wehr":
        people_df.at[index, 'project'] = "Everything, Everywhere"
        people_df.at[index, 'user_email'] = "wehr@uoregon.edu"
    elif person == "Lucas Ott":
        people_df.at[index, 'project'] = "TBD"
        people_df.at[index, 'user_email'] = "lucaso@uoregon.edu"
    elif person == "Kip Keller":
        people_df.at[index, 'project'] = "Sound Inhibition"
        people_df.at[index, 'user_email'] = "keller@uoneuro.uoregon.edu"
    elif person == "Sam Mehan":
        people_df.at[index, "project"] = "Speech Context"
        people_df.at[index, "user_email"] = "smehan@uoregon.edu"
    elif person == "Aldis Weible":
        people_df.at[index, "project"] = "Alzheimer models"
        people_df.at[index, 'user_email'] = "aldis@uoneuro.uoregon.edu"
    elif person == "Jonny Saunders":
        people_df.at[index, "project"] = "Autopilot"
        people_df.at[index, "user_email"] = "jsaunder@uoregon.edu"
    elif person == 'Tillie Morris':
        people_df.at[index, "project"] = "TBD"
        people_df.at[index, 'user_email'] = "tilliem@uoregon.edu"
    elif person == 'Alexa Wright':
        people_df.at[index, "project"] = "ZI Activation"
        people_df.at[index, "user_email"] = "alexawriight@gmail.com"
    elif person == "Loie Bonnet":
        people_df.at[index, "project"] = "ZI Activation"
        people_df.at[index, "user_email"] = "lbonnet@uoregon.edu"

people_df['lab'] = 'Wehr Lab'

# Now ingestion
lab.User.insert(people_df[["user", "user_email"]], skip_duplicates=True)
for index, role in enumerate(user_roles):
    print(role, index)
    lab.UserRole.insert1([role], skip_duplicates=True)
lab.LabMembership.insert(people_df[["lab", "user", "user_role"]], skip_duplicates=True)

#%% Project set-up
proj_columns = ["project", "project_description"]
proj_df = pd.DataFrame(columns=proj_columns)
# Need to add in all projects to then update down on ProjectUser
projects = {
    "ZI Activation": "EDIT LATER: Motivation or something who knows",
    "Behavioral Modeling": "lmao you think I know what my own project is?",
    "TBD": "Placeholder for projects",
    "Everything, Everywhere": "The role of the bossman",
    "Speech Context": "Just make the mice talk 4Head",
    "Sound Inhibition": "Can we disrupt mice's ability to hear what they want to hear?",
    "Alzheimer models": "What is Alzheimer's again?",
    "Autopilot": "I reject your reality and substitute my own"
}

# And Ingestion
for project, description in projects.items():
    lab.Project.insert1({"project": project, "project_description": description}, skip_duplicates=True)

#%% Animal sources
source_columns = ["source", "source_name", "contact_details", "source_description"]
source_df = pd.DataFrame(columns=source_columns)
source_df.at[0, "source"] = "JAX"
source_df.at[0, "source_name"] = "The Jackson Laboratory"
source_df.at[0, "contact_details"] = "www.jax.org"
source_df.at[0, "source_description"] = "Jackson Labs mouse respository"

lab.Source.insert(source_df, skip_duplicates=True)

#%% ProjectUser tables
project_dict = {
    "ZI Activation": ["Molly Shallow", "Loie Bonnet", "Alexa Wright"],
    "Speech Context": ["Sam Mehan", "Nick Sattler", "Loie Bonnet", "Alexa Wright"],
    "Alzheimer models": ["Aldis Weible"],
    "Sound Inhibition": ["Kip Keller"],
    "Autopilot": ["Jonny Saunders"]
}

for project, person_list in project_dict.items():
    for person in person_list:
        lab.ProjectUser.insert1({"project": project, "user": person}, skip_duplicates=True)

#%% Protocol info
lab.ProtocolType.insert1(["Animal: Mouse"], skip_duplicates=True)
protocol_columns = ["protocol", "protocol_type", "protocol_description"]
protocol_df = pd.DataFrame(columns=protocol_columns)

protocol_df.at[0, "protocol"] = "21-20"
protocol_df.at[0, "protocol_description"] = "Protocol for 2AFC, open-arena, and head-fixed" \
                                            "mouse tasks, including associated surgeries."
protocol_df.at[1, "protocol"] = "15-94"
protocol_df.at[1, "protocol_description"] = "Depricated protocol. Replaced by 21-20"
protocol_df.protocol_type = "Animal: Mouse"
lab.Protocol.insert(protocol_df, skip_duplicates=True)

