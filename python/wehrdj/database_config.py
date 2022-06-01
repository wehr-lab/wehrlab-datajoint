import datajoint as dj

#%% Setup database prefixes for schema
dj.config["custom"] = {"database.prefix": "wehr_"}
dj.config.save_local()

#%% Establish paths to raw data from openEphys/clustered kilosort data
# Consider making these paths variables that are based on a config file unique
# to each computer. Makes it more easily deployable

