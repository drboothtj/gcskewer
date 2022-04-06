# skewer
A simple script for generating GC-Skew plots from DNA sequences.

## Usage
```
python skewer.py nucleotidesequence.fasta 500 50
```
Where the three arguments are:

1. A '.fasta' or '.gbk' file containing a nucleotide sequence.
2. The window size for the analysis.
3. The step size for the analysis.

For the time being, `skewer.py` can only handle a single input sequence. This will be updated soon.

It is very important to set an appropriate window and step sizes for the anaylsis. I recommend using a step size that will result in around 1,000 steps. E.g. for a sequence of 50 kb use a step size of 50. Ensure that the window size is **at least** the same size as the step. In future versions, `skewer.py` will be able to reccomend appropriate values for you.

The GC plot will be saved as skewer.html in the current directory.

## Example Data
Comming soon...

## To Do
1. Handle multiple sequences,
2. Automatically calculate reccomended step and window sizes,
3. Plot genbank features over the skew plot,
4. Write the resulting data to a .csv file,
5. Add % completeion for longer analyses,
6. Compile into a software package.
