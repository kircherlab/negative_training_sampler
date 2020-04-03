"""Console script for gtbalancer."""
import sys
import click

from negative_training_sampler.negative_training_balancer import balance_trainingdata

@click.command()
@click.option("-i",
              "label_file",
              required=True,
              type=click.Path(),
              help="Input bed file with labeled regions")
@click.option("-r",
              "reference_file",
              required=True,
              type=click.Path(),
              help="Input genome reference in fasta format")
@click.option("-o",
              "--output_file",
              help="""path to output file.""")
@click.option("--verbose",
              is_flag=True,
              help="Will print verbose messages.")
@click.option("--cores",
              default=1,
              help="""number of used cores\n default: 1""")
@click.option("--memory",
              default="2GB",
              help="""amount of memory per core (e.g. 2 cores * 2GB = 4GB)\ndefault: 2GB""")
def cli(label_file, genome_file, output_file, verbose, cores, memory):    # pylint: disable=no-value-for-parameter
    '''
    A simple script that takes a tsv file with positive and negative labels
    and a genome file. Generates negative samples with the same GC distribution
    as the positive samples per chromosome.
    '''

    balance_trainingdata(label_file=label_file,
                         genome_file=genome_file,
                         output_file=output_file,
                         cores=cores,
                         memory_per_core=memory,
                         verbose=verbose
                         )


if __name__ == "__main__":
    sys.exit(cli())  # pylint: disable=no-value-for-parameter
