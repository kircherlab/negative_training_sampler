#!/usr/bin/env python

"""calculates gc content for coordinates in a .bed file"""

import dask.dataframe as dd
import pybedtools

BEDCOLS = ["chrom", "chromStart", "chromEnd",
           "name", "score", "strand",
           "thickStart", "thickEnd", "itemRGB",
           "blockCount", "blockSizes", "blockStarts"]


def generate_colnames(df, label_num):
    """Generates column names for an input dataframe.

    Arguments:
        df {dataframe} -- [dataframe for which column names are generated]
        label_num {int} -- [number of provided labels]

    Returns:
        [list] -- [list of generated column names]
    """
    colnames = []
    for i in range(df.columns.str.contains("usercol").sum()-label_num):
        colnames.append(BEDCOLS[i])
    for i in range(label_num):
        colnames.append("label_{}".format(i+1))
    colnames.append("gc")
    colnames.append("num_N")
    return colnames

def get_gc(label_file, reference_file, label_num, precision):
    """Calculates gc content for all viable entries in an input dataframe.

    Arguments:
        label_file {dataframe} -- [Dataframe containing genomic regions labeled
                                   as positive(1) or negative(0)]
        genome_file {str} -- [Path to a refrence genome in FASTA format]

    Returns:
        [dataframe] -- [Dataframe containing viable entries and their respective gc content]


    Example: 
    
    For an input label file like this:

    chr1	191200	191500	0.0
    chr1	205950	206250	0.0
    chr1	296600	296900	0.0
    chr1	354950	355250	0.0
    chr1	356950	357250	0.0

    The output of the function will look like this:

    chrom  chromStart  chromEnd  label_1         gc
    0  chr1      191200    191500      0.0  54.669998
    1  chr1      205950    206250      0.0  42.669998
    2  chr1      296600    296900      0.0  35.330002
    3  chr1      354950    355250      0.0  43.669998
    4  chr1      356950    357250      0.0  49.669998
    """
    # loads bed file
    bed_df = pybedtools.BedTool(label_file)
    # calculates nucleotide content -> https://daler.github.io/pybedtools/autodocs/pybedtools.bedtool.BedTool.nucleotide_content.html#pybedtools.bedtool.BedTool.nucleotide_content
    bed_gc = bed_df.nuc(reference_file)
    # reads output table of nuc as table -> bed_gc.fn contains the filename of the temporary file created by bedtools
    gc_df = dd.read_table(bed_gc.fn)
    #get usercolumns (all columns provided in the bedfile), GC content and number of Ns
    gc_df = gc_df.loc[:, gc_df.columns.str.contains("usercol|gc|num_N")]
    # generate column names used later on 
    colnames = generate_colnames(gc_df, label_num)
    gc_df.columns = colnames
    # drop entries if they contain Ns and drop the column afterwards
    gc_df = gc_df.loc[gc_df.num_N == 0].drop("num_N", axis=1)
    gc_df["gc"] = gc_df["gc"].astype("float32")*100
    gc_df["gc"] = gc_df["gc"].round(precision)
    return gc_df


def main():
    """[summary]
    """


if __name__ == "__main__":
    main()
