# negative_training_sampler

This package takes a minimal bed file with positive (1) and negative (0) labeled genomic coordinates, calculates their gc content and balances positive and negative labeled entries per chromosome based on their respective GC content.

## Installation

### Requirements

It is highly recommended to use `conda` to install the dependencies.

Dependencies:

```YAML
dependencies:
  - click
  - pandas
  - pybedtools
  - dask
```

**Note:** If pip is used for installation, make sure bedtools is installed. Otherwise install it manually: [bedtools installation guide](https://bedtools.readthedocs.io/en/latest/content/installation.html)

### Setup

#### with conda

Creating a new environment:

```bash
conda env create -f environment.yml
conda activate negative_training_sampler
```

Updating an existing environment:

```bash
conda env update --name myenv --file environment.yml
conda activate myenv
```

Installing the package:

```bash
pip install /path/to/repo
```

### without conda

**Note:** Make sure bedtools is installed. Otherwise install it manually: [bedtools installation guide](https://bedtools.readthedocs.io/en/latest/content/installation.html)

Installing the package:

```bash
pip install /path/to/repo
```

## Usage

The package needs a minimal bed file with positive (1) and negative (0) labeled regions in one file, a reference genome in fasta format and an output file. For more details see [input](###input) section.

General use:

```bash
negative_input_sampler LABEL_FILE GENOME_FILE -o OUTPUT_FILE
```

More advanced use:

```bash
negative_input_sampler LABEL_FILE GENOME_FILE -o OUTPUT_FILE --cores INT --memory [int]GB
```

### help

The help message of the command line interface can be accesssed by typing:

```bash
negative_training_sampler --help
```

Help output:

```bash
Usage: negative_training_sampler [OPTIONS] LABEL_FILE GENOME_FILE

  A simple script that takes a tsv file with positive and negative labels
  and a genome file. Generates negative samples with the same GC
  distribution as the positive samples per chromosome.

Options:
  -o, --output_file TEXT  path to output file;  default:
                          ./[positive, negative]_samples.tsv

  --cores INTEGER         number of used cores default: 1
  --memory TEXT           amount of memory per core (e.g. 2 cores * 2GB = 4GB)
                          default: 2GB

  --help                  Show this message and exit.
```

### input

Example input:

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

**Note:** Columns are chr, start, stop, label.

### output

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

**Note:** The output is split in two files, one containing the positive samples and one containing the negative samples.

## Licence

MIT license

## Authors

`negative_training_sampler` was written by [Sebastian Röner](mailto:sebastian.roener@charite.de).
