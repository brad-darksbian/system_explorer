import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import configs as conf
import charting_functions as cf
import utility_functions as uf
import layout_configs as lc


#############################################################################
# Style modifications
#############################################################################
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem"
    #'background-color': '#f8f9fa'
}

CONTENT_STYLE = {
    "margin-left": "12rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

TEXT_STYLE = {"textAlign": "center"}

DROPDOWN_STYLE = {"textAlign": "left"}

TABLE_BORDER_STYLE = {
    #'background-color': '#000',
    "border": "1px solid #444",
    "color": "#fff",
    "font-size": ".8rem",
    "font-weight": "500",
    "whiteSpace": "normal",
    "height": "auto",
}

#############################################################################
# Sidebar and Navigation
#############################################################################
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("System View", href="/system"),
                dbc.DropdownMenuItem("Comp CPU", href="/compcpu"),
                dbc.DropdownMenuItem("Comp MEM", href="/compmem"),
                dbc.DropdownMenuItem("Comp SWAP", href="/compswap"),
                dbc.DropdownMenuItem("Comp LOAD", href="/compload"),
                dbc.DropdownMenuItem("Comp IO", href="/compio"),
                dbc.DropdownMenuItem("Comp NETWORK", href="/compnet"),
            ],
            nav=True,
            in_navbar=True,
            label="Menu",
        ),
    ],
    brand="",
    brand_href="",
    color="dark",
    dark=True,
)


sidebar = html.Div(
    [
        html.H4("System Log"),
        html.H4("Analysis"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        navbar,
                    )
                ),
                dbc.Col(),
            ],
            no_gutters=True,
        ),
        html.Hr(),
    ],
    style=SIDEBAR_STYLE,
)

#############################################################################
# Content Section Definitions
#############################################################################
# This section is used to build out the layout row-by-row and aggregated
# in the layout section below.

# Create drop-down selector and initial date picker
# date picker is currently unused, but may add later
day_list = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
]

# Select the system to detail
system_select = dbc.Row(
    [
        dbc.Col(
            md=2,
        ),
        dbc.Col(
            [
                html.Div(
                    [
                        "System Select:",
                        dcc.Dropdown(
                            id="system",
                            options=[
                                {"label": i, "value": i} for i in conf.system_list
                            ],
                            value=conf.default_system,
                        ),
                    ],
                    className="dash-bootstrap",
                ),
            ],
            md=3,
        ),
        dbc.Col(
            md=2,
        ),
        dbc.Col(
            [
                html.Div(
                    [
                        "Date Select:",
                        dcc.Dropdown(
                            id="day-picker",
                            options=[{"label": i, "value": i} for i in day_list],
                            value="01",
                        ),
                    ],
                    className="dash-bootstrap",
                ),
            ],
            md=3,
        ),
        dbc.Col(
            md=2,
        ),
    ]
)


#############################################################################
# Single System Configs
#############################################################################
# Dynamic charts are provided from callbacks
sys_cpu = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="sys-cpu",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=12,
        ),
    ]
)

sys_mem = dbc.Row(
    [
        dbc.Col(
            html.Div(
                dcc.Graph(
                    id="sys-mem-use",
                    style={"height": "45vh"},
                    config=lc.tool_config,
                ),
            ),
            md=6,
        ),
        dbc.Col(
            html.Div(
                dcc.Graph(
                    id="sys-mem-stats",
                    style={"height": "45vh"},
                    config=lc.tool_config,
                ),
            ),
            md=6,
        ),
    ],
    className="g-0",
)

sys_swap = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="sys-swap-use",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="sys-swap-stats",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ],
    className="g-0",
)

sys_load = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="sys-load",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=12,
        ),
    ]
)

sys_io_task = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="sys-io",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="sys-task",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ],
    className="g-0",
)

sys_paging = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="sys-page",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="sys-h-page",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ],
    className="g-0",
)

sys_network = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="sys-network",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=12,
        ),
    ]
)

