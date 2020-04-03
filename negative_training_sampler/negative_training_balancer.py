"""Main module."""

import logging

import sys

from dask.distributed import Client

from negative_training_sampler.bed_gc_calculator import get_gc
from negative_training_sampler.filter import get_negative
from negative_training_sampler.filter import get_positive
from negative_training_sampler.filter import clean_sample
from negative_training_sampler.io import write_to_file
from negative_training_sampler.io import write_to_stdout
from negative_training_sampler.io import load_contigs
from negative_training_sampler.utils import combine_samples


def balance_trainingdata(label_file,
                         reference_file,
                         genome_file,
                         output_file,
                         bgzip,
                         log_file,
                         verbose,
                         cores=1,
                         memory_per_core='2GB'):
    """
    Function that calculates the GC content for positive and negative labeled genomic regions and
    balances their number based on GC content per chromosome.

    Arguments:
        label_file {str}        -- [Path to a .bed file containing genomic regions
                                    labeled as positive(1) or negative(0)]
        reference_file {str}    -- [Path to a reference genome in FASTA format]
        genome_file {str}       -- [Path to the genome file of the reference]
        output_file {str}       -- [Name of the output file. File will be in .bed format]
        bgzip {boolean}         -- [output is compressed or not]
        log_file {str}          -- [Log file to write out loggin. If not None.]
        cores {int}             -- [Number of cores, default is 1. ]
        memory_per_core {str}   -- [Amount of memory per core.
                                    Accepted format [number]GB. Default is 2GB]
    """

    logLevel = logging.INFO
    format='%(message)s'
    if verbose:
        logLevel = logging.DEBUG
        format = None #logging.Formatter(None) #logging.Formatter('%(message)s')
    if log_file is not None:
        logging.basicConfig(filename=log_file, level=logLevel, format=format)
    elif output_file is not None:
        logging.basicConfig(stream=sys.stdout, level=logLevel, format=format)
    else:
        logging.basicConfig(stream=sys.stderr, level=logLevel, format=format)

    logging.info("---------------------\nstarting workers...\n---------------------")

    client = Client(n_workers=cores,
                    threads_per_worker=1,
                    memory_limit=memory_per_core,
                    dashboard_address=None)
    client # pylint: disable=pointless-statement

    logging.info("---------------------\ncalculating GC content...\n---------------------")

    cl_gc = get_gc(label_file, reference_file)

    logging.info("---------------------\nextracting positive samples...\n---------------------")

    positive_sample = get_positive(cl_gc)

    logging.info("---------------------\nbalancing negative sample set...\n---------------------")

    dts = dict(cl_gc.dtypes)
    negative_sample = (cl_gc.groupby(["CHR"], group_keys=False).apply(get_negative,
                                                                      meta=dts)
                       ).compute()

    logging.info("---------------------\nloading contigs...\n---------------------")

    contigs = load_contigs(genome_file)

    logging.info("---------------------\ncleaning samples\n---------------------")

    positive_sample_cleaned = clean_sample(positive_sample, contigs)
    negative_sample_cleaned = clean_sample(negative_sample, contigs)

    logging.info("---------------------\nsaving results\n---------------------")

    sample_df = combine_samples(positive_sample_cleaned, negative_sample_cleaned)

    if output_file:
        write_to_file(sample_df, output_file, bgzip)
    else:
        write_to_stdout(sample_df)

    logging.info("---------------------\nshutting down workers...\n---------------------")

    client.close()
