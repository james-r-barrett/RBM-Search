##  Import required modules
import os
import re
import sys
from Bio import SeqIO
import pandas as pd
from datetime import datetime

##  Define lists to append for each record
sequence_out=[]
seqID_out=[]
length_out=[]
description_out=[]

## Define column name in output file
regex = "Regex Matches to " + sys.argv[2]

## For records in imput file (sys.argv[1]), extract sequence, sequence ID and sequence length
for record in SeqIO.parse(sys.argv[1],'fasta'):
    sequence_out.append(format(record.seq))
    description_out.append(format(record.description))
    seqID_out.append('>' + format(record.id))
    length_out.append(len(record.seq))

## Define lists for motif search
motif_out = []
number_motifs = []

## Define motif search function using sequnce list extracted above
## Count number of motifs found and ouput both to lists above
def motif_search(motif):
    for item in sequence_out:
        result = re.findall(motif,item)
        motif_out.append(result)
        number_motifs.append(len(result))

## Search for regex defined in command line position 2
motif_search(sys.argv[2]) 

##  Write into pandas data frame
df=pd.DataFrame(list(zip(seqID_out,description_out,sequence_out,length_out,motif_out,number_motifs)))

##  Label columns
df.columns = ["Sequence ID", "Description","Sequence", "Length", "Motif", regex]

##  Create dataframe with only motif-containing proteins
df_positive = df[df[regex] != 0]

##  Create new dataframe with only the Sequence ID and Sequences of the positive proteins
df_positive_sequences = df_positive[["Sequence ID", "Sequence"]]

##  Get current date_time to output in filename
datestring = datetime.strftime(datetime.now(), '%y%m%d_%H%M')

##  Get the filename from sysarg variable 1 (input name)
importfilename = os.path.splitext(sys.argv[1])[0]

##  Create final filename (date_time + input filename + motifs output(in tsv format)
filename = str(datestring) + "_" + str(importfilename) + "_" + "motifs" + ".csv"

## Create a second filname for the fasta formatted sequences
fasta_filename = str(datestring) + "_" + str(importfilename) + "_" + "motifcontaining" + ".fasta"

##  Settings filename
settings_filename = str(datestring) + "_" + str(importfilename) + "_" + "settings" + ".txt"

##  Get current directory
wd = os.getcwd()

##  Join current WD path with Results output folder
path = os.path.join(wd,"Results",filename)

##  Check if path exists
isExist = os.path.exists(path)

##  If it doesn't, create it
if not isExist:
    os.makedirs(path)

##  Write data frame positive to motifs to tsv in "Results" directory within folder
df_positive.to_csv(os.path.join(path,filename), index=False, sep=',', header=True)

##  Write a file in fasta format of only the motif-containing proteins
df_positive_sequences.to_csv((os.path.join(path,fasta_filename)), index=False, sep='\n', header=False)

##  Write a file with all motif used for
with open ((os.path.join(path,settings_filename)), "w") as f:
    f.write("Input filename: " + sys.argv[1] + "\n" + "Regular expression used for search: " + sys.argv[2])
    
seqno = (len(df_positive.index))
motifno = df_positive[regex].sum()

print("Program completed successfully! Found " + str(motifno) + " motifs in " + str(seqno) + " sequences.")