#############################################################################
# Comparative System Configs
#############################################################################
# We only need the day selector for the system comparison pages
day_select = dbc.Row(
    [
        dbc.Col(
            md=2,
        ),
        dbc.Col(
            [
                html.Div(
                    [
                        "Date Select:",
                        dcc.Dropdown(
                            id="comp-day-picker",
                            options=[{"label": i, "value": i} for i in day_list],
                            value="01",
                        ),
                    ],
                    className="dash-bootstrap",
                ),
            ],
            md=3,
        ),
        dbc.Col(
            md=2,
        ),
    ]
)


# Let's break this up by page just to keep things organized
#############################################################################
# CPU
#############################################################################
# usr, sys, iowait, soft, nice, idle
comp_cpu1 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="cpu-usr",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="cpu-sys",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ],
    className="g-0",
)

comp_cpu2 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="cpu-iowait",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="cpu-soft",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ],
    className="g-0",
)

comp_cpu3 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="cpu-idle",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="cpu-nice",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ],
    className="g-0",
)

#############################################################################
# Memory
#############################################################################
# kbmemfree, kbmemused, kbbuffers, kbcached, kbcommit, kbactive, kbinact, kbdirty
comp_mem1 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="mem-kbmemfree",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="mem-kbmemused",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

comp_mem2 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="mem-kbbuffers",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="mem-kbcached",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

comp_mem3 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="mem-kbcommit",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="mem-kbdirty",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

comp_mem4 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="mem-kbactive",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="mem-kbinact",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

#############################################################################
# SWAP
#############################################################################
# kbswpfree, kbswpused, %swpused, kbswpcad, %swpcad, pswpin/s, pswpout/s
comp_swap2 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="swap-kbswpfree",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="swap-kbswpused",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

comp_swap3 = dbc.Row(
    [
        dbc.Col(
            md=2,
        ),
        dbc.Col(
            dcc.Graph(
                id="swap-kbswpcad",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=8,
        ),
        dbc.Col(
            md=2,
        ),
    ]
)

comp_swap1 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="swap-swpused",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="swap-swpcad",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

comp_swap4 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="swap-pswpin",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="swap-pswpout",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

#############################################################################
# LOAD
#############################################################################
# ldavg-1, ldavg-15, pct_plist, pct_blocked

comp_load1 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="load-ldavg-1",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="load-ldavg-15",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

comp_load2 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="load-pct_plist",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="load-pct_blocked",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

#############################################################################
# IO
#############################################################################
# ldavg-1, ldavg-15, pct_plist, pct_blocked

comp_io1 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="io-rtps",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="io-wtps",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

comp_io2 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="io-tps",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=12,
        ),
    ]
)

comp_io3 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="io-breads",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
        dbc.Col(
            dcc.Graph(
                id="io-bwrtns",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=6,
        ),
    ]
)

#############################################################################
# NETWORK
#############################################################################
comp_net1 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="net-rxpck",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=12,
        ),
    ]
)

comp_net2 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="net-txpck",
                style={"height": "45vh"},
                config=lc.tool_config,
            ),
            md=12,
        ),
    ]
)

####################################################
# Layout Creation Section
####################################################
system = html.Div(
    [
        system_select,
        sys_cpu,
        sys_mem,
        sys_swap,
        sys_load,
        sys_paging,
        sys_io_task,
        sys_network,
    ],
    style=CONTENT_STYLE,
)

comp_cpu = html.Div(
    [
        day_select,
        comp_cpu1,
        comp_cpu2,
        comp_cpu3,
    ],
    style=CONTENT_STYLE,
)

comp_mem = html.Div(
    [
        day_select,
        comp_mem1,
        comp_mem2,
        comp_mem3,
        comp_mem4,
    ],
    style=CONTENT_STYLE,
)

comp_swap = html.Div(
    [
        day_select,
        comp_swap1,
        comp_swap2,
        comp_swap3,
        comp_swap4,
    ],
    style=CONTENT_STYLE,
)

comp_load = html.Div(
    [
        day_select,
        comp_load1,
        comp_load2,
    ],
    style=CONTENT_STYLE,
)

comp_io = html.Div(
    [
        day_select,
        comp_io1,
        comp_io2,
        comp_io3,
    ],
    style=CONTENT_STYLE,
)

comp_net = html.Div(
    [
        day_select,
        comp_net1,
        comp_net2,
    ],
    style=CONTENT_STYLE,
)

