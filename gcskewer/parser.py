'''
parser for gcskewer
    functions:
        get_parser()
        get_arguments(parser):
        get_args()
'''

import argparse
from argparse import RawTextHelpFormatter

def get_parser():
    '''
    gets argument parser
        arguments:
            None
        returns:
            argument_parser
    '''
    parser = argparse.ArgumentParser(
        prog='gcskewer',
        description=
            '''
            Calculates and plots gc-skew from DNA sequences.
                EXAMPLE USAGE 1:
                    gcskewer -f my_fasta.fna -p 
                EXAMPLE USAGE 2:
                    gcskewer -g my_genbank.gbk -ws 1000 -ss 100 -c
            ''',
        epilog='Written by Dr. Thom Booth, 2023',
        formatter_class=RawTextHelpFormatter
    )
    return parser

def add_input_parser(parser):
    '''
    add input subparser to parser
    '''
    input_parser = parser.add_argument_group(
            'inputs',
            'define the input path for genbank or fasta inputs\n'
            )
    input_parser.add_argument(
        '-g',
        '--genbank',
        type=str,
        default=None,
        help = (
            'path to input genbank file'
        )
    )
    input_parser.add_argument(
        '-f',
        '--fasta',
        type=str,
        default=None,
        help = (
            'path to input fasta nucleotide file'
        )
    )
    return parser

def add_window_parser(parser):
    '''
    add window subparser to parser
    '''
    window_parser = parser.add_argument_group(
        'window parameters',
        'define the parameters of the sliding window\n'
        'NOTE: parameters will be automatically optimised if left blank\n' 
        )
    window_parser.add_argument(
        '-ws',
        '--window-size',
        type=int,
        default=None,
        help = (
            'window size for gc-skew plot'
        )
    )
    window_parser.add_argument(
        '-ss',
        '--step-size',
        type=int,
        default=None,
        help = (
            'step size for gc-skew plot'
        )
    )
    return parser

def add_output_parser(parser):
    '''
    add output subparser to parser
    '''
    output_parser = parser.add_argument_group(
        'output parameters',
        'define the outputs and output directory\n'
        )
    output_parser.add_argument(
        '-d',
        '--dir',
        type=str,
        default=None,
        help=(
            'the directory to save the outputs\n'
            'NOTE: defaults to the current directory'
        )
    )
    output_parser.add_argument(
        '-c',
        '--csv',
        action="store_true",
        help = (
            'write the output to a .csv file'
        )
    )
    output_parser.add_argument(
        '-s',
        '--svg',
        action="store_true",
        help = (
            'write the output to an .svg file'
        )
    )
    output_parser.add_argument(
        '-p',
        '--plot',
        action="store_true",
        help = (
            'write the output to an .html file'
        )
    )
    variables = [
        'gc_skew',
        'at_skew',
        'cummulative_gc_skew',
        'cummulative_at_skew',
        'gc_content',
        'at_content',
    ]
    output_parser.add_argument(
        '-v',
        '--variables',
        nargs='+',
        choices=variables,
        default=variables,
        help=('variables to plot'),
    )
    return parser

def get_arguments(parser):
    '''
    add argument subparsers to the parser
    '''
    add_input_parser(parser)
    add_window_parser(parser)
    add_output_parser(parser)
    return parser

def get_args():
    '''
    gets the arguments from the parser
        arguments:
            None
        returns:
            args: arguments object
    '''
    parser = get_parser()
    parser = get_arguments(parser)
    args = parser.parse_args()
    args.variables = set(args.variables)
    return args
