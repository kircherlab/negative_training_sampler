# negative_training_sampler Changelog

## development

- use a genome file of the fasta for the contigs by `--genome-file` (see #7) to avoid hard-coded contigs. Now this sampler should work with every species.

### Issue #6

- reworked CLI
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
