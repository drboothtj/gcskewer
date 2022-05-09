import sys
import pandas as pd
from skewer import io, parser

def build_dataframe(record_name, record_sequence, window_size, step_size):
    skew_data = []
    sequence_length = len(record_sequence) - window_size
    if sequence_length < 1:
        sequence_length = 1
    io.print_to_system('Calculating GC-skew for ' + record_name + '.')
    cummulative_gc = 0
    cummulative_at = 0
    gc_dataframe = None
    for start_point in range(0, sequence_length, step_size):
        end_point = start_point + window_size
        mid_point = start_point + (window_size/2)
        sub_sequence = record_sequence[start_point:end_point]
        g_count = sub_sequence.upper().count('G') #upper whole sequence
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
    assert gc_dataframe is not None
    return gc_dataframe

def calculate_skew(x, y): 
    skew = (x - y)/(x + y)
    return skew

def get_differences(dataframe):
    gc_max = dataframe['gc skew'].max()
    gc_min = dataframe['gc skew'].min()
    at_max = dataframe['at skew'].max()
    at_min = dataframe['at skew'].min()
    gc_difference = gc_max -  gc_min
    at_difference = at_max -  at_min
    return at_difference, gc_difference



def get_frames(record_names, record_sequences):
    length = len(record_names)
    for i in range(0, length):
        sequence = list(record_sequences[i])
        frame_1 = ''.join([str(base) for base in list(sequence)[::3]])
        record_names.append(record_names[i] + '_frame_1')
        record_sequences.append(frame_1)
        del sequence[0]
        frame_2 = ''.join([str(base) for base in list(sequence)[::3]])
        record_names.append(record_names[i] + '_frame_2')
        record_sequences.append(frame_2)
        del sequence[0]
        frame_3 = ''.join([str(base) for base in list(sequence)[::3]])
        record_names.append(record_names[i] + '_frame_3')
        record_sequences.append(frame_3)
    return record_names, record_sequences

    return record_names, record_sequences

def main():
    io.print_to_system('Running Skewer version 0.1.0!')
    args = parser.parse_args()

    if args.fasta != None:
        filename = args.fasta
        record_names, record_sequences = io.read_file(filename, "fasta")
    elif args.genbank != None:
        filename = args.genbank
        record_names, record_sequences = io.read_file(filename, "genbank")
    else:
        io.print_to_system("No input provided; exiting.")
        exit()

    if args.frame_plot is True:
        record_names, record_sequences = get_frames(record_names, record_sequences)

    window_size = args.window
    step_size = args.step
    min_max_data = []
    min_max_data.append(["Gene", "AT Difference", "GC Difference"])

    for i in range(0, len(record_names)):
        print(record_names[i], record_sequences[i])
        gc_dataframe = build_dataframe(record_names[i], record_sequences[i], window_size, step_size)
        at_difference, gc_difference = get_differences(gc_dataframe)
        name = record_names[i]
        min_max_data.append([name,at_difference,gc_difference])
        io.df_to_csv(gc_dataframe, name)
        io.plot_data(gc_dataframe, name)
    
    io.list_to_csv('skewer_results.csv', min_max_data)
    io.print_to_system('Skewer has finished!')

if __name__ == '__main__':
    main()
