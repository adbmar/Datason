#! /usr/bin/python

# Author: Addison Martin
# This script is a module for the Datason package
# This script takes as its input either a pipe or a file
# The pipe or file is a list of two integers with a consistent
# delimiter between them. The script will plot a 2D histogram
# of these numbers at the specified file location. Originally
# intended to be used with piping on unix but can also use 
# input files

def main():
    import sys, os, argparse
    import matplotlib.pyplot as plt
    import matplotlib as mpl

    def clean_list(list):
    # Function for cleaning out blank items in the beginning/end of a list
        while list[0] == "":
            list.pop(0)
        while list[-1] == "":
            list.pop(-1)

    def check_data(data, sep):
        # Function for checking if all items in a list of lists are integers
        # Protects script by quitting if not all items are integers
        for datum in data:
            try: datum = datum.split(sep)
            except:
                print(f"Note: Seperator not found in one line\n Line that caused failure: {datum}")
                exit()
            for d in datum:
                try: int(d)
                except:
                    print(f"Note: One line from input was not an integer\n  Line that caused entry failure: {datum}")
                    exit()
    
    def check_lists(lista, listb):
        # Function that checks that two list are equal in length
        # Protects script by quitting if both lists are not equal in length
        if len(lista) != len(listb):
            print("Note: data lists provided to script are not equal to one another in length\n Check your data!")
            exit()

    #####################
    # Parsing arguments #
    #####################
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose",
        action = "store_true",
        default = False,
        dest = "verbose")
    parser.add_argument(
        "out",
        help = "File location to save histogram image",
        type = str)
    parser.add_argument(
        "-i", "--in",
        help = "File location for input; if not provided script looks for pipe input",
        type = str,
        dest = "inf")
    parser.add_argument(
        "--header",
        help = "Flag that indicates the first data points are headers",
        action = "store_true",
        dest = "head")
    parser.add_argument(
        "-t", "--title",
        help = "Title to put on graph; note that this must be one string with no spaces",
        type = str,
        dest = "title")
    parser.add_argument(
        "-s", "--seperator",
        help = "String that separates the two values",
        type = str,
        dest = "sep",
        default = "\t")
    parser.add_argument(
        "-l", "--log",
        help = "When this flag is present, axes in plot will be in log scale",
        action = "store_true",
        dest = "log_scale")
    args = parser.parse_args()
    print(args)

    #################
    # File handling #
    #################

    # Output file handling
    outfile = os.path.abspath(args.out)
    if args.verbose == True: print(f"Outputting histogram to {outfile}")
    
    # Input handling
    if args.inf != None:
        # In file if file is provided -- gets content of file as list called data
        in_file = open(os.path.abspath(args.inf), "r")
        data = in_file.read()
        in_file.close()
        data = data.split("\n")
        if args.verbose == True: print(f"Received an -in argument; reading from file {args.inf}")
    else:
        # In file if file is not provided -- wrangles content of piped input as list called data
        if args.verbose == True: print(f"Received no -in argument; using pipe input")
        if sys.stdin.isatty():
            print("No piped input to script and no in file. Quitting...")
            exit()
        else:
            data = sys.stdin.readlines()
            data = [datum.strip() for datum in data]
    
    # Cleaning input data
    clean_list(data)
    check_data(data, args.sep)
    if args.verbose == True: print(f"Working with the following data: {data}")

    # Handling of header flag
    if args.head == True & args.verbose == True: print(f"Received --header flag: using first data as header")
    elif args.head == False & args.verbose == True: print(f"Received no --header flag")
    if args.head == True:
        header = data.pop(0)
        header_x = header.split(args.sep)[0]
        header_y = header.split(args.sep)[1]

    # Processing data into x and y lists
    print(data)
    data = [datum.split(args.sep) for datum in data]
    data_x = [int(datum[0]) for datum in data]
    data_y = [int(datum[1]) for datum in data]
    print(data_x)
    print(data_y)
    check_lists(data_x, data_y)

    # Getting statistics from data for plotting and exporting proportions
    min_x = min(data_x) - 1
    max_x = max(data_x)+1
    min_y = min(data_y)-1
    max_y = max(data_y)+1
    bins_x = range(min_x, max_x, 1)
    bins_y = range(min_y, max_y, 1)
    n_bin_x = max_x - min_x
    n_bin_y = max_y - min_y

    # Plotting
    if args.log_scale == True:
        scale = mpl.colors.LogNorm()
    else:
        scale = None
    plot = plt.hist2d(data_x, data_y, bins=[n_bin_x,n_bin_y], norm = scale, cmap=plt.cm.Greys)
    plt.colorbar()
    
    if args.title != False: plt.title(args.title)
    if args.head == True:
        plt.xlabel(header_x)
        plt.ylabel(header_y)
    plt.savefig(outfile)

    print(f"Plot image saved to {outfile}")


if __name__ == "__main__":
    main()
