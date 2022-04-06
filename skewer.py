###Skewer version 0.0.2##
###Dr . T. J. Booth###

###imports
import sys
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from Bio import SeqIO

###general functions
#print to terminal
def print_to_system(string_to_print):
    now = datetime.now()
    current_time = now.strftime("[%H:%M:%S]: ")
    print(current_time + string_to_print)

#Check the required arguments
def check_arguments(arguments):
    number_of_arguments = len(arguments)
    if number_of_arguments > 4:
        print_to_system("ERROR: Too many arguments! Please provide only the filename, window  and step size.")
        quit()
    elif number_of_arguments < 4:
        print_to_system("ERROR: Too few arguments! Please provide the filename, window and step sizes.")
        quit()
    else:
        print_to_system("Analysing GC-skew from " + arguments[1] + "...")
        return arguments[1], int(arguments[2]), int(arguments[3])
        
def write_csv(df, name):
    file_name = name + '.csv'
    print_to_system('Writing to ' + file_name)
    df.to_csv(file_name, index = False)

###specific functions
#Determine if file is correct type and pass to correct reader
def read_file(filename):
    extension = filename.split('.')[1]
    if extension == 'fasta':
        record_names, record_sequences = read_fasta(filename)
    elif extension == 'gbk':
        record_names, record_sequences = read_genbank(filename)
    else:
        print_to_system('Invalid file name. Please provde a .fasta or .gbk file.')
        exit()
    return record_names, record_sequences

#Read fasta into two lists record_names and record_seqeunces
##THIS CODE CAN BE COMBINED
def read_fasta(filename):
    print_to_system('Reading fasta: ' + filename)
    record_names = []
    record_sequences = []
    for seq_record in SeqIO.parse(filename, "fasta"):
        record_names.append(seq_record.id)
        record_sequences.append(seq_record.seq)
    return record_names, record_sequences

#Read gbk into two lists record_names and record_seqeunces
##THIS CODE CAN COMBINED
def read_genbank(filename):
    print_to_system('Reading genbank: ' + filename)
    record_names = []
    record_sequences = []
    for seq_record in SeqIO.parse(filename, "genbank"):
        record_names.append(seq_record.id)
        record_sequences.append(seq_record.seq)
    return record_names, record_sequences

#creates a dataframe with GC-skew data for plotting in plotly
def build_dataframe(record_name, record_sequence, window_size, step_size):
    skew_data = []
    sequence_length = len(record_sequence) - window_size
    print_to_system('Calculating GC-skew for ' + record_name + '.')
    cummulative_gc = 0
    cummulative_at = 0
    #calculate GC skew for each subsequence using the sliding window
    for start_point in range(0, sequence_length, step_size):
        end_point = start_point + window_size
        mid_point = start_point + (window_size/2)
        sub_sequence = record_sequence[start_point:end_point]
        g_count = sub_sequence.upper().count('G')
        c_count = sub_sequence.upper().count('C')
        t_count = sub_sequence.upper().count('T')
        a_count = sub_sequence.upper().count('A')
        gc_skew = calculate_skew(c_count, g_count)
        cummulative_gc += gc_skew
        at_skew = calculate_skew(t_count, a_count)
        cummulative_at += at_skew
        row = [
                record_name, mid_point, 
                g_count, c_count, gc_skew, cummulative_gc,
                a_count, t_count, at_skew, cummulative_at
               ]
        skew_data.append(row)
        gc_dataframe = pd.DataFrame(skew_data, columns = 
                                            ['record', 'mid point',
                                            'g count', 'c count', 'gc skew', 'cummulative gc skew',
                                            'a count', 't count', 'at skew', 'cummulative at skew'])
    return gc_dataframe

#calculates skew from two numbers
###Potentially update to take letters and string. Will simplify above code
def calculate_skew(x, y): 
    skew = (x - y)/(x + y)
    return skew

#plots the gc dataframe and saves as .html    
def plot_data(df, name):
    print_to_system('Plotting data.')
    #create an empty figure with a secondary y axis!
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    #Now individually add traces
    fig.add_trace(go.Scatter(x=df['mid point'], y=df['gc skew'], name='GC Skew'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['mid point'], y=df['at skew'], name='AT Skew'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['mid point'], y=df['cummulative gc skew'], name='Cummulative GC Skew'), secondary_y=True)
    fig.add_trace(go.Scatter(x=df['mid point'], y=df['cummulative at skew'], name='Cummulative AT Skew'), secondary_y=True)
    file_name = name + ".html"
    fig.write_html(file_name)
    print_to_system('Plot saved to ' + file_name)

#Run Workflow
def main():
    print_to_system('Running Skewer version 0.0.2!')
    filename, window_size, step_size = check_arguments(sys.argv)
    record_names, record_sequences = read_file(filename)
    #For each record in the records list generate the dataframe, plot and save
    for i in range(0, len(record_names)):
        gc_dataframe = build_dataframe(record_names[i], record_sequences[i], window_size, step_size)
        name = record_names[i] + '_' + str(i)
        write_csv(gc_dataframe, name)
        plot_data(gc_dataframe, name)
    print_to_system('Skewer has finished!')
#Run
main()
