'''
main script for gcskewer
    functions:
        build_dataframe(
            record_name: str, record_sequence: str, window_size: int, step_size: int
            ) -> DataFrame
        calculate_skew(x: int, y: int) -> float
        main()
'''
from gcskewer import checks, output, parser
from gcskewer.classes.dataclasses import Frame
from typing import List

def get_frames(
    record_name: str, record_sequence: str, window_size: int, step_size: int
    ) -> List[Frame]:
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
    output.print_to_system('Calculating GC-skew for ' + record_name + '.')
    #calculate GC skew for each subsequence using the sliding window
    for start_point in range(0, sequence_length, step_size):
        end_point = start_point + window_size
        sub_sequence = record_sequence[start_point:end_point]
        frame = Frame(record_name, sub_sequence, start_point, end_point)
        skew_data.append(frame)
    return skew_data

def main():
    '''
    main routine for gcskewer
        arguments: 
            None
        returns: 
            None
    '''
    output.print_to_system('Running gcskewer...')
    args = parser.get_args()
    checks.check_output(args)
    filename, _format = checks.check_input(args)
    records = output.read_file(filename, _format)
    assert records, (
        'No input sequences!'
        'Check your file and that you have used the correct parameter for the filetype (-g/-f)'
    )
    window_size, step_size = checks.check_window_and_step(
        args.window_size, args.step_size, records.values()
        )

    #For each record in the records list generate the dataframe, plot and save
    for record_name, record_sequence in records.items():
        frames = get_frames(record_name, record_sequence, window_size, step_size)
        name = record_name
        if args.csv:
            output.write_gcframes_to_csv(frames, name)
        if args.plot:
            output.plot_data(gc_dataframe, name)
        if args.svg:
            output.plot_svg(gc_dataframe, name)
    output.print_to_system('gcskewer has finished!')

if __name__ == "__main__":
    main()
