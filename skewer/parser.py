'''
Create an argument parser using argparse

Functions:
    get_parser() -> parser
'''

import argparse

def get_parser():
    ''''Create a parser object specific to skewer'''
    parser = argparse.ArgumentParser(
        "skewer",
        description=
        "skewer: a python package to analyse GC content and skew of genes and genomes.",
        epilog="Written by Dr. Thom Booth, 2022."
        )
    parser.add_argument(
        '-f',
        '--fasta',
        type=str,
        default=None,
        help='path to a fasta file containing nucleotide sequences'
        )
    parser.add_argument(
        '-g',
        '--genbank',
        type=str,
        default=None,
        help='path to a genbank file containing nucleotide sequences'
        )
    parser.add_argument(
        '-w',
        '--window',
        type=int,
        default=500,
        help='window size for composition analysis'
        )
    parser.add_argument(
        '-s',
        '--step',
        type=int,
        default=50,
        help='step size for composition analysis'
        )
    parser.add_argument(
        '-fp',
        '--frame-plot',
        action='store_true',
        default=False,
        help='output frame plots'
        )
    return parser

def parse_args():
    '''get the arguments from the console via the parser'''
    arg_parser = get_parser()
    args = arg_parser.parse_args()
    return args