# negative_training_sampler Changelog

## 0.3.0

- adding command line option --precision to round the precision of decimals defining smaller or larger GC buckets
- bugfix when number negatives != 0 but positives > negatives
- bugfix in stdn out (is now tab separated)
- bugfix unordered chromosomes
    - output data is again properly ordered by chrom and chromStart
- added seed option to CLI (Issue #11)
    - seed is used for reproducing sampling results when debugging
- complete support for bed files (Issue #5)
    - added option to specify number of label columns

## v0.2.0

- use a genome file of the fasta for the contigs by `--genome-file` (see #7) to avoid hard-coded contigs. Now this sampler should work with every species.
- adding a logger using logging. with --log the log file can be written.
- reworked CLI (Issue #6)
    - input is now connected to the -i flag
    - refrence is now connected to the -r flag
    - added --verbose flag
    - added -c (--bgzip) flag
- added bgzip support for -o
    - output file is bgzipped if -c flag is set
    - output file is bgzipped if filename ends with `.gz`, even if -c is not set
- changed how output works
    - positive and negative labeled entries are now saved in one file
    - without specifying an output file (-o), the results are written to stdout
- minor bugfixes
    - debug output is now written to stderr
    - rename genome_file to reference-file


## v0.1.0

Initial negative_training_sampler version.
