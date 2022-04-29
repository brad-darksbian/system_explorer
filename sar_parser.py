import pandas as pd
from datetime import datetime, timedelta
import os

"""
    Parser for reading through a systat SAR log file
    Borrowed heavily from Abe Friesen's Parsar project at https://github.com/doyshinda/parsar

    Rewritten to handle server restarts and not take quite a linear
    approach to reading the file itself.

    parse_date and format_time are copied.  Parsefile is well influenced.
"""

# Header string definitions
cpu_header = "12:00:01 AM     CPU      %usr     %nice      %sys   %iowait    %steal      %irq     %soft    %guest    %gnice     %idle"
task_header = "12:00:01 AM    proc/s   cswch/s"
swap_stats_header = "12:00:01 AM  pswpin/s pswpout/s"
paging_stats_header = "12:00:01 AM  pgpgin/s pgpgout/s   fault/s  majflt/s  pgfree/s pgscank/s pgscand/s pgsteal/s    %vmeff"
io_stats_header = "12:00:01 AM       tps      rtps      wtps   bread/s   bwrtn/s"
mem_stats_header = "12:00:01 AM   frmpg/s   bufpg/s   campg/s"
mem_use_header = "12:00:01 AM kbmemfree kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit  kbactive   kbinact   kbdirty"
swap_use_header = "12:00:01 AM kbswpfree kbswpused  %swpused  kbswpcad   %swpcad"
hugepages_header = "12:00:01 AM kbhugfree kbhugused  %hugused"
inode_header = "12:00:01 AM dentunusd   file-nr  inode-nr    pty-nr"
load_header = "12:00:01 AM   runq-sz  plist-sz   ldavg-1   ldavg-5  ldavg-15   blocked"
tty_header = (
    "12:00:01 AM       TTY   rcvin/s   xmtin/s framerr/s prtyerr/s     brk/s   ovrun/s"
)
block_device_header = "12:00:01 AM       DEV       tps  rd_sec/s  wr_sec/s  avgrq-sz  avgqu-sz     await     svctm     %util"
network_activity_header = "12:00:01 AM     IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s"
network_error_header = "12:00:01 AM     IFACE   rxerr/s   txerr/s    coll/s  rxdrop/s  txdrop/s  txcarr/s  rxfram/s  rxfifo/s  txfifo/s"
nfs_client_header = (
    "12:00:01 AM    call/s retrans/s    read/s   write/s  access/s  getatt/s"
)
nfs_server_header = "12:00:01 AM   scall/s badcall/s  packet/s     udp/s     tcp/s     hit/s    miss/s   sread/s  swrite/s saccess/s sgetatt/s"
sockets_header = (
    "12:00:01 AM    totsck    tcpsck    udpsck    rawsck   ip-frag    tcp-tw"
)

