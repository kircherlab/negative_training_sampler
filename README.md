# negative_training_sampler

This package takes a (minimal) bed file with positive (1) and negative (0) labeled genomic coordinates, calculates their gc content and balances positive and negative labeled entries per chromosome based on their respective GC content.

## Installation

### Requirements

The negative_training_sampler uses pybedtools to calculate the GC content for the provided regions. Pybedtools depends on bedtools, so make sure bedtools is installed. Otherwise install it manually: [bedtools installation guide](https://bedtools.readthedocs.io/en/latest/content/installation.html)

Other Dependencies:

```YAML
dependencies:
  - click
  - pandas
  - pybedtools
  - dask
```

### Setup

It is recommended to setup a conda environment prior to installing the package. By doing so, one has more control over the bedtools version used by pybedtools.

```bash
env create -n negative_training_sampler --file environment.yml
```

Installing the package:

```bash
pip install -e /path/to/repo
```

## Usage

The package needs at least a minimal bed file with positive (1) and negative (0) labeled regions in one file, a reference genome in fasta format and the corresponding genome file. The output will be written to stdout or to an output file specified with the '-o' option. For more details see [input](###input) section.

General use:

```bash
negative_training_sampler -i LABEL_FILE -r REFERENCE_FILE -g GENOME_FILE -o OUTPUT_FILE
```

More advanced use:

```bash
negative_training_sampler -i LABEL_FILE -r REFERENCE_FILE -g GENOME_FILE -o OUTPUT_FILE --cores INT --memory [INT]GB
```

### help

The help message of the command line interface can be accesssed by typing:

```bash
negative_training_sampler --help
```

Help output:

```bash
Usage: negative_training_sampler [OPTIONS]

  A simple script that takes a tsv file with positive and negative labels
  and a reference file. Generates negative samples with the same GC
  distribution as the positive samples per chromosome.

Options:
  -i, --label-file PATH      Input bed file with labeled regions.  [required]
  -r, --reference-file PATH  Input genome reference in fasta format.
                             [required]

  -g, --genome-file PATH     Input genome file of reference  [required]
  -o, --output_file PATH     Path to output file.
  -n, --label_num INTEGER    Number of separate label columns. Default=1
  --precision INTEGER        Precision of decimals when computing the
                             attributes like GC content.

  -c, --bgzip                Output will be bgzipped.
  --log PATH                 Write logging to this file.
  --verbose                  Will print verbose messages.
  --seed INTEGER             Sets the seed for sampling.
  --cores INTEGER            Number of used cores default: 1
  --memory TEXT              Amount of memory per core (e.g. 2 cores * 2GB =
                             4GB) default: 2GB

  --help                     Show this message and exit.

```

### input

Input files are in bed format with a minimum of the three required bed field (chrom, chromStart, chromEnd) and up to all 12 bed field. Additionally, at least one label column containing numerical binary labels (0 and 1) is required.

**Note:** It is recommend to have genomic windows of the same size to minimize sampling bias. One way to generate labeled windows of equal size, is to use [Seqdataloader](https://github.com/kundajelab/seqdataloader).

Minimal input example:

```bash
chr1    191200  191500  0.0
chr1    205950  206250  0.0
chr1    296600  296900  0.0
chr1    354950  355250  0.0
chr1    356950  357250  0.0
chr1    362800  363100  1.0
chr1    362850  363150  1.0
chr1    362900  363200  1.0
```

**Note:** Columns are chrom, chromStart, chromEnd, label.

### output

Output contains information from Input (bed fields) and an additional column containing information on the GC content of the region.

example output:

```bash
CHR     START   END     label_1 gc
chr1    362800  363100  1.0     38.666702
chr1    362850  363150  1.0     35.666702
chr1    362900  363200  1.0     41.3333
chr1    381450  381750  1.0     74.3333
chr1    381500  381800  1.0     74.6667
chr1    381550  381850  1.0     73.0
chr1    381600  381900  1.0     72.6667
chr1    381650  381950  1.0     71.3333
chr1    381700  382000  1.0     68.6667
```

**Note:** The output is written to stdout by default or to a file, if an output files is specified by the -o option.

## Licence

MIT license

## Authors

`negative_training_sampler` was written by [Sebastian Röner](mailto:sebastian.roener@charite.de).
