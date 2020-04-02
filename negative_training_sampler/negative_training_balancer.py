"""Main module."""
import sys

from dask.distributed import Client

from negative_training_sampler.bed_gc_calculator import get_gc
from negative_training_sampler.filter import get_negative
from negative_training_sampler.filter import get_positive
from negative_training_sampler.filter import clean_sample
from negative_training_sampler.io import save_to_file
from negative_training_sampler.utils import combine_samples

CHROMS = ["chr1", "chr2", "chr3",
          "chr4", "chr5", "chr6",
          "chr7", "chr8", "chr9",
          "chr10", "chr11", "chr12",
          "chr13", "chr14", "chr15",
          "chr16", "chr17", "chr18",
          "chr19", "chr20", "chr21",
          "chr22", "chrX", "chrY"]

def balance_trainingdata(label_file, genome_file, output_file, verbose, cores=1, memory_per_core='2GB'):
    """
    Function that calculates the GC content for positive and negative labeled genomic regions and
    balances their number based on GC content per chromosome.

    Arguments:
        label_file {str}        -- [Path to a tab separated file containing genomic regions
                                    labeled as positive(1) or negative(0)]
        genome_file {str}       -- [Path to a refrence genome in FASTA format]
        output_file {str}       -- [Name of the output file. File will be in .tsv format.]
        cores {int}             -- [Number of cores, default is 1. ]
        memory_per_core {str}   -- [Amount of memory per core.
                                    Accepted format [number]GB. Default is 2GB]
    """

    if verbose:
        print("---------------------\nstarting workers...\n---------------------")

    client = Client(n_workers=cores,
                    threads_per_worker=1,
                    memory_limit=memory_per_core,
                    dashboard_address=None)
    client

    if verbose:
        print("---------------------\ncalculating GC content...\n---------------------")

    cl_gc = get_gc(label_file, genome_file)

    if verbose:
        print("---------------------\nextracting positive samples...\n---------------------")

    positive_sample = get_positive(cl_gc)

    if verbose:
        print("---------------------\nbalancing negative sample set...\n---------------------")

    dts = dict(cl_gc.dtypes)
    negative_sample = (cl_gc.groupby(["CHR"], group_keys=False).apply(get_negative,
                                                                      meta=dts)
                       ).compute()

    if verbose:
        print("---------------------\ncleaning samples\n---------------------")

    positive_sample_cleaned = clean_sample(positive_sample, CHROMS)
    negative_sample_cleaned = clean_sample(negative_sample, CHROMS)

    if verbose:
        print("---------------------\nsaving results\n---------------------")

    sample_df = combine_samples(positive_sample_cleaned, negative_sample_cleaned)

    if output_file:
        save_to_file(sample_df, output_file)
    else:
        print(sample_df.to_string(index=False, header=False), file=sys.stdout)

    if verbose:
        print("---------------------\nshutting down workers...\n---------------------")

    client.close()