# Function to parse the date
def parse_date(startdate_str):
    """parse the date SAR collection started"""
    formats = ["%y-%m-%d", "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]
    for fmt in formats:
        try:
            startdate = datetime.strptime(startdate_str, fmt)
            return startdate
        except ValueError:
            continue
    else:
        raise Exception("Unknown date format: %s" % startdate_str)


# Function to format the time / date for a SAR log file
def format_time(startdate, timestr, afternoon):
    """format the timstr as a datetime str"""
    datetime_str = "%s-%s-%s %s %s" % (
        startdate.year,
        startdate.month,
        startdate.day,
        timestr,
        afternoon,
    )
    timedate = datetime.strptime(datetime_str, "%Y-%m-%d %I:%M:%S %p")
    return datetime.strftime(timedate, "%Y-%m-%dT%H:%M:%S")


# Function to convert the returns to a dataframe
def convert_to_dataframe(master_list):
    df = pd.DataFrame(master_list[1:], columns=master_list[0])
    return df


# Main function to parse data from sar log file (text)
def parsefile(filename, section, dataframe=1):
    # Check for file to exist
    if not os.path.exists(filename):
        print("File not found")
        return

    # Container to hold the return values
    retvals = []

    # Figure out what report we're working with
    # On some, like CPU, we only want the aggregate row
    # This behavior can be modified if needs dictate.
    if section == "CPU":
        headermap = cpu_header
        filter_tag = ["all"]
    if section == "TASK":
        headermap = task_header
        exception = swap_stats_header.split()
    if section == "SWAP_STATS":
        headermap = swap_stats_header
    if section == "PAGE_STATS":
        headermap = paging_stats_header
    if section == "IO_STATS":
        headermap = io_stats_header
    if section == "MEM_STATS":
        headermap = mem_stats_header
    if section == "MEM_USE":
        headermap = mem_use_header
    if section == "SWAP_USE":
        headermap = swap_use_header
    if section == "HUGEPAGES":
        headermap = hugepages_header
    if section == "INODE":
        headermap = inode_header
    if section == "LOAD":
        headermap = load_header
    if section == "TTY":
        headermap = tty_header
    if section == "BLOCK":
        headermap = block_device_header
    if section == "NETWORK_ACTIVITY":
        headermap = network_activity_header
        filter_tag = ["eth0", "lo"]
    if section == "NETWORK_ERROR":
        headermap = network_error_header
        filter_tag = ["eth0", "lo"]
    if section == "NFS_CLIENT":
        headermap = nfs_client_header
    if section == "NFS_SERVER":
        headermap = nfs_server_header
    if section == "SOCKETS":
        headermap = sockets_header

    header_list = headermap.split()

    with open(filename, "r") as _file:
        # create a header string comprised of the base header + the time label
        headerstr = ["datetime"] + header_list[2:]
        retvals.append(headerstr)

        # Read very first line and extract into elements to get the date
        header = _file.readline()
        header = header.split()
        # Run the extracted date through the function and get result
        startdate = parse_date(header[3])

        pm = False
        target_area = 0
        for line in _file:
            # Make sure the line isn't a throwaway - if so, move on
            if line == "\n" or "Average" in line or "Summary" in line:
                continue

            # Grab the line and turn it into a list
            vals = line.split()

            # On the first run, we are at the top of the file
            # we need should be staring down at a header line
            # we need to compare and mark whether we care about the section or
            # whether it can be ignored
            if len(vals) == len(header_list):
                if section == "TASK" and vals[2:] == exception[2:]:
                    target_area = 0
                    continue

                if vals[2:] == header_list[2:]:
                    target_area = 1
                    continue

                if target_area == 1:
                    if section in {"CPU", "NETWORK_ACTIVITY", "NETWORK_ERROR"}:
                        if vals[2] not in filter_tag:
                            continue

                    if vals[1] == "PM":
                        if not pm:
                            pm = True
                    elif vals[1] == "AM" and pm:
                        startdate = startdate + timedelta(days=1)
                        pm = False

                    return_candidate = [
                        format_time(startdate, vals[0], vals[1])
                    ] + vals[2:]
                    retvals.append(return_candidate)
            else:
                target_area = 0
                continue

    if dataframe == 1:
        return_var = convert_to_dataframe(retvals)
    else:
        return_var = retvals

    return return_var


# function to examine log file for reboots
# Substantially similar to above
def rebootID(filename):
    # Check for file to exist
    if not os.path.exists(filename):
        print("File not found")
        return

    # Container to hold the return values
    retvals = []

    with open(filename, "r") as _file:
        header = _file.readline()
        header = header.split()
        startdate = parse_date(header[3])

        pm = False
        for line in _file:
            if line == "\n" or "Average" in line or "Summary" in line:
                continue

            vals = line.split()

            if vals[3] == "RESTART":
                if vals[1] == "PM":
                    if not pm:
                        pm = True
                elif vals[1] == "AM" and pm:
                    startdate = startdate + timedelta(days=1)
                    pm = False

                return_candidate = [format_time(startdate, vals[0], vals[1])] + vals[2:]
                retvals.append(return_candidate)
            else:
                continue

        return_var = retvals

    return return_var


#############################################################################
# Backstop
#############################################################################
if __name__ == "__main__":
    print("sar_parser has nothing to run directly")
