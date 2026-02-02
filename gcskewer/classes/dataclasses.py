'''
classes for gcskewer
'''
class Frame:
    '''
    frame for the gc plots
    '''
    cummulative_gc = 0
    cummulative_at = 0
    header = [
        'record',
        'sequence',
        'start',
        'end',
        'midpoint',
        'g_count',
        'c_count',
        't_count',
        'a_count',
        'gc_content',
        'at_content',
        'gc_skew',
        'at_skew',
        'cummulative_gc',
        'cummulative_at'
    ] #this can be automated more safely

    @classmethod
    def reset(cls):
        '''
        reset the class variables
        useful when moving to a new record
        '''
        cls.cummulative_gc = 0
        cls.cummulative_at = 0

    def __init__(
        self, record: str, sequence: str, start: int, end: int
        ):
        '''
        initialisation function
        '''
        self.record = record
        self.sequence = sequence
        self.start = start
        self.end = end
        self.midpoint = start + (start + end) / 2
        self.g_count = self.count_nt('G')
        self.c_count = self.count_nt('C')
        self.t_count = self.count_nt('T')
        self.a_count =  self.count_nt('A')
        self.gc_content = (self.g_count + self.c_count) / (len(self.sequence))
        self.at_content = 1 - self.gc_content
        self.gc_skew = self.calculate_skew(self.g_count, self.c_count)
        self.at_skew = self.calculate_skew(self.a_count, self.t_count)

        type(self).cummulative_gc += self.gc_skew
        type(self).cummulative_at += self.at_skew
        self.cummulative_gc = type(self).cummulative_gc
        self.cummulative_at = type(self).cummulative_at

    def count_nt(self, nt: str) -> int:
        '''
        count the occurance of a letter in the string
        '''
        nt = nt.upper()
        return self.sequence.upper().count(nt)

    def calculate_skew(self, x: int, y: int) -> float:
        '''
        calculate gc skew
            arguments
        '''
        skew = (x - y)/(x + y)
        return skew

    def get_line(self):
        '''
        return a list of class variables
        '''
        return list(self.__dict__.values())
