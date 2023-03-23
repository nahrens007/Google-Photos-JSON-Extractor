"""
Google Photos "photoTakenTime" metadata loader

Author: Nathan Ahrens

This script extracts metadata from Google Photos JSON files and adds it to a column and writes the final CSV. 
The CSV file is then ready to be used to load the metadata in the images using exiftool: 
find /mnt/e/takeout-20230312T190809Z-001/Takeout/Google\ Photos/ -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) -print0 | xargs -0 exiftool -csv=out_with_metadata.csv -overwrite_original -tagsfromfile @ -DateTimeOrigininal -csv-delimiter ,

Usage: python extract_json.py

Dependencies: pandas (https://pandas.pydata.org/)
"""

import pandas as pd
import json
import datetime

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv("out_with_json.csv")

# Filter out NA values
df = df[df["JsonFile"].notna()]

def set_dt(row): 
    # Check if the "DateTimeOriginal" column is populated
    if pd.notna(row["DateTimeOriginal"]):
        return row["DateTimeOriginal"]
    
    # Check if JsonFile is populated (nothing to do)
    if pd.isna(row["JsonFile"]):
        return None
    
    try: 
        with open(row["JsonFile"],'r') as file:
            content = json.loads(file.read()) 
            # format: 2022:05:26 16:03:39
            return datetime.datetime.fromtimestamp(int(content['photoTakenTime']['timestamp'])).strftime("%Y:%m:%d %H:%M:%S")
    except: 
        print(f"Couldn't load {row['JsonFile']}")
        return None

# Update DateTimeOriginal, and drop all columns that we don't need, and write to CSV
df["DateTimeOriginal"] = df.apply(set_dt, axis=1)
df.drop(columns=["JsonFile","FileName","FileSize","Model","Flash","ImageSize","FocalLength","ShutterSpeed","Aperture","ISO","WhiteBalance"], axis=1, inplace=True)
df.to_csv("out_with_metadata.csv", index=False)
