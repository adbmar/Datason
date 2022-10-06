#! /usr/bin/python

# Author: Addison Martin
# This script is a module for the Datason package
# This script takes as its input either a pipe or a file
# The pipe or file is a fasta file. The script will spit out
# various statistics for all sequences in the file and saves
# a histogram of fasta lengths at the designated path.
# Intended for quick summative analysis of contents of fasta
# files.

import matplotlib, sys, os, argparse, statistics
import matplotlib.pyplot as plt
matplotlib.use('Agg')

class Fasta:
    # Class to handle individual fasta sequences with their headers
    def __init__(self, header, sequence):
        self.head = str(header.replace("\n", "").replace(" ", ""))
        self.seq = str(sequence.replace("\n", "").replace(" ", ""))

def import_fastas_as_list(source):
    # Function that imports fasta files from either piped input or from file path
    # Fasta sequences in the file will be returned as a list of all the
    # fasta sequences in the file as Fasta objects (defined above)
    # Source is intended to be the source as a string of characters
    try:
        # Removing comments that sometimes preceed actual fasta sequences in some fasta files
        source = source[source.index(">"):]
    except ValueError:
        print("There was no greater than symbol in the file; it appears to not be a fasta file")
        exit()
    print(source)
    split_fasta = source.split(">")
    del split_fasta[0]
    split_fasta = [fasta.split("\n",1) for fasta in split_fasta]
    print(split_fasta)
    return_list = [Fasta(fasta[0], fasta[1]) for fasta in split_fasta]
    while return_list[0] == Fasta("",""):
        del return_list[0]
    return(return_list)

def get_stats(fasta_list, inclusive_GC_status = False):
    # Function that returns statistics about the Fasta obejcts in a list
    # of Fasta objects. The returned statistics are returned as a tuple
    # in the following order: GC content of all sequences, average sequence
    # length, max sequence length, min sequence length, and median sequence
    # length
    if inclusive_GC_status == True: compare_set = set(["G", "C"])
    else: compare_set = set(["G", "C", "R", "Y", "K", "M", "S", "B", "D", "H", "V", "N"])
    total_bases = 0
    g_or_c_bases = 0
    fasta_count = 0
    for fasta in fasta_list:
        fasta_count += 1
        total_bases += len(fasta.seq)
        for base in fasta.seq:
            if set(base) <= compare_set:
                g_or_c_bases += 1
            else:
                continue
    len_fasta_list = [len(fasta.seq) for fasta in fasta_list]
    return(g_or_c_bases/total_bases, total_bases/fasta_count, max(len_fasta_list), min(len_fasta_list), statistics.median(len_fasta_list))
    #Tuple order: GC content, average, max, min, median

def main():
    # Main block

    #Argument parsing
    parser = argparse.ArgumentParser(description = "This module takes as an input a fasta file (or a piped fasta file) and will display various statistics about the sequences contained in that file. Specifically, it will display the average, maximum, minimum, and median sequence length as well as displaying the GC content of the entire file. The module will also save a png image of a histogram of fasta lengths at the path given to it.")
    parser.add_argument(
        "-o", "--out",
        help = "Path to file where histogram of fasta lengths will be saved",
        type = str,
        dest = "out",
        required = True)
    parser.add_argument(
        "-i", "--in",
        help = "File location for input; if not provided script looks for pipe input",
        type = str,
        required = False,
        dest = "in_file")
    parser.add_argument(
        "-v", "--verbose",
        action = "store_true",
        default = False,
        dest = "verbose")
    parser.add_argument(
        "-g", "--gc_inclusive",
        help = "Flag that when used indicates use of inclusive GC content symbols (i.e. nucleotide symbols that COULD indicate a G or C will be counted as G or C)",
        action = "store_true",
        dest = "gc",
        required = False)
    parser.add_argument(
        "-b", "--bins",
        help = "Number of bins in histogram",
        type = int,
        default = 200,
        required = False)
    parser.add_argument(
        "-t", "--title",
        help = "Optional title for histogram",
        type = str,
        default = "Fasta lengths",
        required = False)
    args = parser.parse_args()

    #Out file handling
    outfile_path = os.path.abspath(args.out)
    
    #In file handling
    if args.in_file != None:
        #if in file is provided
        if args.verbose == True: print(f"In file provided to script. Importing {args.in_file}")
        with open(os.path.abspath(args.in_file), "r") as f:
            source = f.read()
    else:
        #if no in file is provided (i.e. getting from pipe)
        if args.verbose == True: print(f"No in file provided to script, Using pipe as input")
        if sys.stdin.isatty():
            source = sys.stdin.read()
        else:
            if args.verbose == True: print(f"No piped input found; quitting")
            exit()
    
    #Importing fasta
    fasta_list = import_fastas_as_list(source)
    if args.verbose == True: print(f"Imported {len(fasta_list)} fasta sequences from {args.in_file}")
    if args.verbose == True:
        for fasta in fasta_list:
            print(fasta.seq)
        print([len(fasta.seq) for fasta in fasta_list])

    #Analyzing and printing fasta sequence stats
    if args.verbose == True: print(f"Acquiring statistics on fasta sequences...")
    stats = get_stats(fasta_list, args.gc)
    print(f"Average length: {stats[1]}")
    print(f"Maximum length: {stats[2]}")
    print(f"Minimum length: {stats[3]}")
    print(f"Median length:  {stats[4]}")
    print(f"GC Content:     {stats[0]}")

    #Exporting fasta length histogram
    print(f"Saving histogram to {outfile_path}")
    plt.hist([len(fasta.seq) for fasta in fasta_list], density = False, bins = args.bins)
    plt.ylabel("Occurences")
    plt.xlabel("Fasta sequence length")
    plt.title(args.title)
    plt.savefig(outfile_path)
    plt.show()

if __name__ == "__main__":
    main()
