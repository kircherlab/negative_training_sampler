"""Console script for gtbalancer."""
import sys
import click

from negative_training_sampler.negative_training_balancer import balance_trainingdata


@click.command()
@click.option("-i",
              "--label-file",
              'label_file',
              required=True,
              type=click.Path(exists=True, readable=True),
              help="Input bed file with labeled regions")
@click.option("-r",
              "--reference-file",
              'reference_file',
              required=True,
              type=click.Path(exists=True, readable=True),
              help="Input genome reference in fasta format")
@click.option("-g",
              "--genome-file",
              'genome_file',
              required=True,
              type=click.Path(exists=True, readable=True),
              help="Input genome file of reference")
@click.option("-f",
              "--fasta-file",
              'fasta_file',
              required=False,
              type=click.Path(exists=True, readable=True),
              help="Use fasta sequences as positive label insteald of label bed file")
@click.option("-o",
              "--output_file",
              'output_file',
              type=click.Path(writable=True),
              help="Path to output file.")
@click.option("-n",
              "--label_num",
              type=click.INT,
              default=1,
              help="Number of separate label columns.")
@click.option("--precision",
              default=2,
              type=int,
              help="Precision of decimals when computing the attributes like GC content.")
@click.option("-c",
              "--bgzip",
              is_flag=True,
              help="Output will be bgzipped.")
@click.option("--log",
              "log_file",
              type=click.Path(writable=True),
              help="Write logging to this file.")
@click.option("--verbose",
              is_flag=True,
              help="Will print verbose messages.")
@click.option("--seed",
              "seed",
              type=click.INT,
              default=None,
              help="Sets the seed for sampling.")
@click.option("--cores",
              default=1,
              type=int,
              help="number of used cores\n default: 1")
@click.option("--memory",
              default="2GB",
              help="amount of memory per core (e.g. 2 cores * 2GB = 4GB)\ndefault: 2GB")
def cli(label_file, reference_file, genome_file, fasta_file, output_file, precision, label_num,
        bgzip, log_file, verbose, seed, cores, memory):  # pylint: disable=no-value-for-parameter
    '''
    A simple script that takes a tsv file with positive and negative labels
    and a reference file. Generates negative samples with the same GC distribution
    as the positive samples per chromosome.
    '''

    balance_trainingdata(label_file=label_file,
                         reference_file=reference_file,
                         genome_file=genome_file,
                         precision=precision,
                         fasta_file=fasta_file,
                         output_file=output_file,
                         label_num=label_num,
                         bgzip=bgzip,
                         log_file=log_file,
                         verbose=verbose,
                         seed=seed,
                         cores=cores,
                         memory_per_core=memory
                         )


if __name__ == "__main__":
    sys.exit(cli())  # pylint: disable=no-value-for-parameter
