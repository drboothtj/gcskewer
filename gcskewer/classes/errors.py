'''
errors for gcskewer
'''
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
