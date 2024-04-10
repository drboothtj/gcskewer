'''
checks inputs for gcskewer
    functions:
    !!!!!!!!!
'''
from gcskewer.io import print_to_system

from typing import List

class GCSkewerError(Exception):
    '''
    General error for gcskewer
    '''

class InputError(GCSkewerError):
    '''
    Error raised for incorrectly provided inputs
    '''

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
    raise InputError('Something unexpected happened when processing the input. Please contact directly for help!') 

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
        print_to_system('Warning: No window size provided. Automatically set to: ' + str(window_size))
    if step_size is None:
        step_size = get_step_size(window_size)
        print_to_system('Warning: No step size provided. Automatically set to: ' + str(step_size))
    return window_size, step_size
