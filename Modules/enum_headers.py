#! /usr/bin/python

# Author: Addison Martin
# Datason is a suite of scripts that provide useful data wrangling functions that
# I developed for various uses during my PhD.
# This is a script that is used for enumerating headers in a text file (most
# likely a csv file). This is intended to quickly give you the index of
# a column instead of opening a file and counting the headers manually. The
# script will take in the file and print results to the command line

import argparse, os

def main_block(in_file, sep, starting_index):
    # Function that does the main task of parsing out the first row of the file,
    # splitting up the first row based on the seperator, and
    # printing out the 
    header = in_file.readline()
    separated_header = header.split(sep)
    i = starting_index
    j = 0
    print(f"The file contains the following {len(separated_header)} column headers as indexed: (starting with index of {starting_index} as first index)")
    for title in separated_header:
        print(f"{i} - {separated_header[j]}")
        i =+ 1
        j =+ 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose",
        action = "store_true",
        default = False,
        dest = "verbose")
    parser.add_argument(
        "in_file",
        help = "File location of file of interest",
        type = str)
    parser.add_argument(
        "-s", "--sep",
        help = "Character (or string of characters) used as separator in this file",
        type = str,
        required = False,
        default = ",",
        dest = "sep")
    parser.add_argument(
        "--index",
        help = "Integer value of first index (usually 0 or 1)",
        type = int,
        required = False,
        default = 0)
    args = parser.parse_args()

    print(f"Reading file: {os.path.abspath(args.in_file)}")
    with open(args.in_file, "r") as in_file:
        main_block(in_file, args.sep, args.index)

if __name__ == "__main__":
    main()