###Skewer version 0.0.1##
###Dr . T. J. Booth###

###imports
import sys
from datetime import datetime
from Bio import SeqIO

###general functions
#print to terminal
def print_to_system(string_to_print):
    now = datetime.now()
    current_time = now.strftime("[%H:%M:%S]: ")
    print(current_time + string_to_print)

#Check the required arguments
def check_arguments(arguments):
    number_of_arguments = len(arguments)
    print(number_of_arguments)
    if number_of_arguments > 3:
        print_to_system("ERROR: Too many arguments! Please provide only the filename and window size.")
        quit()
    elif number_of_arguments < 3:
        print_to_system("ERROR: Too few arguments! Please provide the filename and window size.")
        quit()
    else:
        print_to_system("Analysing GC-skew from " + arguments[1] + "...")
        return arguments[1], arguments[2]

###specific functions
#Determine if file is correct type and pass to correct reader
def read_file(filename):
    extension = filename.split('.')[1]
    if extension == 'fasta':
        record_names, record_sequences = read_fasta(filename)
    elif extension == 'gbk':
        record_names, record_sequences = read_genbank(filename)
    else:
        print_to_system('Invalid file name. Please provde a .fasta or .gbk file.')
        exit()
    return record_names, record_sequences

#Read fasta into two lists record_names and record_seqeunces
##THIS CODE CAN BE COMBINED
def read_fasta(filename):
    print_to_system('Reading fasta: ' + filename)
    record_names = []
    record_sequences = []
    for seq_record in SeqIO.parse(filename, "fasta"):
        record_names.append(seq_record.id)
        record_sequences.append(seq_record.seq)
    return record_names, record_sequences

#Read gbk into two lists record_names and record_seqeunces
##THIS CODE CAN COMBINED
def read_genbank(filename):
    print_to_system('Reading genbank: ' + filename)
    record_names = []
    record_sequences = []
    for seq_record in SeqIO.parse(filename, "genbank"):
        record_names.append(seq_record.id)
        record_sequences.append(seq_record.seq)
    return record_names, record_sequences

def calculate_skew(record_names, record_sequences, window_size):
    for record in record_names:
        print_to_system('Calculating GC-skew for ' + record + '.')


#Run Workflow
def main():
    print_to_system('Running Skewer version 0.0.1!')
    filename, window_size = check_arguments(sys.argv)
    record_names, record_sequences = read_file(filename)
    calculate_skew(record_names, record_sequences, window_size)

    print_to_system('Method: ...')
#Run
main()
