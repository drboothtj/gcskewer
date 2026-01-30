'''
classes for gcskewer
'''
class Frame:
    '''
    frame for the gc plots
    '''
    CUMMULATIVE_GC = 0
    CUMMULATIVE_AT = 0

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

        self.midpoint = start + (start - end) / 2
        self.g_count = self.count_nt('G')
        self.c_count = self.count_nt('C')
        self.t_count = self.count_nt('T')
        self.a_count =  self.count_nt('A')
        self.gc_content = (self.g_count + self.c_count) / (self.t_count + self.a_count)
        self.at_content = 1 - self.gc_content
        self.gc_skew = self.calculate_skew(self.c_count, self.g_count)
        self.at_skew = self.calculate_skew(self.t_count, self.a_count)

        type(self).CUMMULATIVE_GC += self.gc_skew
        type(self).CUMMULATIVE_AT += self.at_skew
        self.cummulative_gc = type(self).CUMMULATIVE_GC
        self.cummulative_at = type(self).CUMMULATIVE_AT

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
