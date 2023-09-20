# RBM-Search
Regular expression-based Rubisco-binding motif search program

Usage:

python3 RBM-search.py [fasta file] '[regex term]'

Note:
The regex term should be in the standard re format as defined [here](https://docs.python.org/3/library/re.html).
The term should also be quoted.
Example:

'[Q][\D][F][A]{1,3}[R]'

Outputs:

By default the program will create a results folder (if not already existing).
Within the results folder and new, time-dated folder for each search completed will be created.
3 ouptut files are created within this folder:

  1) A fasta file which contains the motif-containing sequences
  2) A csv file which contains the sequence IDs, sequences, length of sequence, identified motif sequences and number of motifs
  3) A settings file which contains the name of the sequence searched and the regular expression search term used
