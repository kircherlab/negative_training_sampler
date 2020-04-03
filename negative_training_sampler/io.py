#!/usr/bin/env python

"""i/o functions"""

def save_to_file(sample_df, output_file):
    """Saves dataframe to output_file.

    Arguments:
        sample_df {dataframe} -- [dataframe containing balanced samples]
        output_file {str} -- [path to the output file]
    """

    with open(output_file, "w") as file:
        sample_df.to_csv(file, sep="\t", index=False, header=False)
