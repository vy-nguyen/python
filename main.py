#!/usr/bin/python

#
# Written by Vy Nguyen
#
import os
import argparse

from pprint  import pprint
from Global  import Global
from SymTab  import SymTab

def main(in_file):
    glob = Global()
    glob.run_file(in_file)
    glob.main()
    glob.debug_dump()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', nargs = 1, help = 'Input .json file to run');

    args = parser.parse_args();
    if not args.file:
        parser.print_usage()
        parser.exit()

    main(args.file)
