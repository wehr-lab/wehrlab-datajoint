"""
File containing path variables that may vary from system to system. Ultimately,
this should probably be moved outside the package and be added in some diectory
that is appeneded to the system path so it isn't tracked on git
"""

import pathlib

EPHYS_DATA_PATH = pathlib.PurePath("/Users/Matt/Desktop/Research/Wehr/wehr_nas_mount")

DLC_CONFIG_PATH = pathlib.PurePath("/Users/Matt/Desktop/Research/Wehr/wehr_nas_mount")

OUTPUT_SAVE_LOCATION = pathlib.PurePath("/Users/Matt/Desktop/Research/Wehr/data")
