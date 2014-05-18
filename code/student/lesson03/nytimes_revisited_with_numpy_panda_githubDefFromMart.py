#!/usr/bin/env python
"""
General Assembly - Data Science
Lesson 3 : New York Times, Aggregated CTR
"""
from __future__ import division
#
import pandas as pd
import os.path

# Define the location of the data directory in relation to this script.
DATA_DIR = '../../../data/'

def load_nytimes_dataset():
    """
    Load NYT datasets into a Pandas DataFrame

    @return DataFrame      DataFrame of NYT Impressions
    """

    # Check whether the seperate CSVs have already been
    if not os.path.isfile(DATA_DIR + 'nyt_agg.csv'):
        # What base_url fo all files have in common?
        base_url = 'http://stat.columbia.edu/~rachel/datasets/nyt'
        # Download the series of CSVs and store the file_list.
        file_list = download_series(base_url, 'csv', 31)
        # Merge the CSVs listed in the file_list into nyt_agg.csv
        merge_csv(file_list, 'nyt_agg.csv')
    
    # read nyt_agg.csv into a pandas DataFrame
    df = pd.read_csv(DATA_DIR + 'nyt_agg.csv')

    return df

# Call the function which loads the NYT dataset into a DataFrame
df = load_nytimes_dataset()

# Aggregate by 'Age','Gender','Signed_In' to summarise for the whole group.
dfg = df.groupby(['Age','Gender','Signed_In'])

# Find the mean for "Clicks", "Impressions", given the groupings 
dfg = dfg["Clicks", "Impressions"].mean()

# Add a new column with the CTR
dfg["CTR"] = dfg["Clicks"] / dfg["Impressions"]

# Only export the relevant data, CTR with indices.
dfg["CTR"].to_csv(DATA_DIR + 'nytimes_agg_CTR.csv')