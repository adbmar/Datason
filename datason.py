#! /usr/bin/python

# Author: Addison Martin
# Datason is a suite of scripts that provide useful data wrangling functions that
# I developed for various uses during my PhD.
# This is the wrapper script for properly executing Datason scripts from the command line
# This script will take in command line and then execute the proper script
# This wrapper script functions by importing modules for command scripts
# so the .py files for modules must be kept in directory with this script

import argparse, os, subprocess

def main():
    # Gets directory of this script to locate module py files
    # Assumption here is that module py files are in the same
    # directory as this script
    directory = os.path.dirname(os.path.realpath(__file__)) 

    # Dictionary to associate command with a .py file
    module_dict = {
        "inthisto" : directory+"/Modules/"+"inthisto.py",
        "inthisto2d" : directory+"/Modules/"+"inthisto2d.py",
        "fastastats" : directory+"/Modules/"+"fastastats.py",
        "enum_headers" : directory+"/Modules/"+"enum_headers.py"}

    # Parsing top level arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        type = str,
        choices = module_dict.keys())
    parser.add_argument(
        "-v", "--verbose",
        action = "store_true",
        default = False,
        dest = "verbose_main")

    # Parsing top level params, running appropriate script, and passing rest of commands to script
    base_args, rest_args = parser.parse_known_args()
    if base_args.verbose_main == True: print(f"Verbose status: {base_args.verbose_main}")
    if base_args.verbose_main == True: print(f"Command: {base_args.command}")
    if base_args.verbose_main == True: print(f"Rest of arguments: {rest_args}")

    #Assembling command to execute modules
    module_path = module_dict.get(base_args.command)
    command = "python3 " + module_path + " " + " ".join(rest_args)
    if base_args.verbose_main == True: print(f"Command to run: {command}\n Running command...")
    subprocess.call(command, shell=True)

if __name__ == "__main__":
    main()