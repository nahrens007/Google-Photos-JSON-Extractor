"""
Google Photos JSON Extractor

Author: Nathan Ahrens

This script extracts metadata from Google Photos JSON files and matches them with their corresponding image files
based on various naming conventions. It updates a CSV file containing metadata for a Google Photos library, adding
the path to the JSON file for each image file in the library. The CSV file is then ready to be imported into another 
script that will open the JSON file and actually read the metadata from the JSON file. 

Usage: python extract_json.py

Dependencies: pandas (https://pandas.pydata.org/)
"""

import pandas as pd
import os

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv("out.csv")

# Add an empty "JsonFile" column to the DataFrame
df["JsonFile"] = pd.Series(dtype=str)

# Define a function to find the JSON file name for a given image file name
def find_json_file(row):
    # Check if the JSON file path is already present in the row
    if pd.notna(row["JsonFile"]):
        return row["JsonFile"]

    # Check if the "DateTimeOriginal" column is empty (no need to look for JSON if it is populated)
    if pd.isna(row["DateTimeOriginal"]):
        # Only consider JPEG and PNG files
        if not row["SourceFile"].lower().endswith((".jpg", ".jpeg", ".png")):
            return None

        # Get the directory, base name, and extension of the image file
        directory = os.path.dirname(row["SourceFile"])
        basename,ext = os.path.splitext(row["FileName"])

        # If there are no 
        

        # If basename has parentheses in it, extract the text between
        # the parentheses as 'n', and build the new file name by removing the last 3 
        # characters from the basename, adding the original file extension 'ext', 
        # 'n' surrounded by parentheses, and the '.json' extension.
        # In other words, for a file such as "IMG_1667(1).jpg", the corresponding
        # json file would be "IMG_1667.jpg(1).json" (moving the "(1)").
        n = None
        if "(" in basename and basename.endswith(")"):
            n = basename.split("(")[-1].split(")")[0]
            json_basename = f"{basename[:-3]}{ext}({n}).json"
        # If the basename is now ending with "-edited", remove that portion, 
        # add back on the extention, and add .json. 
        # Thus, a file such as "Snapchat-1068254512-edited.jpg" has json "Snapchat-1068254512.jpg.json"
        elif basename.endswith("-edited"):
            json_basename = f"{basename[:-7]}{ext}.json"
        # If there are no parentheses or "-edited" in the basename, simply add the 
        # '.json' extension to the basename.
        else: 
            json_basename = f"{row['FileName']}.json"

        # Try to find a JSON file in the same directory, with the same base name in the DataFrame.
        # Not using df[df["SourceFile"] == f"{directory}/{json_basename}"], or even 
        # df[df["SourceFile"] == f"{os.path.join(directory,json_basename)}"]  
        # because OS used to generate csv file and OS used to parse the csv could differ.
        json_rows = df[df["SourceFile"].str.startswith(directory) & df["SourceFile"].str.endswith(json_basename)]
        if len(json_rows) > 0:
            return json_rows.iloc[0]["SourceFile"]
        
        # Next search for json without the image file extension: 
        # base file: content_media_external_images_media_1000001232.jpg
        # json file: content_media_external_images_media_1000001232.json
        json_rows = df[df["SourceFile"].str.startswith(directory) & df["SourceFile"].str.endswith(f"{basename}.json")]
        if len(json_rows) > 0:
            return json_rows.iloc[0]["SourceFile"]
        
        # Next search for json WITH the image full name: 
        # base file: signal-2021-10-13-211744 (2).jpg
        # json file: signal-2021-10-13-211744 (2).jpg.json
        json_rows = df[df["SourceFile"].str.startswith(directory) & df["SourceFile"].str.endswith(f"{basename}{ext}.json")]
        if len(json_rows) > 0:
            return json_rows.iloc[0]["SourceFile"]

    # If the "DateTimeOriginal" column is not empty or no JSON file was found, return None
    return None

# Apply the find_json_file function to each row in the DataFrame to create the "JsonFile" column
df["JsonFile"] = df.apply(find_json_file, axis=1)

# Filter the DataFrame to only include rows for images where "DateTimeOriginal" is empty
df = df[(df["SourceFile"].str.lower().str.endswith((".jpg", ".jpeg", ".png"))) & (df["DateTimeOriginal"].isna())]

# Save the updated DataFrame to a new CSV file
df.to_csv("out_with_json.csv", index=False)

# Evaluate and print results
notna_rows = df["JsonFile"].notna().sum()
na_rows = df["JsonFile"].isna().sum()
print(f"Found matching JSON file for {notna_rows} photos.\nCould not find matching JSON file for {na_rows} photos.") 
