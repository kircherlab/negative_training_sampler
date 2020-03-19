#!/usr/bin/env python

"""calculates gc content for coordinates in a .bed file"""

import pandas as pd

def get_negative(df):
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
            print("len of neg: {}".format(len(neg)))
            print(gc, count)
        else:
            frac = count/len(neg)
            neg_sample = neg_sample.append(neg
                                           .sample(frac=frac, random_state=1)
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

    Arguments:
        df {dataframe} -- [dataframe containing labeled genomic coordinates]
        chroms {list} -- [list containing all valid chromosome names]

    Returns:
        [dataframe] -- [sorted and cleaned dataframe]
    """
    df.CHR = pd.Categorical(df.CHR,
                            categories=chroms,
                            ordered=True)
    if isinstance(df.index, pd.MultiIndex):
        df = df.droplevel(0)
    df_cleaned = (df.sort_values(by=["CHR", "START"])
                  .reset_index()
                  .drop(columns="index"))
    return df_cleaned
