'''
'''
class GCSkewerError(Exception):
    '''
    General error for gcskewer
    '''

class InputError(GCSkewerError):
    '''
    Error raised for incorrectly provided inputs
    '''

def check_args(args):
    '''
    [...]

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
