#! /usr/bin/python

# Author: Addison Martin
# This script is a module for the Datason package
# This script takes as its input either a pipe or a file
# The pipe or file is a list of integers with each number
# on a new row. The script will plot a histogram of these numbers
# at the specified file location. Originally intended to be
# used with piping on unix but can also use input files

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

    def check_data(data):
        # Function for checking if all items in a list are integers
        # Protects script by quitting if not all items are integers
        for datum in data:
            try: int(datum)
            except:
                print(f"Note: One line from input was not an integer\n  Line that caused entry failure: {datum}")
                exit()
        
    def proportion_printing(data, min_datum, max_datum):
        # Function for proportion printing 
        # which involves printing the proportion of data represented
        # by each integer in the range of data values
        total = len(data)
        proportion = {}
        for i in range(min_datum,max_datum,1):
            count = 0
            for datum in data:
                if datum == i:
                    count += 1
            proportion[i]=count/total
        sorted_proportion = sorted(proportion.items())
        print(sorted_proportion)

    #####################
    # Parsing arguments #
    #####################
    parser = argparse.ArgumentParser(description = "This module was originally conceived as a tool to pipe into an awk command from a csv file. Thus it takes as its input a list of integers separated by the newlines (whether from an input file or from a pipe). The module will then save a png image of a histogram of the integers in this list.")
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
        required = False,
        dest = "inf")
    parser.add_argument(
        "--header",
        help = "Flag that indicates the first data points are headers",
        action = "store_true",
        required = False,
        dest = "head")
    parser.add_argument(
        "-t", "--title",
        help = "Title to put on graph; note that this must be one string with no spaces",
        type = str,
        dest = "title")
    args = parser.parse_args()
    if args.verbose == True: print(f"The following arguments were received: {args}") # for troubleshooting

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
    
    # Handling of header flag
    if args.head == True & args.verbose == True: print(f"Received --header flag: using first data as header")
    elif args.head == False & args.verbose == True: print(f"Received no --header flag")
    if args.head == True:
        header = data.pop(0)
    
    # Cleaning input data
    clean_list(data)
    check_data(data)
    data = [int(datum) for datum in data]
    if args.verbose == True: print(f"Working with the following data: {data}")

    # Getting statistics from data for plotting and exporting proportions
    min_datum = min(data)-1
    max_datum = max(data)+1
    bins = range(min_datum,max_datum,1)

    # Proprtion printing
    if args.verbose == True:
        proportion_printing(data, min_datum, max_datum)

    # Plotting
    try:
        _, _, plot = plt.hist(data, density=False, align="mid", bins=bins)
        for point in plot:
            x = (point._x0+point._x1)/2
            y = point._y1 + 0.05
            plt.text(x,y, point._y1)
    except:
        plot = plt.hist(data,density=False, align="mid", bins=bins)
    plt.ylabel('Counts')
    if args.head == True: plt.xlabel(header)
    else: plt.xlabel("Values")
    if args.title != False: plt.title(args.title)
    plt.savefig(outfile)
    print(f"Plot image saved to {outfile}")


if __name__ == "__main__":
    main()
