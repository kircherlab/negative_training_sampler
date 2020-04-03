#!/usr/bin/env python

import csv

"""i/o functions"""

def save_to_file(sample_df, output_file):
    """Saves dataframe to output_file.

    Arguments:
        sample_df {dataframe} -- [dataframe containing balanced samples]
        output_file {str} -- [path to the output file]
    """

    with open(output_file, "w") as file:
        sample_df.to_csv(file, sep="\t", index=False, header=False)


def load_contigs(genome_file):
    """loads a genome file of the reference.

    Arguments:
        genome_file {str} -- [path to the genome file]

    Returns:
        [list] -- list containing contigs of the genome file
    """

    contigs = set()
    with open(genome_file) as file:
        genome_file_reader = csv.reader(file, delimiter='\t')
        for contig in genome_file_reader:
            contigs.add(contig[0])
    return list(contigs)
