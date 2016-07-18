#!/usr/bin/env python

# from __future__ import print_function, division, absolute_import, unicode_literals
from __future__ import print_function, division, absolute_import
import argparse
import json
import os.path
import sys

HISTORY = "./pairwise_history.json"
# pairwise_history.json is a dictionary with keys of ISO8601 timestamps
# and value of a list of pair_lists
COWORKERS = "./pairwise_coworkers.json"
# list of lists of mutual coworkers.  If more than 2 people work together,
# put them in the same list.  All pairwise combinations will be created.
NAMES = "./pairwise_names.json"
# pairwise_names.json is a list of all the names in the rota
RELEVANT_HISTORY = 8
# RELEVANT_HISTORY controls how much recent history is used for ensuring
# matches are not repeated.  Set to zero (0) to ignore


def parse_cli(test_args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--names", default=NAMES,
                        help="File for the list participant names")
    parser.add_argument("member", help="Member to add to names list")
    if test_args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(test_args)
    return args


def load_names(args):
    """Loads the names from JSON"""
    # NAMES is a json document which is just a list of names
    if os.path.isfile(args.names):
        with open(args.names, 'r') as n:
            try:
                names = json.load(n)
            except:
                sys.exit("ERROR: {0} is invalid JSON".format(args.names))
    else:
        names = []
    return names


def save_names(args, names):
    """Saves the names to JSON"""
    # NAMES is a json document which is just a list of names
    with open(args.names, 'w') as n:
        try:
            json.dump(names, n, sort_keys=True, indent=4)
        except:
            sys.exit("ERROR! Failed to overwrite args.names")


def main():
    args = parse_cli()
    names = load_names(args)
    if args.member in names:
        names.remove(args.member)
    else:
        sys.exit("ERROR: Could not find {0} in list of names".format(args.member))
    save_names(args, names)


if __name__ == "__main__":
    main()
