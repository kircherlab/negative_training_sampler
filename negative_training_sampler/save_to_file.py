#!/usr/bin/env python

"""calculates gc content for coordinates in a .bed file"""

def save_to_file(negative_sample, positive_sample, output_file):
    """Saves positive and negative sample dataframes to output files.

    Arguments:
        negative_sample {dataframe} -- [dataframe containing negative samples]
        positive_sample {dataframe} -- [dataframe containing positive samples]
        output_file {str} -- [stem name of the output file]
    """
    if "/" in output_file:
        split_path = output_file.split("/")
        out_path = "/".join(split_path[:-1])+"/"+"{}"+str(split_path[-1])
    else:
        out_path = "{}" + str(output_file)
    with open(out_path.format("/positive_"), "w") as file:
        positive_sample.to_csv(file, sep="\t", index=False)
    with open(out_path.format("/negative_"), "w") as file:
        negative_sample.to_csv(file, sep="\t", index=False)
