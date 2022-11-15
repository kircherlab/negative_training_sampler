#!/usr/bin/env python

"""Utility functions"""

import pandas as pd


def combine_samples(positive_sample_cleaned, negative_sample_cleaned, sort=True):
    """Combines positive an negative samples into on dataframe.

    Arguments:
        positive_sample_cleaned {dataframe} -- Dataframe containing positive labeled samples
        negative_sample_cleaned {dataframe} -- Dataframe containing negative labeled samples

    Returns:
        [dataframe] -- Dataframe containing positive and negative labeled samples
    """

    if sort:
        return pd.concat([positive_sample_cleaned, negative_sample_cleaned],
                         axis=0).sort_values(by=["chrom", "chromStart"])
    else:
        return pd.concat([positive_sample_cleaned, negative_sample_cleaned],
                         axis=0)