#############################################################################
# Application parameters
#############################################################################
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.CYBORG],
)
app.config.suppress_callback_exceptions = True
app.title = "System Performance Log Analysis"
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), sidebar, html.Div(id="page-content")]
)

# Multi-page selector callback
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/compcpu":
        return comp_cpu
    if pathname == "/compmem":
        return comp_mem
    if pathname == "/compswap":
        return comp_swap
    if pathname == "/compload":
        return comp_load
    if pathname == "/compnet":
        return comp_net
    if pathname == "/compio":
        return comp_io
    else:
        return system


####################################################
#  Callbacks - charts
####################################################
# All charts are generated dynamically so this section gets pretty long

# This is the main list of sections we can extract
# "CPU", "TASK", "SWAP_STATS", "PAGE_STATS", "IO_STATS", "MEM_STATS", "MEM_USE",
# "SWAP_USE", "HUGEPAGES", "INODE", "LOAD", "TTY", "BLOCK", "NETWORK_ACTIVITY",
# "NETWORK_ERROR", "NFS_CLIENT", "NFS_SERVER", "SOCKETS"

####################################################
#  Single System
####################################################
# System-level Reports
# CPU
@app.callback(
    dash.dependencies.Output("sys-cpu", "figure"),
    [
        dash.dependencies.Input("system", "value"),
        dash.dependencies.Input("day-picker", "value"),
    ],
)
def cpu(system, day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "CPU")
    fig = cf.monitoring_line_chart(df, system, "CPU DATA", 0, rb_df)
    return fig


# Memory stats
@app.callback(
    dash.dependencies.Output("sys-mem-stats", "figure"),
    [
        dash.dependencies.Input("system", "value"),
        dash.dependencies.Input("day-picker", "value"),
    ],
)
def mem(system, day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "MEM_STATS")
    fig = cf.monitoring_line_chart(df, system, "MEMORY STATS", 0, rb_df)
    return fig


# Memory use
@app.callback(
    dash.dependencies.Output("sys-mem-use", "figure"),
    [
        dash.dependencies.Input("system", "value"),
        dash.dependencies.Input("day-picker", "value"),
    ],
)
def mem(system, day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "MEM_USE")
    fig = cf.monitoring_line_chart(df, system, "MEMORY USE", 0, rb_df)
    return fig


# Swap stats
@app.callback(
    dash.dependencies.Output("sys-swap-stats", "figure"),
    [
        dash.dependencies.Input("system", "value"),
        dash.dependencies.Input("day-picker", "value"),
    ],
)
def swap(system, day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "SWAP_STATS")
    fig = cf.monitoring_line_chart(df, system, "SWAP STATS", 0, rb_df)
    return fig


# Swap use
@app.callback(
    dash.dependencies.Output("sys-swap-use", "figure"),
    [
        dash.dependencies.Input("system", "value"),
        dash.dependencies.Input("day-picker", "value"),
    ],
)
def swap(system, day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "SWAP_USE")
    fig = cf.monitoring_line_chart(df, system, "SWAP USE", 0, rb_df)
    return fig


# Load
@app.callback(
    dash.dependencies.Output("sys-load", "figure"),
    [
        dash.dependencies.Input("system", "value"),
        dash.dependencies.Input("day-picker", "value"),
    ],
)
def load(system, day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "LOAD")
    load_df = uf.load_stats(df)
    fig = cf.monitoring_line_chart(load_df, system, "LOAD STATS", 0, rb_df)
    return fig


# IO
@app.callback(
    dash.dependencies.Output("sys-io", "figure"),
    [
        dash.dependencies.Input("system", "value"),
        dash.dependencies.Input("day-picker", "value"),
    ],
)
def load(system, day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "IO_STATS")
    fig = cf.monitoring_line_chart(df, system, "I/O STATS", 0, rb_df)
    return fig


# Task
@app.callback(
    dash.dependencies.Output("sys-task", "figure"),
    [
        dash.dependencies.Input("system", "value"),
        dash.dependencies.Input("day-picker", "value"),
    ],
)
def load(system, day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "TASK")
    fig = cf.monitoring_line_chart(df, system, "TASK STATS", 0, rb_df)
    return fig


