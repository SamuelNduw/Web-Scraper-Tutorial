import shutil
import csv
import argparse

parser = argparse.ArgumentParser(description='Clean data.')

parser.add_argument('filename', help='File to clean')
parser.add_argument('output_filename', help='Cleaned data file')
args = parser.parse_args()

input_file = args.filename
output_file = args.output_filename

shutil.copy2(input_file, output_file)

with open(input_file, "r", encoding="utf-8") as infile, \
    open(output_file, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        row["Rank"] = int(row["Rank"].replace(".", ""))
        row["Points"] = int(row["Points"].replace(" points", ""))
        row["Comments"] = int(row["Comments"].replace(" comments", "").replace("\xa0comments", ""))
        row["Age"] = row["Age"].replace(" ago", "")

        writer.writerow(row)

print("Cleaning complete. Output saved to:", output_file)