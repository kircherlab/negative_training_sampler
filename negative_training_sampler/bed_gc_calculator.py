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
    """
    bed_df = pybedtools.BedTool(label_file)
    bed_gc = bed_df.nuc(reference_file)
    gc_df = dd.read_table(bed_gc.fn)
    gc_df = gc_df.loc[:, gc_df.columns.str.contains("usercol|gc|num_N")]
    colnames = generate_colnames(gc_df, label_num)
    gc_df.columns = colnames
    gc_df = gc_df.loc[gc_df.num_N == 0].drop("num_N", axis=1)
    gc_df["gc"] = gc_df["gc"].astype("float32")*100
    gc_df["gc"] = gc_df["gc"].round(precision)
    return gc_df


def main():
    """[summary]
    """


if __name__ == "__main__":
    main()
