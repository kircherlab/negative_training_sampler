#!/usr/bin/env python

"""calculates gc content for coordinates in a .bed file"""

import logging
import pandas as pd

def get_negative(df, seed):
    """Samples negative labeled entries of a dataframe
    according to the gc content of the positive labeled entires.

    Arguments:
        df {dataframe} -- [a dataframe containing genomic coodinates
                           and their respective labels and gc content]

    Returns:
        [dataframe] -- [dataframe containing the sampled negative entries]
    """
    pos_gc_u = df["gc"].loc[(df.iloc[:, 3:-1] == 1).any(axis=1)].unique()
    pos_gc_count = dict(df["gc"].loc[(df.iloc[:, 3:-1] == 1).any(axis=1)].value_counts())
    neg_df = df.loc[(df.iloc[:, 3:-1] == 0).all(axis=1)]
    cleaned_df = neg_df[neg_df.gc.isin(pos_gc_u)]
    neg_sample = pd.DataFrame()

    for gc, count in pos_gc_count.items():
        neg = cleaned_df.loc[cleaned_df["gc"] == gc]

        if len(neg) == 0:
            logging.info("len of neg: {}")
            logging.info(gc, count)
        else:
            if (count > len(neg)):
                n = len(neg)
            else:
                n = count
            neg_sample = neg_sample.append(neg
                                           .sample(n=n, random_state=seed)
                                           )
    return neg_sample

def get_positive(df):
    """Filters dataframe for positive labeled entries.

    Arguments:
        df {dataframe} -- [a dataframe containing genomic coodinates
                           and their respective labels and gc content]

    Returns:
        [dataframe] -- [dataframe containing positive labeled entries]
    """
    return df.loc[(df.iloc[:, 3:-1] == 1).any(axis=1)].compute()


def clean_sample(df, chroms):
    """Sorts entries in dataframe by chromosome
    and drops an indexlevel in case of a multiindex.
    Removes entries where contig is not present.

    Arguments:
        df {dataframe} -- [dataframe containing labeled genomic coordinates]
        chroms {list} -- [list containing all valid chromosome names]

    Returns:
        [dataframe] -- [sorted and cleaned dataframe]
    """
    df.chrom = pd.Categorical(df.chrom,
                            categories=chroms,
                            ordered=True)
    if isinstance(df.index, pd.MultiIndex):
        df = df.droplevel(0)
    df_cleaned = (df.dropna()
                  .sort_values(by=["chrom", "chromStart"])
                  .reset_index()
                  .drop(columns="index"))
    return df_cleaned
