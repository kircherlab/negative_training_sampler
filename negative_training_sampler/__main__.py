#!/usr/bin/env python

import sys

from negative_training_sampler  import cli

def main():
    """
    Main module calling the command line interface
    """
    sys.exit(cli.cli())

if __name__ == "__main__":
    main()
