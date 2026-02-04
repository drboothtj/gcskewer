'''
main script for gcskewer
'''
from typing import Dict, List

from gcskewer import checks, output, parser
from gcskewer.classes.dataclasses import Frame

def get_dict_for_plotting(frames: List[Frame]) -> Dict:
    '''
    gets data as a dictionary from members of the Frame class
        arguments:
            frames: a list of Fram objects
        returns:
            plotting_dict: frame data formmatted as a Dict
    '''
    plotting_dict = {
        'midpoint' :  [frame.midpoint for frame in frames],  
        'gc_skew' : [frame.gc_skew for frame in frames],
        'at_skew' : [frame.at_skew for frame in frames],
        'cummulative_gc_skew' : [frame.cummulative_gc for frame in frames],
        'cummulative_at_skew' : [frame.cummulative_at for frame in frames],
        'gc_content' : [frame.gc_content for frame in frames],
        'at_content' : [frame.at_content for frame in frames],
    }
    return plotting_dict

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
    output.print_to_system('Running gcskewer version 1.1.1')
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
    for record_name, record_sequence in records.items():
        frames = get_frames(record_name, record_sequence, window_size, step_size)
        name = record_name
        # technically frame_dict doesnt need to be calculated for .csv
        frame_dict = get_dict_for_plotting(frames)
        if args.csv:
            output.write_gcframes_to_csv(frames, name)
        if args.plot:
            output.plot_html(frame_dict, name)
        if args.svg:
            output.plot_svg(frame_dict, name)
        Frame.reset() #vital!
    output.print_to_system('gcskewer has finished!')

if __name__ == "__main__":
    main()
