import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from Bio import SeqIO

def print_to_system(string_to_print):
    now = datetime.now()
    current_time = now.strftime("[%H:%M:%S]: ")
    print(current_time + string_to_print)
        
def write_csv(df, name):
    file_name = name + '.csv'
    print_to_system('Writing to ' + file_name)
    df.to_csv(file_name, index = False)

def read_file(filename, file_type):
    record_names = []
    record_sequences = []
    for seq_record in SeqIO.parse(filename, file_type):
        record_names.append(seq_record.id)
        record_sequences.append(seq_record.seq)
    return record_names, record_sequences

def plot_data(df, name):
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