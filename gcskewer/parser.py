'''
parser for gcskewer
    functions:
        get_parser()
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
                EXAMPLE USAGE 1:'
                    FILL ME IN DUMMY!
                EXAMPLE USAGE 2:'
                    FILL ME IN TOO DUMMY!
            ''',
        epilog='Written by Dr. T. J. Booth, 2023',
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        '-g',
        '--genbank',
        type=str,
        default=None,
        help = (
            'path to input genbank file'
        )
    )
    parser.add_argument(
        '-f',
        '--fasta',
        type=str,
        default=None,
        help = (
            'path to input fasta nucleotide file'
        )
    )
    parser.add_argument(
        '-ws',
        '--window-size',
        type=int,
        default=500,
        help = (
            'window size for gc-skew plot'
        )
    )
    parser.add_argument(
        '-ss',
        '--step-size',
        type=int,
        default=50,
        help = (
            'step size for gc-skew plot'
        )
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default='output.csv',
        help = (
            'prefix for output .csv file'
        )
    )
    parser.add_argument(
        '-s',
        '--svg',
        type=str,
        default=None,
        help = (
            'prefix for output .svg file'
        )
    )
    parser.add_argument(
        '-p',
        '--plot',
        type=str,
        default=None,
        help = (
            'prefix for output .html file'
        )
    )
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
    args = parser.parse_args()
    return args
        
