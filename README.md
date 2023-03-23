# Google Photos JSON Matcher
This repository contains a Python script that matches image files (jpg, jpeg, png) downloaded from Google Photos with their associated JSON files. The script uses a CSV file generated from ExifTool to find the matching JSON files. 

## Description

This script matches JSON files to associated image files (jpg, jpeg, and png) downloaded from Google Takeout extract of Google Photos.

## Installation

1. Clone the repository: `git clone https://github.com/redninja2/Google-Photos-JSON-Extractor.git`
2. Install required libraries: `pip install pandas`

## Usage

1. Generate a CSV file using ExifTool with the following command (replace directory with your directory): `exiftool -common -csv "/mnt/e/takeout-20230312T190809Z-001/Takeout/Google Photos/" > out.csv` 
2. Run the script: `python json_matcher.py`

The script will output a CSV file with the matched image and JSON files.

## License

This project is licensed under the [MIT License](LICENSE).




