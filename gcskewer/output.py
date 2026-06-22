'''
reading and writing for gcskewer
    functions:
        read_file(filename:str, _format: str)-> List[str], List[str]
        write_csv(df: DataFrame, name:str) -> None
        plot_data(df: DataFrame, name: str) -> None
        plot_svg(df: DataFrame, name: str) -> None
        print_to_system(string_to_print: str) -> None
'''
import csv
import os

from datetime import datetime
from typing import List, Dict

from Bio import SeqIO
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from gcskewer.classes.dataclasses import Frame

def read_file(filename:str, _format: str) -> (List[str], List[str]):
    '''
    read file with biopython and reurn record names and sequences as two lists
        arguments:
            filename: path to the file to be read
            _format: string specifying 'fasta' or 'genbank' for BioPython
        returns:
            records: a dictionary of {record.id : record.seq}
    '''
    print_to_system('Reading fasta: ' + filename)
    records = {}
    for seq_record in SeqIO.parse(filename, _format):
        records.update({seq_record.id : seq_record.seq})
    return records

def write_gcframes_to_csv(frames: List[Frame], filename:str) -> None:
    '''
    writes the df to a .csv
        arguments: 
            frames: a list of Frame objects
            name: the name of the record the dataframe was generated from
        returns:
            None
    '''
    lines = [Frame.header]
    lines.extend([frame.get_line() for frame in frames])
    print_to_system('Writing to ' + filename)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(lines)

def plot_html(frames: Dict, filename: str, variables: set[str]) -> None:
    '''
    plot the data to an .html file with plotly
         arguments:
            frames: the dictionary of frame data
            name: the name of the record from which the df originated
        returns:
            None
    '''
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    ### SKEW ###
    if 'gc_skew' in variables:
        fig.add_trace(
            go.Scatter(x=frames['midpoint'], y=frames['gc_skew'], name='GC Skew'), secondary_y=False
            )
    if 'at_skew' in variables:
        fig.add_trace(
            go.Scatter(x=frames['midpoint'], y=frames['at_skew'], name='AT Skew'), secondary_y=False
            )
    if 'cummulative_gc_skew' in variables:
        fig.add_trace(
            go.Scatter(
                x=frames['midpoint'], y=frames['cummulative_gc_skew'], name='Cummulative GC Skew'
                ), secondary_y=True
            )
    if 'cummulative_at_skew' in variables:
        fig.add_trace(
            go.Scatter(
                x=frames['midpoint'], y=frames['cummulative_at_skew'], name='Cummulative AT Skew'
                ), secondary_y=True
            )
    ### CONTENT ###
    if 'gc_content' in variables:
        fig.add_trace(
            go.Scatter(
                x=frames['midpoint'], y=frames['gc_content'], name='GC Content'
                ), secondary_y=False
            )
    if 'at_content' in variables:
        fig.add_trace(
            go.Scatter(
                x=frames['midpoint'], y=frames['at_content'], name='AT Content'
                ), secondary_y=False
            )
    fig.write_html(filename)
    print_to_system('Plot saved to ' + filename)

def plot_svg(frames: Frame, filename: str, variables: set[str]) -> None:
    '''
    plot svg from dataframe
        arguments:
            frames: the dictionary of frame data
            name: the name of the record from which the df originated
        returns:
            None
    '''
    lines = []
    labels = []
    lines2 = []
    labels2 = []
    _, ax1 = plt.subplots()
    ax1.set_xlabel('Position')
    ax1.set_title('GC skew of ' + os.path.splitext(os.path.basename(filename))[0])
    if {'gc_skew', 'at_skew', 'gc_content', 'at_content'}.intersection(variables):
        ### AXIS 1: SKEW AND CONTENT ###
        if 'gc_skew' in variables:
            ax1.plot(frames['midpoint'], frames['gc_skew'], label="GC skew", color='#56b4e9')
        if 'at_skew' in variables:
            ax1.plot(frames['midpoint'], frames['at_skew'], label="AT skew", color='#e69f00')
        if 'gc_content' in variables:
            ax1.plot(frames['midpoint'], frames['gc_content'], label="GC content", color='#0072B2')
        if 'at_content' in variables:
            ax1.plot(frames['midpoint'], frames['at_content'], label="AT content", color='#f0e442')
        ax1.set_ylabel('Skew/Content')
        lines, labels = ax1.get_legend_handles_labels()
    else:
        ax1.set_yticks([]) # remove left Y ticks
    if {'cummulative_gc_skew', 'cummulative_at_skew'}.intersection(variables):
        ### AXIS2: CUMMULATIVE SKEW ###S
        ax2 = plt.twinx()
        if 'cummulative_gc_skew' in variables:
            ax2.plot(
                frames['midpoint'], frames['cummulative_gc_skew'],
                label="Cumulative GC skew",color='#009e73'
                )
        if 'cummulative_at_skew' in variables:
            ax2.plot(
                frames['midpoint'], frames['cummulative_at_skew'],
                label="Cumulative AT skew", color='#cc79a7'
                )
        ax2.set_ylabel('Cummulative Skew')
        lines2, labels2 = ax2.get_legend_handles_labels()
    #legend
    plt.legend(lines + lines2, labels + labels2)
    plt.savefig(filename)

def print_to_system(string_to_print: str) -> None:
    '''
    prints a line to the terminal with date and time
        arguments:
            string_to_print: the text to be printed
        returns:
            None
    '''
    now = datetime.now()
    current_time = now.strftime("[%H:%M:%S]: ")
    print(current_time + string_to_print)
