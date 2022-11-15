#!/usr/bin/env python

"""calculates gc content for coordinates in a .bed file"""

import dask.dataframe as dd
import dask.bag as db
import pandas as pd
import gzip

COLUMNS = ["chrom", "chromStart", "chromEnd"]


def generate_colnames(label_num):
    """Generates column names for an input dataframe.

    Arguments:
        df {dataframe} -- [dataframe for which column names are generated]
        label_num {int} -- [number of provided labels]

    Returns:
        [list] -- [list of generated column names]
    """
    colnames = [] + COLUMNS
    for i in range(label_num):
        colnames.append("label_{}".format(i+1))
    colnames.append("gc")
    return colnames

def read_fasta(filehandle):
    """
    Reads fasta entries from filehandle
    supports multiline fasta
    """
    count = 0
    seq = ""
    id = ""
    for line in filehandle:
        line = line.rstrip("\n\r")
        if ( (count == 0) and line.startswith(">")): # Read identifier
            id = line[1:]
            count+=1
        elif count == 1:        # read sequence
            seq = line
            count+=1
        elif count == 2:  # multiple case:  a) more sequence (fasta), c) next sequence identifier (fasta)
            if line.startswith(">") : # case c)
                yield seq
                id, seq  = None, None
                count = 1
                id = line[1:]
            else: # case b)
                seq = seq + line
        else:
          sys.stderr.write("Unexpected line:" + str(line.strip()) + "\n")
          count = 0
    if id and seq:
        yield seq
    return

def compute_gc(seq):
    return (seq.count("G")+seq.count("C")+seq.count("c")+seq.count("g"))/(len(seq)-seq.count("n")-seq.count("N"))

def get_gc(fasta_file, label_num, precision):
    """Calculates gc content for all viable entries in an input dataframe.

    Arguments:
        fasta_file {dataframe} -- [Dataframe containing genomic regions labeled
                                   as positive(1) or negative(0)]
        genome_file {str} -- [Path to a refrence genome in FASTA format]

    Returns:
        [dataframe] -- [Dataframe containing viable entries and their respective gc content]
    """
    colnames = generate_colnames(label_num)

    if fasta_file.endswith(".gz"):
        file_handle = gzip.open(fasta_file, 'rt')
    else:
        file_handle = open(fasta_file, 'r')
    seq_db = db.from_sequence([i for i in read_fasta(file_handle)])
    seq_dd = dd.from_pandas(pd.DataFrame({"gc":db.map(compute_gc,seq_db).compute(),"label_1":1},columns=colnames), npartitions=1)
    
    seq_dd["gc"] = seq_dd["gc"].astype("float32")*100
    seq_dd["gc"] = seq_dd["gc"].round(precision)
    return seq_dd


def main():
    """[summary]
    """


if __name__ == "__main__":
    main()