# Page
@app.callback(
    dash.dependencies.Output("sys-page", "figure"),
    [
        dash.dependencies.Input("system", "value"),
        dash.dependencies.Input("day-picker", "value"),
    ],
)
def load(system, day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "PAGE_STATS")
    fig = cf.monitoring_line_chart(df, system, "PAGE STATS", 0, rb_df)
    return fig


# Inodes
@app.callback(
    dash.dependencies.Output("sys-h-page", "figure"),
    [
        dash.dependencies.Input("system", "value"),
        dash.dependencies.Input("day-picker", "value"),
    ],
)
def load(system, day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "INODE")
    fig = cf.monitoring_line_chart(df, system, "INODE STATS", 0, rb_df)
    return fig


# Network Activity
@app.callback(
    dash.dependencies.Output("sys-network", "figure"),
    [
        dash.dependencies.Input("system", "value"),
        dash.dependencies.Input("day-picker", "value"),
    ],
)
def load(system, day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "NETWORK_ACTIVITY")
    df1 = df.loc[df["IFACE"] == "eth0"]
    fig = cf.monitoring_line_chart(df1, system, "NETWORK ACTIVITY STATS", 0, rb_df)
    return fig


####################################################
#  Comparisons
####################################################
# CPU
# usr, sys, iowait, soft, nice, idle
@app.callback(
    dash.dependencies.Output("cpu-usr", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def cpu_usr(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "CPU")
    fig = cf.comparison_line_chart(df, "%usr", "CPU", 0, rb_df)
    return fig


# sys
@app.callback(
    dash.dependencies.Output("cpu-sys", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def cpu_sys(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "CPU")
    fig = cf.comparison_line_chart(df, "%sys", "CPU", 0, rb_df)
    return fig


# iowait
@app.callback(
    dash.dependencies.Output("cpu-iowait", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def cpu_iowait(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "CPU")
    fig = cf.comparison_line_chart(df, "%iowait", "CPU", 0, rb_df)
    return fig


# soft
@app.callback(
    dash.dependencies.Output("cpu-soft", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def cpu_soft(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "CPU")
    fig = cf.comparison_line_chart(df, "%soft", "CPU", 0, rb_df)
    return fig


# idle
@app.callback(
    dash.dependencies.Output("cpu-idle", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def cpu_idle(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "CPU")
    fig = cf.comparison_line_chart(df, "%idle", "CPU", 0, rb_df)
    return fig


# nice
@app.callback(
    dash.dependencies.Output("cpu-nice", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def cpu_nice(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "CPU")
    fig = cf.comparison_line_chart(df, "%nice", "CPU", 0, rb_df)
    return fig


# memory
# kbmemfree, kbmemused, kbbuffers, kbcached, kbcommit, kbactive, kbinact, kbdirty
@app.callback(
    dash.dependencies.Output("mem-kbmemfree", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def mem_free(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "MEM_USE")
    fig = cf.comparison_line_chart(df, "kbmemfree", "MEM USE", 0, rb_df)
    return fig


# kbmemused
@app.callback(
    dash.dependencies.Output("mem-kbmemused", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def mem_used(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "MEM_USE")
    fig = cf.comparison_line_chart(df, "kbmemused", "MEM USE", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("mem-kbbuffers", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def mem_buffers(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "MEM_USE")
    fig = cf.comparison_line_chart(df, "kbbuffers", "MEM USE", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("mem-kbcached", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def mem_cached(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "MEM_USE")
    fig = cf.comparison_line_chart(df, "kbcached", "MEM USE", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("mem-kbcommit", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def mem_commit(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "MEM_USE")
    fig = cf.comparison_line_chart(df, "kbcommit", "MEM USE", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("mem-kbactive", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def mem_active(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "MEM_USE")
    fig = cf.comparison_line_chart(df, "kbactive", "MEM USE", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("mem-kbinact", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def mem_inactive(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "MEM_USE")
    fig = cf.comparison_line_chart(df, "kbinact", "MEM USE", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("mem-kbdirty", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def mem_dirty(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "MEM_USE")
    fig = cf.comparison_line_chart(df, "kbdirty", "MEM USE", 0, rb_df)
    return fig


# Swap
# kbswpfree, kbswpused, %swpused, kbswpcad, %swpcad, pswpin/s, pswpout/s
@app.callback(
    dash.dependencies.Output("swap-kbswpfree", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def swap_free(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "SWAP_USE")
    fig = cf.comparison_line_chart(df, "kbswpfree", "SWAP USE", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("swap-kbswpused", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def swap_used(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "SWAP_USE")
    fig = cf.comparison_line_chart(df, "kbswpused", "SWAP USE", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("swap-swpused", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def swap_used_pct(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "SWAP_USE")
    fig = cf.comparison_line_chart(df, "%swpused", "SWAP USE", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("swap-kbswpcad", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def swap_cad(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "SWAP_USE")
    fig = cf.comparison_line_chart(df, "kbswpcad", "SWAP USE", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("swap-swpcad", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def swap_cad_pct(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "SWAP_USE")
    fig = cf.comparison_line_chart(df, "%swpcad", "SWAP USE", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("swap-pswpin", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def swap_in(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "SWAP_STATS")
    fig = cf.comparison_line_chart(df, "pswpin/s", "SWAP STATS", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("swap-pswpout", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def swap_out(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "SWAP_STATS")
    fig = cf.comparison_line_chart(df, "pswpout/s", "SWAP STATS", 0, rb_df)
    return fig


# Load
# ldavg-1, ldavg-15, pct_plist, pct_blocked
@app.callback(
    dash.dependencies.Output("load-ldavg-1", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def load_avg_1(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "LOAD")
    fig = cf.comparison_line_chart(df, "ldavg-1", "LOAD", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("load-ldavg-15", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def load_avg_15(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "LOAD")
    fig = cf.comparison_line_chart(df, "ldavg-15", "LOAD", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("load-pct_plist", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def load_plist_pct(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "LOAD")
    load_df = uf.load_stats(df)
    fig = cf.comparison_line_chart(load_df, "pct_plist", "LOAD", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("load-pct_blocked", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def load_blocked_pct(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "LOAD")
    load_df = uf.load_stats(df)
    fig = cf.comparison_line_chart(load_df, "pct_blocked", "LOAD", 0, rb_df)
    return fig


# IO
# tps, rtps, wtps, bread/s, bwrtn/s
@app.callback(
    dash.dependencies.Output("io-tps", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def io_tps(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "IO_STATS")
    fig = cf.comparison_line_chart(df, "tps", "IO", 0, rb_df)
    return fig


# rtps
@app.callback(
    dash.dependencies.Output("io-rtps", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def io_rtps(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "IO_STATS")
    fig = cf.comparison_line_chart(df, "rtps", "IO", 0, rb_df)
    return fig


# wtps
@app.callback(
    dash.dependencies.Output("io-wtps", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def io_wtps(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "IO_STATS")
    fig = cf.comparison_line_chart(df, "wtps", "IO", 0, rb_df)
    return fig


# bread/s
@app.callback(
    dash.dependencies.Output("io-breads", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def io_bread(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "IO_STATS")
    fig = cf.comparison_line_chart(df, "bread/s", "IO", 0, rb_df)
    return fig


# bwrtn/s
@app.callback(
    dash.dependencies.Output("io-bwrtns", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def io_bwrtn(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "IO_STATS")
    fig = cf.comparison_line_chart(df, "bwrtn/s", "IO", 0, rb_df)
    return fig


# Network
@app.callback(
    dash.dependencies.Output("net-rxpck", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def net_rxpck(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "NETWORK_ACTIVITY")
    df1 = df.loc[df["IFACE"] == "eth0"]
    fig = cf.comparison_line_chart(df1, "rxpck/s", "NETWORK", 0, rb_df)
    return fig


@app.callback(
    dash.dependencies.Output("net-txpck", "figure"),
    [
        dash.dependencies.Input("comp-day-picker", "value"),
    ],
)
def net_txpck(day):
    rb_df = uf.get_reboots(conf.file_locations, day)
    df = uf.get_section_all_files(conf.file_locations, day, "NETWORK_ACTIVITY")
    df1 = df.loc[df["IFACE"] == "eth0"]
    fig = cf.comparison_line_chart(df1, "txpck/s", "NETWORK", 0, rb_df)
    return fig


###################################################
# Server Run
###################################################
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8090, dev_tools_hot_reload=True)
