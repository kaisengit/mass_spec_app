# 2024-09 Kai-Michael Kammer
"""
Imports strings from the os environment
Contains global string declarations
"""
import os

DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE_URL_TEST = os.environ["DATABASE_URL_TEST"]


STR_COMPOUNDS = "compounds"
STR_MEASURED_COMPOUNDS = "measured_compounds"
STR_RETENTION_TIME = "retention_time"
STR_ADDUCTS = "adducts"
STR_TOOLS = "tools"
