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
notna_rows = len(df[df["DateTimeOriginal"].notna() & df["SourceFile"].str.lower().str.endswith((".jpg", ".jpeg", ".png"))])
na_rows = len(df[df["DateTimeOriginal"].isna() & df["SourceFile"].str.lower().str.endswith((".jpg", ".jpeg", ".png"))])
print(f"{notna_rows} photos have DateTimeOriginal.\n{na_rows} photos do not have DateTimeOriginal.") 
