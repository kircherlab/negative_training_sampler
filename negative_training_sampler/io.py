#!/usr/bin/env python

"""i/o functions"""
import sys

from . import bgzf

def write_to_file(sample_df, output_file, bgzip):
    """writes dataframe to output_file.

    Arguments:
        sample_df {dataframe} -- [dataframe containing balanced samples]
        output_file {str} -- [path to the output file]
        bgzip {bool} -- [bool value to determine, whether output is bgzipped or not.]
    """
    if bgzip or (bgzip is False and output_file and output_file.endswith(".gz")):
        file = bgzf.BgzfWriter(filename=output_file)
        file.write(sample_df.to_string(index=False, header=False))
        file.close()
    else:
        with open(output_file, "w") as file:
            sample_df.to_csv(file, sep="\t", index=False, header=False)

def write_to_stdout(sample_df):
    """Writes df to stdout.

    Arguments:
        sample_df {dataframe} -- [dataframe containing balanced samples]
        bgzip {bool} -- [bool value to determine, whether output is bgzipped or not.]
    """

    print(sample_df.to_string(index=False, header=False), file=sys.stdout)
