'''
main script for gcskewer
    functions:
        build_dataframe(
            record_name: str, record_sequence: str, window_size: int, step_size: int
            ) -> DataFrame
        calculate_skew(x: int, y: int) -> float
        main()
'''

import pandas as pd
from pandas import DataFrame
from gcskewer import checks, io, parser

def build_dataframe(
    record_name: str, record_sequence: str, window_size: int, step_size: int
    ) -> DataFrame:
    '''
    get gc skew and store in a dataframe
        record_name: name of the dna sequence
        record_sequence: dna sequence
        window_size: size of the analysis window
        step_size: step size to move the window
    returns:
        gc_dataframe: gc data dependent on midpoint for plotting
    '''
    skew_data = []
    sequence_length = len(record_sequence) - window_size
    io.print_to_system('Calculating GC-skew for ' + record_name + '.')
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

def calculate_skew(x: int, y: int) -> float:
    '''
    calculate gc skew
        arguments
    '''
    skew = (x - y)/(x + y)
    return skew

def main():
    '''
    main routine for gcskewer
        arguments: 
            None
        returns: 
            None
    '''
    io.print_to_system('Running gcskewer...')
    args = parser.get_args()
    filename, _format = checks.check_input(args)
    records = io.read_file(filename, _format)
    assert records, (
        'No input sequences!'
        'Check your file and that you have used the correct parameter for the filetype (-g/-f)'
    )
    window_size, step_size = checks.check_window_and_step(
        args.window_size, args.step_size, records.values()
        )

    #For each record in the records list generate the dataframe, plot and save
    for record_name, record_sequence in records.items():
        gc_dataframe = build_dataframe(record_name, record_sequence, window_size, step_size)
        name = record_names[i] + '_' + str(i)
        if args.csv:
            io.write_csv(gc_dataframe, name)
        if args.plot:
            io.plot_data(gc_dataframe, name)
        if args.svg:
            io.plot_svg(gc_dataframe, name)
    io.print_to_system('gcskewer has finished!')

if __name__ == "__main__":
    main()
