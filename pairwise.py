#!/usr/bin/env python

# from __future__ import print_function, division, absolute_import, unicode_literals
from __future__ import print_function, division, absolute_import
import argparse
import copy
import datetime
import itertools
import json
import os.path
import random
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
    parser.add_argument("--history", default=HISTORY,
                        help="File for pair history")
    parser.add_argument("--coworkers", default=COWORKERS,
                        help="File for lists of coworkers")
    parser.add_argument("--names", default=NAMES,
                        help="File for the list participant names")
    parser.add_argument("--relevant-history", default=RELEVANT_HISTORY,
                        dest='relevant_history',
                        help="Number of past pairings to consider when "
                             "validating pairs")
    parser.add_argument("-d", "--dry-run", dest="dry_run", action='store_true',
                        help="dry run everything")
                                                     
    if test_args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(test_args)
    return args


def make_pairs(innames):
    """
    Makes a randomized pairs from the innames list.
    If the length is odd, a sublist of 3 will be created.
    """
    names = copy.deepcopy(innames)
    pairs = []
    if len(names) % 2 == 1:
        m = random.randint(0, len(names) - 1)
        singleton = names[m]
        del names[m]
    else:
        singleton = None
    while len(names) > 0:
        i = 0
        j = 0
        while i == j:
            i = random.randint(0, len(names) - 1)
            j = random.randint(0, len(names) - 1)
        # print("i is", i, "j is", j)
        k = names[i]
        l = names[j]
        # print("k is", k, "l is", l)
        if i > j:
            del names[i]
            del names[j]
        else:
            del names[j]
            del names[i]
        # print("names is", repr(names))
        if singleton is None:
            pairs.append(set([k, l]))
        else:
            pairs.append(set([k, l, singleton]))
            singleton = None
    return pairs


def validate_pairs(pairs, historical_pairs):
    """
    Compares pairs with historical_pairs.  If any pair in pairs exists in
    historical_pairs, return False (reject the pair set)
    """
    if pairs is None:
        return False
    for p in pairs:
        if p in historical_pairs:
            return False
    return True


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
        sys.exit("ERROR {0} file not found.".format(args.names))
    if len(names) <= 1:
        sys.exit("ERROR: {0} needs to have more than 1 name in it".format(args.names))
    return names


def prune_history(metahistory, relevant_history):
    """
    Prunes the historical pairs, and returns a list of sets of relevant
    pairs based on relevant_history
    """
    historical_pairs = []
    # Show only the relevant keys:
    relevant_dates = sorted(metahistory.keys())[0 - relevant_history:]
    for date in relevant_dates:
        for p in metahistory[date]:
            historical_pairs.append(set(p))
    return historical_pairs


def load_history(args):
    """Loads the historical pairs from JSON"""
    # history is a json document as a big dictionary
    # the keys are date/timestamps. The result is a list of pairlists
    # only will return the 'relevant' pairs, meaning the most recent
    # RELEVANT_HISTORY ones.
    if os.path.isfile(args.history):
        with open(args.history, 'r') as h:
            metahistory = json.load(h)
    else:
        metahistory = {}
    return prune_history(metahistory, args.relevant_history)


def load_coworkers(args):
    """Loads the coworker pairings from JSON.
    If more than 2 are in a list, return all pairwise combinations"""
    if os.path.isfile(args.coworkers):
        with open(args.coworkers, 'r') as c:
            list_coworkers = json.load(c)
    else:
        list_coworkers = []
    coworkers = []
    for coworker_set in list_coworkers:
        for pair in itertools.combinations(coworker_set, 2):
            # print("pair is {}".format(pair))
            coworkers.append(set(pair))
    return coworkers


def update_history(pairs, args):
    if os.path.isfile(args.history):
        with open(args.history, 'r') as h:
            history = json.load(h)
    else:
        history = {}
    dts = datetime.datetime.now().isoformat(' ')
    pair_list = []
    for p in pairs:
        pair_list.append(list(p))
    history[dts] = pair_list
    with open(args.history, 'w') as h:
        json.dump(history, h)


def print_pairs(pairs):
    counter = 0
    for pair in pairs:
        counter += 1
        p = sorted(list(pair))
        if len(pair) == 2:
            print("Pair {0:02d}: {1} and {2}".format(counter, p[0], p[1]))
        elif len(pair) == 3:
            print("Pair {0:02d}: {1}, {2} and {3}".format(counter, p[0], p[1], p[2]))
        else:
            print("A serious error happened.  A pair should be either 2 or 3 people, not {}.".format(len(pair)))


def main():
    args = parse_cli()
    names = load_names(args)
    historical_pairs = load_history(args)
    historical_pairs.extend(load_coworkers(args))
    pairs = None
    validation_checks = 0
    validation_succeeded = True
    while validate_pairs(pairs, historical_pairs) is False:
        pairs = make_pairs(names)
        validation_checks += 1
        if validation_checks > len(list(itertools.combinations(names, 2))):
            validation_succeeded = False
            break
    if validation_succeeded:
        print_pairs(pairs)
        
        if args.dry_run is False:
            update_history(pairs, args)
    else:
        print("ERROR: validating pairs failed. There may be something wrong with the availability possible matches.")

if __name__ == "__main__":
    main()
