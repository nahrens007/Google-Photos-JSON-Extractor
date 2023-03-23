"""
Google Photos - Metadata Evaluator

Author: Nathan Ahrens

This script loads a CSV file containing metadata for a Google Photos library and 
displays results: how many photos have, and do not have, the DateTimeOriginal metadata tag.

Usage: python evaluate_results.py

Dependencies: pandas (https://pandas.pydata.org/)
"""

import pandas as pd

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv("results.csv")

# Evaluate df
notna_rows = df["DateTimeOriginal"].notna().sum()
na_rows = df["DateTimeOriginal"].isna().sum()
print(f"{notna_rows} photos have DateTimeOriginal.\n{na_rows} photos do not have DateTimeOriginal.") 
