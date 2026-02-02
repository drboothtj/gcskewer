'''
checks inputs for gcskewer
    functions:
    !!!!!!!!!
'''
from typing import List
from gcskewer.output import print_to_system

class GCSkewerError(Exception):
    '''
    General error for gcskewer
    '''

class InputError(GCSkewerError):
    '''
    Error raised for incorrectly provided inputs
    '''

class OutputError(GCSkewerError):
    '''
    Error raised when no output is provided
    '''

def check_output(args):
    '''
    check an output exists
    '''
    output_args = [args.csv, args.svg, args.plot]
    if all(arg is False for arg in output_args):
        raise OutputError(
            'No output flag was set! Please choose at least 1 output.'
            )

def check_input(args):
    '''
    Checks what input the user provided, and
    errors if neither or both is set, or
    returns file type for reading
        arguments:
            args: args from argsparse
        returns:
            input path, file extension
    '''
    if args.genbank is None and args.fasta is None:
        raise InputError('No input file!')
    if args.fasta and args.genbank:
        raise InputError('Both genbank and fasta input provided - pick one!')
    if args.genbank is None:
        return args.fasta, 'fasta'
    if args.fasta is None:
        return args.genbank, 'genbank'
    raise InputError(
        'Something unexpected happened when processing the input. Please report the issue!'
        )

def get_window_size(sequences: List):
    '''
    return window size of 1% of the smalles sequences
        arguments:
            record_sequences: list of dna sequences
        returns:
            window_size: 1% of the smallest sequence
    '''
    sequence_lengths = [len(seq) for seq in sequences]
    window_size = min(sequence_lengths)//100
    return window_size

def get_step_size(window_size: int):
    '''
    returns 1/10 of the window size
        arguments:
            window_size: window size for analysis
        returns:
            step_size: step size is 1/10 of the window size
    '''
    step_size = window_size // 10
    return step_size

def check_window_and_step(window_size, step_size, sequences):
    '''
    checks if window and step sizes are set and, 
    if not, automatically sets them proportionate to the size of the smallest input sequence
        arguments:
            window_size: window size from argparse
            step_size: step size from argparse
            sequences: a list of input dna sequences
    '''
    if window_size is None:
        window_size = get_window_size(sequences)
        print_to_system(
            'Warning: No window size provided. Automatically set to: ' + str(window_size)
            )
    if step_size is None:
        step_size = get_step_size(window_size)
        print_to_system('Warning: No step size provided. Automatically set to: ' + str(step_size))
    return window_size, step_size
