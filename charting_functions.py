"""
    This file is a good place to aggregate all the charting functions 
    in one place.  These functions can then be called directly from
    the main application and displayed.
"""

import pandas as pd
import numpy as np
import utility_functions as uf
import layout_configs as lc
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

pd.options.plotting.backend = "plotly"
pio.templates.default = "plotly_dark"

#############################################################################
# Charts
#############################################################################
# template chart to display the raw data in comparison - one system
def monitoring_line_chart(df, system_name, title_text, display, reboot_df):
    """
    df: the dataframe holding the section data
    system_name:  The specific system to detail from the configured list
    title_text: the title of the chart
    display: output a chart directly or not - useful for debugging
    reboot_df:  dataframe holding reboot data
    """
    # Create a new dataframe for just the system requested
    df1 = df.loc[df["system"] == system_name].copy()

    # Get list of column names since we know nothing about the dataframe
    column_names = df1.columns.values.tolist()
    df1 = uf.set_types(df1)

    fig = go.Figure(layout=lc.layout_simple)

    # Create a trace for all relevant data columns
    for i in column_names[1:]:
        # Skip label columns
        if i == "CPU" or i == "system" or i == "DEV" or i == "IFACE" or i == "TTY":
            continue

        # I wanted something a bit different for CPU charting which is
        # a stacked group of values.
        if (
            i == "CPU"
            or i == "%usr"
            or i == "%nice"
            or i == "%sys"
            or i == "%iowait"
            or i == "%steal"
            or i == "%irq"
            or i == "%soft"
            or i == "%guest"
            or i == "%gnice"
            or i == "%idle"
        ):
            fig.add_traces(
                go.Scatter(
                    x=df1.datetime,
                    y=df1[i],
                    name=i,
                    line_width=2,
                    stackgroup="one",
                )
            )
        else:
            fig.add_traces(
                go.Scatter(
                    x=df1.datetime,
                    y=df1[i],
                    name=i,
                    line_width=2,
                    fill="tozeroy",
                )
            )

    # Mark where the reboot - if any occurred
    for row in reboot_df.iterrows():
        fig.add_vline(
            x=row[0],
            line_width=3,
            line_dash="dash",
            line_color="aqua",
        )
        fig.add_annotation(
            text="Rebooted System: " + row[3],
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.95,
            showarrow=False,
        )
    # create the labels for the chart and set the drawing color
    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title=title_text + ": " + df1.iloc[0].system,
        xaxis_title="",
        yaxis_title="",
    )

    if display == 1:
        fig.show(config=lc.tool_config)

    return fig


# Function to compare multiple systems on a section and a parameter
def comparison_line_chart(df, param, title_text, display, reboot_df):
    """
    df: the dataframe holding the section data
    param: the dataframe column(s) to be displayed
    title_text: the title of the chart
    display: output a chart directly or not - useful for debugging
    reboot_df:  dataframe holding reboot data

    This function is not so effective with packed sections like BLOCK, NETWORK, TTY
    CPU is an exception because the collector pulls the aggregate
    """
    df = uf.set_types(df)

    fig = px.line(
        df,
        x="datetime",
        y=param,
        color="system",
    )

    # Mark where the reboot - if any occurred
    for index, row in reboot_df.iterrows():
        fig.add_vline(
            x=row[0],
            line_width=3,
            line_dash="dash",
            line_color="aqua",
        )
        fig.add_annotation(
            text="Rebooted System: " + row[3],
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.95,
            showarrow=False,
        )
    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title=title_text + ": " + param,
        xaxis_title="",
        yaxis_title="",
    )

    if display == 1:
        fig.show(config=lc.tool_config)

    return fig


# Function to compare multiple systems on a section and a parameter grouped
# by secondary differentiator
def comparison_grouped_line_chart(df, param, group, title_text, display, reboot_df):
    """
    df: the dataframe holding the section data
    param: the dataframe column(s) to be displayed
    title_text: the title of the chart
    display: output a chart directly or not - useful for debugging
    reboot_df:  dataframe holding reboot data

    This function is not so effective with packed sections like BLOCK, NETWORK, TTY
    CPU is an exception because the collector pulls the aggregate
    """
    df = uf.set_types(df)

    fig = px.line(
        df,
        x="datetime",
        y=param,
        line_group=group,
        color="system",
    )

    # Mark where the reboot - if any occurred
    for index, row in reboot_df.iterrows():
        fig.add_vline(
            x=row[0],
            line_width=3,
            line_dash="dash",
            line_color="aqua",
        )
        fig.add_annotation(
            text="Rebooted System: " + row[3],
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.95,
            showarrow=False,
        )
    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title=title_text + ": " + param,
        xaxis_title="",
        yaxis_title="",
    )

    if display == 1:
        fig.show(config=lc.tool_config)

    return fig


#############################################################################
# Backstop
#############################################################################
if __name__ == "__main__":
    print("Nothing to do")
