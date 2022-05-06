import sys
import pandas as pd
from skewer import io, parser

def build_dataframe(record_name, record_sequence, window_size, step_size):
    skew_data = []
    sequence_length = len(record_sequence) - window_size
    io.print_to_system('Calculating GC-skew for ' + record_name + '.')
    cummulative_gc = 0
    cummulative_at = 0
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

def calculate_skew(x, y): 
    skew = (x - y)/(x + y)
    return skew

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

    window_size = args.window
    step_size = args.step

    for i in range(0, len(record_names)):
        gc_dataframe = build_dataframe(record_names[i], record_sequences[i], window_size, step_size)
        name = record_names[i] + '_' + str(i)
        io.write_csv(gc_dataframe, name)
        io.plot_data(gc_dataframe, name)
    io.print_to_system('Skewer has finished!')

if __name__ == '__main__':
    main()
