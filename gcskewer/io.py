'''
reading and writing for gcskewer
    functions:
        read_file(filename:str, _format: str)-> List[str], List[str]
        write_csv(df: DataFrame, name:str) -> None
        plot_data(df: DataFrame, name: str) -> None
        plot_svg(df: DataFrame, name: str) -> None
        print_to_system(string_to_print: str) -> None
'''
from datetime import datetime
from typing import List

import matplotlib.pyplot as plt
import plotly.graph_objects as go

from Bio import SeqIO
from pandas import DataFrame
from plotly.subplots import make_subplots

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

def write_csv(df: DataFrame, name:str) -> None:
    '''
    writes the df to a .csv
        arguments: 
            df: the dataframe to write
            name: the name of the record the dataframe was generated from
        returns:
            None
    '''
    file_name = name + '.csv'
    print_to_system('Writing to ' + file_name)
    df.to_csv(file_name, index = False)

def plot_data(df: DataFrame, name: str) -> None:
    '''
    plot the data to an .html file with plotly
         arguments:
            df: the datagrame with gc skew data
            name: the name of the record from which the df originated
        returns:
            None
    '''
    #create an empty figure with a secondary y axis!
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    #Now individually add traces
    fig.add_trace(
        go.Scatter(x=df['mid point'], y=df['gc skew'], name='GC Skew'), secondary_y=False
        )
    fig.add_trace(
        go.Scatter(x=df['mid point'], y=df['at skew'], name='AT Skew'), secondary_y=False
        )
    fig.add_trace(
        go.Scatter(
            x=df['mid point'], y=df['cummulative gc skew'], name='Cummulative GC Skew'
            ), secondary_y=True
        )
    fig.add_trace(
        go.Scatter(
            x=df['mid point'], y=df['cummulative at skew'], name='Cummulative AT Skew'
            ), secondary_y=True
        )
    file_name = name + ".html"
    fig.write_html(file_name)
    print_to_system('Plot saved to ' + file_name)

def plot_svg(df: DataFrame, name: str) -> None:
    '''
    plot svg from dataframe
        arguments:
            df: the datagrame with gc skew data
            name: the name of the record from which the df originated
        returns:
            None
    '''
    #axis 1
    _, ax1 = plt.subplots()
    ax1.plot(df["mid point"], df['gc skew'], label="GC skew", color='#56b4e9')
    ax1.plot(df["mid point"], df['at skew'], label="AT skew", color='#e69f00')
    ax1.set_xlabel('Position')
    ax1.set_ylabel('Skew')
    ax1.set_title('GC skew of ' + name)
    #add second axis
    ax2 = plt.twinx()
    ax2.plot(
        df["mid point"], df['cummulative gc skew'], label="Cumulative GC skew",color='#009e73'
        )
    ax2.plot(
        df["mid point"], df['cummulative at skew'], label="Cumulative AT skew", color='#cc79a7'
        )
    ax2.set_ylabel('Cummulative Skew')
    #legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    plt.legend(lines + lines2, labels + labels2)
    plt.savefig(name + '.svg')

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
