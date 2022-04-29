"""
    A collection of configuration parameters
"""
import utility_functions as uf

# This is the list of file locations that are plain-text sar logs
# Each entry is the storage point for a specific system's logs to be compared
# The system assumes the files will be stored in a format of:
# base_path/SYSTEM_NAME/file_prefix
# The specific file will be named according to the day of the month
# and added during selection and processing
file_locations = [
    "./data/system1/sar",
    "./data/system2/sar",
    "./data/system3/sar",
]

# Generate a list of systems from the above list for use in the interface
system_list = uf.create_system_list(file_locations)
default_system = system_list[0]
