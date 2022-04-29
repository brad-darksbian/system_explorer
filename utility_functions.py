"""
    This file contains all the various functions that are used in formatting
    and processing that don't quite go elsewhere.

    It's an organizational thing...
"""
import pandas as pd
import sar_parser as sp

# Function to set the right datatypes in a dataframe
def set_types(df):
    column_names = df.columns.values.tolist()
    # Loop through the columns to set the correct types
    count = 0
    while count < (len(column_names) - 1):
        if count > 0:
            # If we are on the first column of the following sections
            # skip the type set.  These values are usually text identifiers.
            if (
                column_names[count] == "CPU"
                or column_names[count] == "DEV"
                or column_names[count] == "IFACE"
                or column_names[count] == "TTY"
                or column_names[count] == "system"
            ):
                count += 1
                continue
            df[df.columns[count]] = df[df.columns[count]].apply(pd.to_numeric)
        count += 1

    return df


# create the actual file list to work from
def generate_file_list(file_list, date):
    listing = []
    for i in file_list:
        listing.append(i + date)

    return listing


# To populate system selector dropdown
def create_system_list(file_list):
    listing = []
    for i in file_list:
        path_list = i.split("/", -1)
        system_name = path_list[2]
        listing.append(system_name)

    return listing


# Create complete section-specific dataframes
# This is the main list of sections we can extract
# The actual list is dependent on how the system is configured for logging.
# "CPU", "TASK", "SWAP_STATS", "PAGE_STATS", "IO_STATS", "MEM_STATS", "MEM_USE",
# "SWAP_USE", "HUGEPAGES", "INODE", "LOAD", "TTY", "BLOCK", "NETWORK_ACTIVITY",
# "NETWORK_ERROR", "NFS_CLIENT", "NFS_SERVER", "SOCKETS"


def get_section_all_files(file_list, date, section):
    system_list = []
    df = pd.DataFrame()

    logs = generate_file_list(file_list, date)
    for i in logs:
        path_list = i.split("/", -1)
        system_name = path_list[2]
        system_list.append(system_name)

        data = sp.parsefile(i, section)
        data["system"] = system_name
        df = pd.concat([df, data])
        df.reset_index(drop=True, inplace=True)

    return df


# Create a dataframe of identified restarts
def get_reboots(file_list, date):
    system_list = []
    df = pd.DataFrame()

    logs = generate_file_list(file_list, date)
    for i in logs:
        path_list = i.split("/", -1)
        system_name = path_list[2]
        system_list.append(system_name)

        rb_list = sp.rebootID(i)
        reboot_listing = pd.DataFrame(
            rb_list,
            columns=["datetime", "os", "action"],
        )
        reboot_listing["system"] = system_name
        reboot_listing["system"] = reboot_listing["system"].apply(str)
        df = pd.concat([df, reboot_listing])
        df.reset_index(drop=True, inplace=True)

    return df


# Add some data to the LOAD section dataframe
def load_stats(load_df):
    load_df = set_types(load_df)
    df = load_df.copy()
    df["pct_plist"] = (df["runq-sz"] / df["plist-sz"]) * 100
    df["pct_blocked"] = (df["blocked"] / df["plist-sz"]) * 100

    return df


#############################################################################
# Backstop
#############################################################################
if __name__ == "__main__":
    print("Nothing to do")
